"""Validate local Markdown asset links and well-formed canonical SVGs."""
import re,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parents[1];errors=[]
for page in root.rglob('*.md'):
    if any(p.startswith('.') for p in page.relative_to(root).parts):continue
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',page.read_text(encoding='utf-8')):
        target=link.split('#')[0].split(' "')[0]
        if not target or ':' in target or target.startswith('/'):continue
        if not (page.parent/target).exists():errors.append(f'{page.relative_to(root)}: {target}')
for image in (root/'assets').rglob('*.svg'):ET.parse(image)
if errors:raise SystemExit('\n'.join(errors))
print('Local Markdown links and SVG XML validated.')
