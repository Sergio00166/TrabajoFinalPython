from cryptography.fernet import Fernet

encrypted_text = input("PASTE TEXT: ")

cipher_suite = Fernet(b'W3NFJwDhdDLeE48araLk2P_kETmFjPhct-kif7QhgI4=')

# Decrypt the text
try:
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    print("Decrypted text:", decrypted_text.decode('utf-8'))
except Exception as e:
    print("An error occurred:", e)

input()
