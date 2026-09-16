from pathlib import Path
from html import escape
import textwrap,math,json
import cairosvg
from PIL import ImageFont
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def wrap_pixels(text,width,size):
 font=ImageFont.truetype(FONT,size);out=[];line=""
 for word in text.split():
  candidate=(line+" "+word).strip()
  if font.getlength(candidate)>width and line:out.append(line);line=word
  else:line=candidate
 if line:out.append(line)
 return out
R=Path(__file__).resolve().parents[1];A=R/'assets';A.mkdir(exist_ok=True)
BG='#080f20'; PANEL='#111e33'; BORDER='#29405e'; INK='#edf4ff'; MUTED='#9cacc4'; TEAL='#65e3c5'; GOLD='#f1c87d'; VIOLET='#b0a4ff'; RED='#ff94a6'
class Plate:
 def __init__(self,number,title,sub,w=1800,h=1160):
  self.w=w;self.h=h
  self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><desc>{escape(sub)}</desc>', '<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1a2c46" stroke-width="0.6" opacity="0.5"/></pattern><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#7e9abc"/></marker></defs>',f'<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#grid)"/>']
  self.text(64,52,'ASTERION   /   SYSTEM ATLAS',16,TEAL,600,spacing=3)
  self.text(w-210,52,f'{number:02d}   /   08',16,MUTED,500,spacing=2)
  self.text(64,114,title,44,INK,650)
  self.text(64,157,sub,18,MUTED)
  self.a.append(f'<path d="M64 182H{w-64}" stroke="{BORDER}"/>')
 def text(self,x,y,t,size=18,color=INK,weight=400,spacing=0):
  self.a.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Inter,DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(str(t))}</text>')
 def box(self,x,y,w,h,title,lines,tag='',accent=TEAL,dashed=False):
  dash=' stroke-dasharray="8 6"' if dashed else ''
  self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{PANEL}" stroke="{BORDER}"{dash}/><rect x="{x}" y="{y+20}" width="4" height="{h-40}" rx="2" fill="{accent}"/>')
  yy=y+28
  if tag:self.text(x+23,yy,tag,12,accent,600,spacing=1.5);yy+=30
  title_size=22
  while ImageFont.truetype(FONT,title_size).getlength(title)>w-48 and title_size>16:title_size-=1
  self.text(x+23,yy,title,title_size,INK,650);yy+=30
  for size in range(16,12,-1):
   wrapped=[t for ln in lines for t in wrap_pixels(ln,w-48,size)]
   line_height=size+6
   if yy+(len(wrapped)-1)*line_height <= y+h-15:break
  if yy+(len(wrapped)-1)*line_height>y+h-12: print("OVERFLOW",title,len(wrapped),h)
  for line in wrapped:
   self.text(x+23,yy,line,size,MUTED);yy+=line_height
 def line(self,x1,y1,x2,y2,label='',dashed=False):
  dash=' stroke-dasharray="7 6"' if dashed else ''
  self.a.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#7e9abc" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
  if label:self.text((x1+x2)/2+8,(y1+y2)/2-10,label,13,MUTED)
 def path(self,d):self.a.append(f'<path d="{d}" fill="none" stroke="#7e9abc" stroke-width="2" marker-end="url(#arrow)"/>')
 def band(self,x,y,w,h,title):
  self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="none" stroke="{BORDER}" stroke-dasharray="8 7"/>');self.text(x+18,y+28,title,13,VIOLET,600,1)
 def footer(self,t):
  self.a.append(f'<path d="M64 {self.h-68}H{self.w-64}" stroke="{BORDER}"/>');self.text(64,self.h-36,t,14,MUTED);self.text(self.w-325,self.h-36,'DESIGN + EVIDENCE / v0.1',13,TEAL,500)
 def save(self,name):
  self.a.append('</svg>');s=''.join(self.a);(A/f'{name}.svg').write_text(s,encoding='utf-8',newline='\n')
  cairosvg.svg2png(bytestring=s.encode(),write_to=str(A/f'{name}.png'))
