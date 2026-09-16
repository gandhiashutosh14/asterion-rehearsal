"""Detect changed files in an exported local dossier, without claiming authenticity."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);args=p.parse_args()
root=args.directory.resolve();m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for name,expected in m['files'].items():
    target=(root/name).resolve()
    if target.parent!=root or not target.is_file():raise SystemExit('Invalid manifest path: '+name)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise SystemExit('Digest mismatch: '+name)
print('All dossier file hashes match. This checks integrity, not origin or scientific validity.')
