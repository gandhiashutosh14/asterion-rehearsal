import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'src'))
from asterion.models import Contract,Scenario,Witness,RunRequest,ReviewRequest,Observation
from asterion.api import create_app
out=root/'schemas';out.mkdir(exist_ok=True)
for model in [Contract,Scenario,Witness,RunRequest,ReviewRequest,Observation]:
    (out/f'{model.__name__}.schema.json').write_text(json.dumps(model.model_json_schema(),indent=2)+'\n',encoding='utf-8',newline='\n')
import tempfile
with tempfile.TemporaryDirectory() as d:
    (out/'openapi.json').write_text(json.dumps(create_app(Path(d),{}).openapi(),indent=2)+'\n',encoding='utf-8',newline='\n')