# 1
p=Plate(1,'The deployment rehearsal control plane.','Customer intent → typed obligations → bounded scenarios → evidence-linked human handoff.',h=1220)
p.band(64,215,1672,210,'01  /  CUSTOMER INTERFACE — LOCAL API IMPLEMENTED; ENTERPRISE IDENTITY IS A TARGET')
p.box(86,262,380,138,'Customer acceptance contract',['9 owned obligations • 12 required cells','Versioned synthetic YAML, not prose guesses'],tag='INTENT',accent=GOLD)
p.box(535,262,720,138,'FastAPI admission + execution ledger',['Mapped bearer principal → tenant namespace → idempotency key','One synchronous local worker; no distributed queue is claimed'],tag='CONTROL SURFACE')
p.box(1325,262,390,138,'Human reviewer',['Digest-bound approve or reject','No application deployment endpoint'],tag='AUTHORITY',accent=GOLD)
p.line(466,331,535,331);p.line(1255,331,1325,331)
p.band(64,460,1672,458,'02  /  EXECUTION + EVIDENCE — SHARED NODES; OPTIONAL NATIVE LANGGRAPH WIRING')
xs=[86,505,925,1345]
for x,title,lines,tag,acc in [
 (86,'Integration Cartographer',['Declares synthetic CRM / ERP','Records environment context'],'DISCOVER',TEAL),
 (505,'Scenario Architect',['Deterministic catalog planning','Optional Bedrock ID proposal'],'PROPOSE',VIOLET),
 (925,'Rehearsal Fabric',['Scripted target sees inputs only','Fixture effects remain in-process'],'EXECUTE',TEAL),
 (1345,'Independent verifier',['Curated expected outcomes','No oracle reaches target policy'],'CHECK',GOLD)]:p.box(x,512,370,163,title,lines,tag,acc)
for a,b in [(456,505),(875,925),(1295,1345)]:p.line(a,594,b,594)
p.box(86,723,510,155,'Witness-Coverage Gate',['Required obligation × operational slice','Unknown is HOLD; critical failure is BLOCKED'],'WCG / CORE MECHANISM',TEAL)
p.box(650,723,505,155,'Handoff Seal',['Hashes contract, request, observations + witnesses','Review recomputes evidence before state transition'],'CONTENT INTEGRITY',GOLD)
p.box(1210,723,505,155,'Acceptance capsule',['JSON + HTML + Markdown + event journal','Manifest is integrity evidence, not a signature'],'EXPORT',TEAL)
p.path('M1530 675V696H340V723');p.line(596,800,650,800);p.line(1155,800,1210,800)
p.line(1518,400,1518,460,'review')
p.box(86,960,510,145,'SQLite evidence ledger',['Idempotent admission • serialized review','Same-host persistence, not fleet-scale storage'],'IMPLEMENTED')
p.box(650,960,505,145,'Native LangGraph checkpointer',['StateGraph + SQLite saver + interrupt / resume','Optional integration; verify separately'],'OPTIONAL',VIOLET,True)
p.box(1210,960,505,145,'AWS / Azure reference topology',['Private workers, managed identities, queue, store','Cloud target; not deployed by this repository'],'DESIGN TARGET',GOLD,True)
p.footer('Solid: local implementation. Purple/dashed: optional integration. Gold/dashed: reference architecture, not a deployed service.')
p.save('01-system-atlas')
# 2
p=Plate(2,'Bounded autonomy. Explicit authority.','The same domain nodes support a no-key reference runner and a native LangGraph state machine.')
for x,title,tag in [(80,'Intake','VALIDATE'),(430,'Discover','CONTEXT'),(780,'Plan','SELECT'),(1130,'Rehearse','EXECUTE')]:
 p.box(x,270,295,150,title,{'Intake':['Strict input schemas','Contract + catalog digest'],'Discover':['Synthetic environment','No live discovery call'],'Plan':['Whitelist catalog IDs','At most 4 per batch'],'Rehearse':['Input-only target access','Separate curated oracle']}[title],tag)
