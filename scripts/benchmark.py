"""Four fully synthetic, deterministic-policy case studies; not model benchmarking."""
from pathlib import Path
import argparse,hashlib,importlib.metadata,json,platform,sys,time
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from asterion.models import RunRequest
from asterion.workflow import run_reference
from asterion.reporting import export_dossier

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('reports/reference'))
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    results=[]
    for profile,suite in [('optimistic','happy-only'),('optimistic','complete'),('guarded','happy-only'),('guarded','complete')]:
        start=time.perf_counter();request=RunRequest(profile=profile,suite=suite)
        state=run_reference(f'benchmark-{profile}-{suite}',request)
        elapsed=time.perf_counter()-start
        export_dossier(state,args.output/f'{profile}-{suite}')
        a=state['assessment']
        results.append({'profile':profile,'suite':suite,'scenarios':len(state['completed_ids']),
                        'required_cells':len(a['cells']),'covered_cells':sum(c['status']!='MISSING' for c in a['cells']),
                        'failed_cells':len(a['failed_cells']),'coverage':a['coverage'],
                        'observed_witness_pass_rate':a['observed_pass_rate'],'state':state['status'],
                        'elapsed_seconds':round(elapsed,6),'evidence_digest':state['evidence_digest']})
    root=Path(__file__).resolve().parents[1]
    manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'src').rglob('*')) if p.is_file() and p.suffix in {'.py','.json','.yaml'}}
    payload={'kind':'synthetic-policy-case-study','engine':'reference','planner':'deterministic',
             'generated_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
             'dependencies':{k:importlib.metadata.version(k) for k in ['pydantic','PyYAML']},
             'scope':'No LLM, network, live connector, cloud deployment or production certification.',
             'command':'python scripts/benchmark.py','results':results,'source_sha256':manifest}
    (args.output/'summary.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8',newline='\n')
    md=['# Synthetic deployment rehearsal — measured reference results','',payload['scope'],'',
        '| Policy | Suite | Cases | Coverage | Witness pass rate | Failed cells | State |','|---|---|---:|---:|---:|---:|---|']
    for r in results:md.append(f"| {r['profile']} | {r['suite']} | {r['scenarios']} | {r['coverage']:.1%} | {r['observed_witness_pass_rate']:.1%} | {r['failed_cells']} | {r['state']} |")
    md+=['','The happy-only suites score perfectly on observed witnesses while leaving 11 of 12 required cells untested. These outcomes demonstrate the gate on authored fixtures, not statistical reliability or superiority over a frontier model.','',
         'Execution times are local wall-clock observations, not service latency measurements. Digests bind code inputs and evidence; they do not authenticate the evaluator.','',f"Python {payload['python']}. Command: `python scripts/benchmark.py`. Source hashes: `summary.json`."]
    (args.output/'README.md').write_text('\n'.join(md)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
