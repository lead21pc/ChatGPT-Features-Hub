import compileall
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
os.chdir(ROOT)
stage=sys.argv[1]
assert stage in ('static','final')
OUT=Path(__file__).resolve().parent
blocked="import socket,unittest,sys; from unittest.mock import patch; p=patch.object(socket.socket,'connect',side_effect=AssertionError('network blocked globally')); p.start(); "
commands={
 'local': [sys.executable,'-X','utf8','-B','-c',blocked+"r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('legacy/tests',pattern='test_*.py')); sys.exit(not r.wasSuccessful())"],
 'upstream_authoring':[sys.executable,'-X','utf8','-B','-c',blocked+"sys.path.insert(0,'legacy/upstream/Central Hub/tests'); r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_authoring_isolation','test_authoring_candidate','test_authoring_m1','test_authoring_m2','test_authoring_m4'])); sys.exit(not r.wasSuccessful())"]}
results={}
for name,cmd in commands.items():
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/f'explicit_{stage}_{name}.txt').write_bytes(r.stdout)
 results[name]={'exit_code':r.returncode,'log':f'explicit_{stage}_{name}.txt'}
 print(name,r.returncode,r.stdout.decode('utf-8')[-250:])
paths=[str(p) for p in ROOT.rglob('*.py') if '.git' not in p.parts and '__pycache__' not in p.parts]
with tempfile.TemporaryDirectory(prefix='m3_compile_') as tmp:
 r=subprocess.run([sys.executable,'-X','utf8','-X',f'pycache_prefix={tmp}','-m','compileall','-q',*paths],capture_output=True)
 results['compileall']={'exit_code':r.returncode,'files':len(paths)}
 print('compileall',r.returncode,len(paths))
r=subprocess.run(['git','diff','--check'],capture_output=True)
results['diff_check']={'exit_code':r.returncode}
preserved=json.loads((OUT/'explicit_preserved_manifest.json').read_text(encoding='utf-8'))
results['experiment_1_preserved']=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in preserved.items())
key=json.loads(Path('config.json').read_text(encoding='utf-8'))['openai_api_key']
results['secret_scan_pass']=not any(key.encode() in p.read_bytes() for p in OUT.rglob('*') if p.is_file())
results['static_pass']=all(v['exit_code']==0 for v in results.values() if isinstance(v,dict)) and results['secret_scan_pass'] and results['experiment_1_preserved']
(OUT/f'explicit_{stage}_checks.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results))
sys.exit(not results['static_pass'])