for a,b in [(375,430),(725,780),(1075,1130)]:p.line(a,344,b,344)
p.box(1130,525,295,155,'Evaluate',['Reject stale witnesses','Update cell coverage'],'VERIFY',GOLD)
p.line(1275,420,1275,525)
p.path('M1130 590H925V420');p.text(675,483,'More eligible cases + remaining budget',15,VIOLET)
p.box(740,525,295,155,'Seal evidence',['Terminal dossier digest','Pending / hold / blocked'],'BIND')
p.line(1130,630,1035,630)
p.box(80,525,570,155,'Hard termination conditions',['max_cases ≤ 64 • max_rounds ≤ 8','No new permitted IDs → stop; no infinite repair loop'],'BOUNDS',GOLD)
p.box(740,815,295,165,'Human interrupt',['Exact digest approval','No side effects before interrupt'],'OPTIONAL LANGGRAPH',VIOLET,True)
p.line(887,680,887,815,'complete + passing')
p.box(1130,815,570,165,'Approve / reject capsule',['A reviewer changes the rehearsal status only','Stored event journal is replayed; not live token streaming'],'FINAL AUTHORITY',GOLD)
p.line(1035,895,1130,895)
p.box(80,815,570,165,'HOLD / BLOCKED',['Missing cells or failures stay visible','No approval route for an incomplete dossier'],'SAFE STOP',RED)
p.path('M740 615H692V790H365V815')
p.footer('LangGraph interrupt nodes restart on resume. The review node performs no external effects before interrupt().')
p.save('02-runtime-statechart')
# 3
p=Plate(3,'The Witness-Coverage Gate.','A 100% score over observed examples says nothing about the required situations you did not test.')
p.box(64,225,520,185,'Required cells',['R = {(obligation, operational slice)}','Coverage = observed required cells / |R|','Coverage measures scope, not probability.'],'CONTRACT',GOLD)
p.box(64,447,520,205,'Compatible witness',['Binds run + contract + scenario + target version','Independent expected checks vs observed fields','Duplicate witness IDs cannot inflate coverage.'],'EVIDENCE',TEAL)
p.box(64,692,520,200,'Gate precedence',['Critical failure / invalid witness → BLOCKED','Missing or advisory failure → HOLD','All covered and passing → READY_FOR_REVIEW'],'DECISION',VIOLET)
p.band(630,225,1106,667,'MEASURED SYNTHETIC CASE STUDY / REFERENCE ENGINE / NO LLM CALLS')
headers=['TARGET / SUITE','CASES','COVERAGE','PASS RATE','STATE'];col=[660,1040,1160,1355,1510]
for x,t in zip(col,headers):p.text(x,310,t,13,MUTED,600,1)
rows=[('Optimistic / happy-only','2','1 / 12','100%','HOLD'),('Optimistic / complete','13','12 / 12','23.1%','BLOCKED'),('Guarded / happy-only','2','1 / 12','100%','HOLD'),('Guarded / complete','13','12 / 12','100%','REVIEW')]
for i,row in enumerate(rows):
 y=379+i*85
 p.a.append(f'<path d="M652 {y+28}H1710" stroke="{BORDER}"/>')
 for j,(x,t) in enumerate(zip(col,row)):p.text(x,y,t,18,GOLD if j==4 and t=='HOLD' else RED if t=='BLOCKED' else TEAL if j==4 else INK,600 if j==4 else 400)
