"""Non-actuating migration checks: imports and registered hardware interfaces only."""
import importlib
from importlib.metadata import version
from pathlib import Path
import subprocess,json
results={}
for name in ['pyfurby','board','digitalio','pwmio','gpiod','mpu6050','pyttsx3','pyaudio','pandas','speech_recognition','ipykernel','zmq']:
 try:importlib.import_module(name);results[name]='OK'
 except Exception as error:results[name]=type(error).__name__+': '+str(error)
results['model']=Path('/proc/device-tree/model').read_text().rstrip('\x00')
results['i2c1']=Path('/dev/i2c-1').exists()
for cmd in [['aplay','-l'],['arecord','-l']]:
 p=subprocess.run(cmd,capture_output=True,text=True);results[cmd[0]]=p.stdout.strip() or p.stderr.strip()
print(json.dumps(results,indent=2))
if any(v!='OK' for k,v in results.items() if k in ['pyfurby','board','digitalio','pwmio','gpiod','mpu6050','pyttsx3','pyaudio','pandas','speech_recognition','ipykernel','zmq']):raise SystemExit(1)
