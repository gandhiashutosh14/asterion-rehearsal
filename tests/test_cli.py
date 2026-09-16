import json,sys
from asterion.cli import main

def test_cli_demo_and_review(tmp_path,monkeypatch,capsys):
    base=['asterion','--state-dir',str(tmp_path/'state')]
    monkeypatch.setattr(sys,'argv',base+['demo','--output',str(tmp_path/'out')])
    main();result=json.loads(capsys.readouterr().out)
    assert result['status']=='PENDING_REVIEW'
    monkeypatch.setattr(sys,'argv',base+['review',result['run_id'],'--digest',result['evidence_digest'],'--decision','approve','--rationale','Reviewed this synthetic contract','--output',str(tmp_path/'review')])
    main();assert json.loads(capsys.readouterr().out)['status']=='APPROVED'

def test_cli_happy_only_holds(tmp_path,monkeypatch,capsys):
    monkeypatch.setattr(sys,'argv',['asterion','--state-dir',str(tmp_path/'state'),'demo','--suite','happy-only','--output',str(tmp_path/'out')])
    main();assert json.loads(capsys.readouterr().out)['status']=='HOLD'