p.text(660,770,'The optimistic policy fails 10 required cells in the full suite.',20,INK,600)
p.text(660,811,'The happy-only baseline misses them by never visiting those cells.',17,MUTED)
p.text(660,849,'All outcomes are generated by scripted policies over authored synthetic fixtures.',15,MUTED)
p.box(64,935,1672,113,'What is not claimed',['No statistical reliability bound, certified safety case, novel theorem, or production readiness guarantee.'],'SCOPE',GOLD)
p.footer('Results: reports/reference/summary.json. “Pass rate” means passing witnesses / observed witnesses; not assertion-level accuracy.')
p.save('03-witness-gate')
# 4
p=Plate(4,'AWS reference deployment.','Architecture target for a customer-isolated service. Only the repository foundation is supplied as Terraform.',h=1270)
p.box(64,230,410,170,'Developer trust boundary',['GitHub protected rehearsal environment','OIDC subject: exact repository + environment','Manual image publish, never auto-rollout'],'BUILD PLANE',VIOLET)
p.box(555,230,480,170,'ECR + encryption foundation',['Immutable image tags • scan-on-push','S3 private evidence bucket + KMS rotation','Terraform source supplied; not applied'],'IAC SOURCE',GOLD,True)
p.box(1115,230,620,170,'CloudWatch + scoped IAM',['Image publisher can push to one ECR repository','No ECS rollout, customer data, or Bedrock rights','Existing account OIDC provider is an input'],'IAC SOURCE',GOLD,True)
p.line(474,315,555,315);p.line(1035,315,1115,315)
p.band(64,440,1672,660,'CUSTOMER AWS ACCOUNT / PRIVATE APPLICATION NETWORK — TARGET ONLY')
p.box(90,494,455,160,'SSO + private ingress',['Customer IdP → validated application principal','Internal ALB / VPN / enterprise ingress','TLS, rate limits and authentication middleware'],'ACCESS TARGET',GOLD,True)
p.box(605,494,500,160,'ECS service + job admission',['Stateless API • per-customer queue','Reject oversize jobs; return asynchronous run ID','Not the current SQLite synchronous API'],'CONTROL TARGET',GOLD,True)
p.box(1170,494,540,160,'Isolated rehearsal workers',['LangGraph orchestration + sandbox fixtures','Task IAM role distinct from execution role','No production-write connector by default'],'EXECUTION TARGET',GOLD,True)
p.line(545,580,605,580);p.line(1105,580,1170,580)
p.box(90,714,455,160,'Aurora PostgreSQL',['Authoritative run + review transactions','Worker lease, outbox, row-level tenant policy','Replace SQLite before multi-replica service'],'STATE TARGET',GOLD,True)
p.box(605,714,500,160,'S3 evidence / KMS',['Content manifest + retention policy','Per-customer access; optional signed attestations','Current code exports local files only'],'EVIDENCE TARGET',GOLD,True)
p.box(1170,714,540,160,'Bedrock private model access',['Selected model / profile supplied by operator','Only objective + scenario metadata in prompt','Optional Boto3 adapter exists; live call untested'],'MODEL BOUNDARY',VIOLET,True)
p.line(1440,654,1440,714);p.line(855,654,855,714);p.path('M705 654V685H315V714')
p.box(90,927,1620,127,'Operational acceptance before a customer pilot',['Queue leasing and recovery • verified tenancy • secrets resolution • model budget • restore drill • incident owner','Network egress policy and VPC endpoints must be designed together; this diagram is not a one-command deployment.'],'UNIMPLEMENTED RELEASE GATES',RED,True)
p.footer('Do not deploy the single-host SQLite demo as this topology. Cloud resources and paid inference require separate operator approval.')
p.save('04-aws-reference')
# 5
p=Plate(5,'Azure reference deployment.','Equivalent responsibilities, not a claim of interchangeable clouds or an implemented Azure adapter.',h=1190)
p.box(64,225,480,165,'Identity + access',['Entra ID validates customer users','Managed identity represents the workload','Application still enforces tenant authorization'],'TRUST TARGET',GOLD,True)
p.box(640,225,500,165,'Container delivery',['GitHub federated credentials → ACR','Container Apps with private environment','Protected promotion gates and image digests'],'DELIVERY TARGET',GOLD,True)
p.box(1230,225,505,165,'Operational ownership',['Azure Monitor / Application Insights','OpenTelemetry export with data minimization','Owner, incident contact and restore checklist'],'OPERATIONS TARGET',GOLD,True)
p.line(544,307,640,307);p.line(1140,307,1230,307)
p.band(64,435,1672,565,'PRIVATE CUSTOMER ENVIRONMENT / TARGET ARCHITECTURE / NO AZURE IAC OR SDK ADAPTER SHIPPED')
p.box(90,490,470,165,'API + admission',['Container Apps API / private ingress','Service Bus work queue and dead-letter path','Replace synchronous local admission'],'CONTROL TARGET',GOLD,True)
p.box(665,490,470,165,'Rehearsal execution',['Dedicated worker identity per boundary','Same typed contracts and witness schema','No customer operations from a planner prompt'],'EXECUTION TARGET',GOLD,True)
p.box(1240,490,470,165,'Model gateway',['Azure AI Foundry endpoint','Managed identity, region + budget policy','Adapter intentionally not implemented'],'OPTIONAL FUTURE',VIOLET,True)
p.line(560,572,665,572);p.line(1135,572,1240,572)
p.box(90,725,470,170,'PostgreSQL Flexible Server',['Run ledger and human review transaction','Versioned migration and backup policy','Tenant isolation requires dedicated validation'],'STATE TARGET',GOLD,True)
p.box(665,725,470,170,'Blob evidence vault',['Private endpoints + customer retention rules','Content manifests with access controls','Do not confuse blob immutability with truth'],'EVIDENCE TARGET',GOLD,True)
p.box(1240,725,470,170,'Key Vault + network policy',['Workload identity, no keys in prompts','Private access + least-privilege RBAC','Egress allowlists and credential rotation'],'SECRET TARGET',GOLD,True)
p.line(320,655,320,725);p.line(900,655,900,725);p.line(1475,655,1475,725)
p.text(90,1050,'Portability seam: domain contracts + observations + witness verification, not provider-specific infrastructure.',20,INK,600)
p.footer('Cloud mapping supports an architecture discussion. This repository makes no Azure deployment or compliance claim.')
p.save('05-azure-reference')
#6
p=Plate(6,'Trust the boundary, not the adjective.','Every planner suggestion and evidence object crosses a concrete validation boundary.',h=1160)
p.band(64,225,500,718,'UNTRUSTED / LIMITED AUTHORITY')
p.box(88,284,450,160,'Client request',['Bearer token resolves tenant server-side','Cannot choose another tenant in run JSON','Idempotency key binds exact request'],'API BOUNDARY',TEAL)
p.box(88,484,450,168,'Optional model proposal',['Only catalog IDs, never executable code','No expected outcomes or raw notes sent','Unknown IDs dropped; case budget enforced'],'MODEL BOUNDARY',VIOLET,True)
p.box(88,690,450,195,'Scripted target policy',['Receives CaseInput, never Scenario.expected','Untrusted note remains fixture data','No model prompt-injection resistance measured'],'TARGET BOUNDARY',TEAL)
p.band(650,225,590,718,'TRUSTED EVALUATION CORE')
p.box(677,284,535,160,'Contract + curated oracle',['Human-authored constraints and golden outcomes','Immutable-by-convention for one rehearsal','Wrong oracle can still produce a wrong verdict'],'TRUST ROOT',GOLD)
p.box(677,484,535,168,'Witness validation',['Contract / scenario / target / run bindings','Expected field checks + witness coherence','Unbound or invalid evidence blocks handoff'],'REFERENCE MONITOR',TEAL)
p.box(677,690,535,195,'Review transaction',['Recompute dossier digest before approval','Reviewer principal required at API boundary','Local CLI trusts the operating-system user'],'HUMAN AUTHORITY',GOLD)
p.line(538,360,677,360);p.line(538,568,677,568);p.path('M538 790H604V610H677')
p.box(1320,284,415,250,'Exports are not proof',['JSON / HTML / journal + hashes','Same-host SHA-256 integrity','No evaluator attestation','No cryptographic signatures','No immutable external audit log'],'EVIDENCE LIMIT',GOLD)
p.box(1320,614,415,271,'Production hardening gap',['SSO / tenant DB policy','Asynchronous admission','Process and network sandbox','Signed source + binary identity','Restore and crash recovery drill'],'DESIGN TARGET',RED,True)
p.line(1212,775,1320,775)
p.text(82,1013,'A hostile evaluator can fabricate internally consistent observations. Hashing does not eliminate that trust assumption.',19,INK,600)
p.footer('No PHI, real customer records, cloud credentials, live financial actions, or production connectors are included.')
p.save('06-trust-boundaries')
#7
p=Plate(7,'The forward-deployed engineering loop.','Connect customer ambiguity, implementation trade-offs and operational ownership through inspectable evidence.',h=1160)
cols=[64,350,635,920,1205,1490]
stages=[('01','Discover',['Map decision + user','Name failure cost'],['Problem brief','Stakeholder map']),('02','Contract',['Define obligations','Assign owners'],['Acceptance workbook','Required slice matrix']),('03','Integrate',['Declare dependencies','Isolate synthetic twin'],['Data flow inventory','Boundary / threat model']),('04','Rehearse',['Exercise failures','Capture counterexamples'],['Witness report','Failure taxonomy']),('05','Review',['Bind exact evidence','Resolve go / no-go'],['Decision record','Handoff capsule']),('06','Operate',['Name the responder','Feed gaps into next run'],['Runbook + RACI','Pilot exit checklist'])]
for x,(n,title,lines,outs) in zip(cols,stages):
 p.box(x,290,245,235,title,lines,'PHASE '+n,TEAL)
 p.box(x,595,245,210,'Deliverables',outs,'IN REPOSITORY',GOLD)
 p.line(x+122,525,x+122,595)
