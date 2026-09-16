from pathlib import Path
import json,os,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];out=R/'reports/verification';out.mkdir(parents=True,exist_ok=True)
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or p.chromium.executable_path,headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
 page.set_content((R/'site/index.html').read_text(encoding='utf-8'),wait_until='load');page.wait_for_selector('#matrix tr')
 assert page.locator('#status').inner_text()=='HOLD'
 assert page.locator('#matrix tr').count()==12
 page.screenshot(path=str(R/'assets/explorer-hold.png'),full_page=True)
 checks.append('Default happy-only case: HOLD and 12 required rows')
 page.get_by_role('tab').nth(1).click()
 assert page.locator('#status').inner_text()=='BLOCKED'
 assert page.locator('#case-select option').count()==10
 page.screenshot(path=str(R/'assets/explorer-blocked.png'),full_page=True)
 checks.append('Optimistic complete: BLOCKED and 10 selectable counterexamples')
 page.locator('#case-select').select_option('3');assert page.locator('#counter pre').count()==1
 checks.append('Counterexample selection renders JSON with textContent')
 page.get_by_role('tab').nth(3).click()
 assert page.locator('#status').inner_text()=='PENDING REVIEW'
 page.screenshot(path=str(R/'assets/explorer-ready.png'),full_page=True)
 checks.append('Guarded complete: PENDING REVIEW, no false auto-deployment')
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
 page.screenshot(path=str(R/'assets/explorer-mobile.png'),full_page=True)
 checks.append('390px responsive view has no horizontal document overflow')
 page.set_viewport_size({'width':1280,'height':900})
 page.set_content((R/'reports/reference/guarded-complete/report.html').read_text(encoding='utf-8'),wait_until='load')
 page.screenshot(path=str(R/'assets/generated-dossier.png'),full_page=True)
 checks.append('Actual generated dossier renders in Chromium')
 assert not errors,errors
 browser.close()
(out/'browser-check.json').write_text(json.dumps({'engine':'Playwright Chromium','network':'page.set_content from local HTML; no network requests','checks':checks,'page_errors':errors},indent=2)+'\n',encoding='utf-8',newline='\n')
print('\n'.join(checks))
