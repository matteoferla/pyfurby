from pathlib import Path
from urllib.request import Request,urlopen
from jupyter_client import KernelManager
import json,time
# Keep the authentication token private; only report endpoint status.
token=Path('/home/matteo/.config/furby/jupyter-token').read_text().strip()
for attempt in range(12):
 try:
  req=Request('http://127.0.0.1:8888/api/status',headers={'Authorization':'token '+token})
  with urlopen(req,timeout=5) as response:print('Authenticated Jupyter API status:',response.status,flush=True)
  break
 except OSError:
  if attempt==11:raise
  time.sleep(3)
km=KernelManager(kernel_name='furby');kc=None
try:
 km.start_kernel();kc=km.client();kc.start_channels();kc.wait_for_ready(timeout=90)
 msg=kc.execute('from pyfurby import Furby\nimport pandas, pyaudio, speech_recognition\nprint("Furby kernel imports passed")')
 while True:
  reply=kc.get_shell_msg(timeout=90)
  if reply.get('parent_header',{}).get('msg_id')==msg:
   assert reply['content']['status']=='ok',reply['content'];break
 print('Real notebook kernel executed Furby, pandas, audio and speech-recognition imports.',flush=True)
finally:
 if kc:kc.stop_channels()
 km.shutdown_kernel(now=True)
