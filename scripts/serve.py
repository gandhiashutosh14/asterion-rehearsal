"""Local API with random, ephemeral demo credentials; never expose to the internet."""
import os,sys,secrets,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import uvicorn
from asterion.api import create_app
if __name__=='__main__':
    tokens={secrets.token_urlsafe(32):{'tenant':'local-demo','role':role,'actor':f'local-{role}'} for role in ['operator','reviewer','viewer']}
    print('Local demo tokens (not saved; do not commit or share):')
    for token,record in tokens.items():print(record['role']+': '+token)
    print('API documentation: http://127.0.0.1:8000/docs')
    uvicorn.run(create_app(token_map=tokens),host='127.0.0.1',port=8000,access_log=False)