for a,b in zip(cols,cols[1:]):p.line(a+245,395,b,395)
p.band(64,857,1672,179,'STAFF-LEVEL DESIGN JUDGMENT')
p.text(90,922,'Prefer one falsifiable acceptance claim over ten unverified platform promises.',26,INK,600)
p.text(90,968,'ADR decisions: bounded planning • oracle separation • local-first evidence • explicit cloud boundary • independent approval.',17,MUTED)
p.footer('Synthetic engagement kit: docs/fde/. No real customer endorsement, adoption, revenue impact or production outcome is implied.')
p.save('07-fde-delivery-loop')
#8
p=Plate(8,'The evidence model.','Bind observations to the requirement they discharge, then bind approval to the complete evidence set.',h=1170)
p.box(64,245,480,185,'Contract',['id • version • objective • classification','Obligation[]: id, owner, critical, required_slices','Canonical JSON → contract digest'],'CUSTOMER ACCEPTANCE',GOLD)
p.box(660,245,480,185,'Scenario',['id • operational slice • CaseInput','expected[obligation_id] = curated field checks','Scenario digest binds inputs + golden checks'],'CURATED REHEARSAL',TEAL)
p.box(1260,245,475,185,'Observation',['decision • owner • source count • effects','cross-tenant flag • modeled deadline • trace','Produced by input-only ScriptedTarget'],'TARGET OUTPUT',TEAL)
p.line(544,337,660,337);p.line(1140,337,1260,337,'inputs only')
p.box(64,542,480,205,'Run',['run_id • request • target_version • rounds','selected IDs • witnesses • observations • events','Tenant binding stays in the local ledger'],'EXECUTION RECORD',TEAL)
p.box(660,542,480,205,'Witness',['run / contract / scenario / target bindings','obligation_id • slice • expected • observed','passed • mismatch fields • content digest'],'VERIFIABLE SHAPE',VIOLET)
p.box(1260,542,475,205,'Assessment',['Cell state: PASS / FAIL / MISSING','Coverage • observed witness pass rate','Counterexamples • missing cells • invalid count'],'DETERMINISTIC GATE',GOLD)
p.line(895,430,895,542);p.path('M1495 430V488H1140V615');p.line(544,645,660,645);p.line(1140,645,1260,645)
p.box(64,856,800,170,'Review',['approve / reject • rationale • expected evidence_digest • actor','Serial transaction checks pending state + recomputed digest','No modification of the contract or witnesses during approval'],'DIGEST-BOUND HUMAN DECISION',GOLD)
p.box(955,856,780,170,'Portable handoff capsule',['report.json + report.html + report.md + events.jsonl + manifest.json','File hashes detect edits; they do not prove who executed the test','Source manifest in benchmark summary identifies evaluated source files'],'LOCAL ARTIFACT',TEAL)
p.path('M1495 747V797H455V856');p.line(864,941,955,941)
p.footer('The trusted evaluator and authored oracle remain assumptions. Production source attestation and signed approval are future work.')
p.save('08-evidence-model')
# Branded hero, exact editable vector; separate image-generation concept asset can accompany it.
p=Plate(1,'ASTERION','Evidence-linked deployment rehearsals for enterprise agents.',w=1800,h=720)
p.box(64,247,970,215,'Ship the evidence. Not just the demo.',['Customer acceptance contracts become bounded failure-mode rehearsals,','then a reviewable, digest-bound handoff capsule.'],'FORWARD-DEPLOYED ENGINEERING',TEAL)
# Concentric original labyrinth motif.
for i in range(7):
 r=145-i*17; x=1400;y=348
 p.a.append(f'<path d="M{x-r} {y+r}V{y-r}H{x+r}V{y+r-22}H{x-r+22}V{y-r+22}" fill="none" stroke="{TEAL if i%2==0 else VIOLET}" stroke-width="4" opacity="{0.8-i*0.07}"/>')
p.text(66,534,'WITNESS-COVERAGE GATE',15,GOLD,600,2)
p.text(66,578,'LANGGRAPH  /  FASTAPI  /  SYNTHETIC DIGITAL TWIN  /  AWS + AZURE DESIGN',18,MUTED,500)
p.footer('Runnable local prototype + engineering atlas. Cloud topology is a reference design, not a deployed service.')
p.save('hero')
print('Rendered',len(list(A.glob('*.svg'))),'SVG + PNG asset pairs')
