"""Native framework tests. A skip is not framework verification."""
import pytest
pytest.importorskip('langgraph')
pytest.importorskip('langgraph.checkpoint.sqlite')
from asterion.langgraph_runtime import invoke
from asterion.models import RunRequest,ReviewRequest
pytestmark=pytest.mark.framework

def test_interrupt_and_resume_across_connections(tmp_path):
    db=tmp_path/'graph.sqlite'
    s=invoke(db,'thread',RunRequest(engine='langgraph'))
    assert s['status']=='PENDING_REVIEW'
    out=invoke(db,'thread',review_request=ReviewRequest(decision='approve',expected_digest=s['evidence_digest'],rationale='Checked synthetic acceptance'))
    assert out['status']=='APPROVED'

def test_incomplete_does_not_reach_approval(tmp_path):
    s=invoke(tmp_path/'graph.sqlite','thread',RunRequest(engine='langgraph',suite='happy-only'))
    assert s['status']=='HOLD'

def test_failed_run_terminates_without_review(tmp_path):
    s=invoke(tmp_path/'graph.sqlite','thread',RunRequest(engine='langgraph',profile='optimistic'))
    assert s['status']=='BLOCKED'
