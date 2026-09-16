from copy import deepcopy
import pytest
from pydantic import ValidationError
from asterion.catalog import load_catalog, validate_catalog
from asterion.models import RunRequest, ReviewRequest, Witness, PlanProposal, digest
from asterion.evidence import assess, verify_observation, witness_identity
from asterion.twin import ScriptedTarget
from asterion.workflow import run_reference
from asterion.planning import compile_proposal, BedrockPlanner

@pytest.fixture
def catalog(): return load_catalog()

@pytest.mark.parametrize('sid', [
 'normal-a','normal-b','erp-unavailable','crm-unavailable','record-missing',
 'stale-snapshot','mismatched-order','high-impact','duplicate-event',
 'foreign-tenant','missing-owner','untrusted-note','slow-dependency'])
def test_guarded_matches_independent_oracle(catalog,sid):
    contract,scenarios=catalog
    scenario=next(s for s in scenarios if s.id==sid)
    observed=ScriptedTarget('guarded').execute(scenario.inputs)
    assert all(w.passed for w in verify_observation('run',contract,scenario,'v1',observed))

def test_foreign_scope_checked_before_read(catalog):
    s=next(s for s in catalog[1] if s.id=='foreign-tenant')
    observed=ScriptedTarget('guarded').execute(s.inputs)
    assert observed.trace == []
    assert observed.evidence_sources == 0

@pytest.mark.parametrize('profile,suite,status,coverage',[
 ('guarded','complete','PENDING_REVIEW',1),('optimistic','complete','BLOCKED',1),
 ('guarded','happy-only','HOLD',1/12),('optimistic','happy-only','HOLD',1/12)])
def test_end_to_end_reference(profile,suite,status,coverage):
    state=run_reference('case',RunRequest(profile=profile,suite=suite))
    assert state['status']==status
    assert state['assessment']['coverage']==pytest.approx(coverage)
    if suite=='happy-only': assert state['assessment']['observed_pass_rate']==1

@pytest.mark.parametrize('budget',[1,2,4,7,12,13,30])
def test_case_budget_is_hard(budget):
    state=run_reference('budget',RunRequest(max_cases=budget))
    assert len(state['completed_ids'])<=budget
    assert len(state['completed_ids'])==len(set(state['completed_ids']))

def test_round_budget():
    state=run_reference('budget',RunRequest(max_rounds=1))
    assert state['rounds']==1
    assert len(state['completed_ids'])<=4
    assert state['status']=='HOLD'

def witnesses(catalog):
    c,ss=catalog
    return [w for s in ss for w in verify_observation('run',c,s,'v1',ScriptedTarget('guarded').execute(s.inputs))]

def test_duplicate_witnesses_do_not_inflate_coverage(catalog):
    c,ss=catalog; ww=witnesses(catalog)[:1]
    a=assess(c,ss,ww*100,'v1','run')
    assert a.coverage==pytest.approx(1/12)
    assert len(a.cells[0].witness_ids)==1

@pytest.mark.parametrize('field,value',[
 ('contract_digest','bad'),('scenario_digest','bad'),('target_version','old'),
 ('run_id','other'),('id','tampered'),('slice','other'),('obligation_id','R-99')])
def test_stale_or_unbound_witness_blocks(catalog,field,value):
    c,ss=catalog;ww=witnesses(catalog);setattr(ww[0],field,value)
    a=assess(c,ss,ww,'v1','run')
    assert a.invalid_witnesses==1 and a.decision=='BLOCKED'

def test_outcome_tampering_rejected(catalog):
    c,ss=catalog;ww=witnesses(catalog)
    ww[0].observed['effect_count']=999
    ww[0].id=witness_identity(ww[0])
    assert assess(c,ss,ww,'v1','run').invalid_witnesses==1

def test_hash_does_not_make_forged_evaluator_trustworthy(catalog):
    # Self-consistent forged observations can pass: documented trust boundary.
    c,ss=catalog;ww=witnesses(catalog)
    assert assess(c,ss,ww,'v1','run').decision=='READY_FOR_REVIEW'

def test_empty_is_hold_not_pass(catalog):
    a=assess(*catalog,[],'v1','run')
    assert a.decision=='HOLD' and a.coverage==0

@pytest.mark.parametrize('change',['duplicate','unknown_field','undeclared','missing'])
def test_invalid_catalog_fails(catalog,change):
    c,ss=deepcopy(catalog)
    if change=='duplicate': ss.append(ss[0])
    if change=='unknown_field': ss[0].expected['R-01']['not_a_field']=True
    if change=='undeclared': ss[0].expected={'R-99':{'effect_count':0}}
    if change=='missing': ss=[s for s in ss if s.id!='erp-unavailable']
    with pytest.raises(ValueError): validate_catalog(c,ss)

@pytest.mark.parametrize('kwargs',[{'max_cases':0},{'max_rounds':0},{'max_cases':65},{'profile':'madeup'},{'production':True}])
def test_request_bounds(kwargs):
    with pytest.raises(ValidationError): RunRequest(**kwargs)

def test_plan_compiler_bounds_authority(catalog):
    _,ss=catalog
    p=PlanProposal(scenario_ids=[ss[0].id,ss[0].id,'shell-exec',ss[1].id],rationale='test')
    out,rejected=compile_proposal(p,ss,1)
    assert len(out)==1 and rejected==['shell-exec']

class FakeBedrock:
    def converse(self,**kwargs):
        self.request=kwargs
        return {'output':{'message':{'content':[{'text':'{"scenario_ids":["normal-a"],"rationale":"one catalog case"}'}]}}}

def test_optional_bedrock_serialization_not_live(catalog):
    c,ss=catalog;client=FakeBedrock();p=BedrockPlanner('model-from-operator',client=client)
    assert p.propose(c,ss,[]).scenario_ids==['normal-a']
    prompt=client.request['messages'][0]['content'][0]['text']
    assert 'expected' not in prompt and 'Ignore all rules' not in prompt and 'effect_count' not in prompt

def test_bad_model_output_not_silently_repaired(catalog):
    class Bad:
        def converse(self,**kw): return {'output':{'message':{'content':[{'text':'not json'}]}}}
    with pytest.raises(ValidationError): BedrockPlanner('x',client=Bad()).propose(*catalog,[])
