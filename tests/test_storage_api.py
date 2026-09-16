import json
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient
from asterion.storage import Ledger, ConflictError, NotFoundError
from asterion.models import RunRequest,ReviewRequest
from asterion.api import create_app
from asterion.reporting import export_dossier, render_html

TOKENS={'operator-012345678901234567890':{'tenant':'a','actor':'operator','role':'operator'},
        'reviewer-012345678901234567890':{'tenant':'a','actor':'reviewer','role':'reviewer'},
        'viewer-01234567890123456789012':{'tenant':'a','actor':'viewer','role':'viewer'},
        'foreign-0123456789012345678901':{'tenant':'b','actor':'foreign','role':'reviewer'}}
def headers(role='operator',key='one'):
    token=next(k for k in TOKENS if k.startswith(role+'-'))
    return {'Authorization':f'Bearer {token}','Idempotency-Key':key}
@pytest.fixture
def client(tmp_path): return TestClient(create_app(tmp_path,TOKENS))
def ready(l): return l.create('a','key',RunRequest())[0]
def req(s,decision='approve'):
    return ReviewRequest(decision=decision,expected_digest=s['evidence_digest'],rationale='Synthetic acceptance reviewed')

def test_idempotent_create_and_restart(tmp_path):
    l=Ledger(tmp_path);s,fresh=l.create('a','key',RunRequest())
    again,fresh2=Ledger(tmp_path).create('a','key',RunRequest())
    assert fresh and not fresh2 and s==again
    with pytest.raises(ConflictError): l.create('a','key',RunRequest(profile='optimistic'))

def test_tenant_scoped_idempotency_and_reads(tmp_path):
    l=Ledger(tmp_path);a=ready(l);b=l.create('b','key',RunRequest())[0]
    assert a['run_id']!=b['run_id']
    with pytest.raises(NotFoundError): l.get('b',a['run_id'])
    assert len(l.list('a'))==1

@pytest.mark.parametrize('decision,status',[('approve','APPROVED'),('reject','REJECTED')])
def test_review_and_no_double_review(tmp_path,decision,status):
    l=Ledger(tmp_path);s=ready(l);out=l.review('a',s['run_id'],req(s,decision),'reviewer')
    assert out['status']==status and out['review']['actor']=='reviewer'
    with pytest.raises(ConflictError): l.review('a',s['run_id'],req(s),'reviewer')

def test_stale_digest_denied(tmp_path):
    l=Ledger(tmp_path);s=ready(l);r=req(s);r.expected_digest='a'*64
    with pytest.raises(ConflictError):l.review('a',s['run_id'],r,'reviewer')

def test_modified_evidence_denied(tmp_path):
    l=Ledger(tmp_path);s=ready(l);s['observations'][0]['observation']['owner']='tampered'
    with l.connect() as db:db.execute('UPDATE runs SET state_json=? WHERE id=?',(json.dumps(s),s['run_id']))
    with pytest.raises(ConflictError):l.review('a',s['run_id'],req(s),'reviewer')

def test_incomplete_cannot_be_approved(tmp_path):
    l=Ledger(tmp_path);s=l.create('a','k',RunRequest(suite='happy-only'))[0]
    with pytest.raises(ConflictError):l.review('a',s['run_id'],req(s),'reviewer')

def test_concurrent_admission_returns_one_run(tmp_path):
    l=Ledger(tmp_path)
    with ThreadPoolExecutor(max_workers=4) as ex:
        out=list(ex.map(lambda _: l.create('a','same',RunRequest()),range(4)))
    assert len({s['run_id'] for s,_ in out})==1 and sum(f for _,f in out)==1

def test_concurrent_review_has_one_winner(tmp_path):
    l=Ledger(tmp_path);s=ready(l)
    def review(_):
        try: return l.review('a',s['run_id'],req(s),'reviewer')['status']
        except ConflictError:return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(review,range(2)))
    assert sorted(out)==['APPROVED','conflict']

@pytest.mark.parametrize('path',['/v1/runs','/v1/runs/not-found'])
def test_auth_required(client,path): assert client.get(path).status_code==401

def test_unconfigured_auth_fails_closed(tmp_path):
    c=TestClient(create_app(tmp_path,{}))
    assert c.get('/healthz').status_code==200
    assert c.get('/v1/runs').status_code==503

def test_role_tenant_and_digest_api(client):
    assert client.post('/v1/runs',json={},headers=headers('viewer')).status_code==403
    response=client.post('/v1/runs',json={},headers=headers())
    assert response.status_code==201,response.text
    s=response.json();path='/v1/runs/'+s['run_id']
    assert client.post('/v1/runs',json={},headers=headers()).status_code==200
    assert client.post('/v1/runs',json={'profile':'optimistic'},headers=headers()).status_code==409
    assert client.get(path,headers=headers('foreign')).status_code==404
    assert client.post(path+'/review',json=req(s).model_dump(),headers=headers()).status_code==403
    assert client.post(path+'/review',json=req(s).model_dump(),headers=headers('reviewer')).status_code==200
    assert client.get(path,headers=headers()).json()['status']=='APPROVED'
    assert client.get('/v1/runs',headers=headers('foreign')).json()==[]

def test_api_rejects_live_sync_planning(client):
    assert client.post('/v1/runs',json={'planner':'bedrock'},headers=headers()).status_code==422

def test_api_report_headers_and_journal(client):
    s=client.post('/v1/runs',json={},headers=headers()).json();path='/v1/runs/'+s['run_id']
    report=client.get(path+'/report',headers=headers())
    assert report.status_code==200 and report.headers['x-content-type-options']=='nosniff'
    events=client.get(path+'/events',headers=headers())
    assert 'event: journal\n' in events.text and 'data: {' in events.text

def test_html_escaping_and_export(tmp_path):
    import hashlib
    l=Ledger(tmp_path/'db');s=ready(l);s['target_version']='<script>alert(1)</script>'
    assert '<script>alert' not in render_html(s)
    export_dossier(s,tmp_path/'out')
    manifest=json.loads((tmp_path/'out'/'manifest.json').read_text())
    assert (tmp_path/'out'/'report.html').exists()
    for name,value in manifest['files'].items():
        assert hashlib.sha256((tmp_path/'out'/name).read_bytes()).hexdigest()==value


def test_unicode_bad_credentials_are_denied_not_server_error(client):
    # Raw non-ASCII header bytes must not make the authentication path return 500.
    response=client.get('/v1/runs',headers={b'authorization':b'Bearer invalid-\xc3\xb1'})
    assert response.status_code==401

def test_invalid_token_configuration_rejected(tmp_path):
    with pytest.raises(ValueError):create_app(tmp_path,{'short':{'tenant':'a','role':'reviewer','actor':'a'}})

def test_review_unknown_run_is_404(client):
    request={'decision':'approve','expected_digest':'a'*64,'rationale':'A proper review rationale'}
    assert client.post('/v1/runs/unknown/review',json=request,headers=headers('reviewer')).status_code==404
