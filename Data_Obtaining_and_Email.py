import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import ssl

# Yeni duyuruların takibi için bir liste
previous_announcements = []

# Web sitesinden duyuruları kontrol eden fonksiyon
def check_announcements():
    global previous_announcements
    url = "https://....../"  # Kendi URL'nizi buraya yazın
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # "duyuru_baslik" sınıfına sahip duyuruları al
    announcements = soup.find_all('div', class_='duyuru_baslik')
    current_announcements = [a.text.strip() for a in announcements]

    # Yeni duyuruları kontrol et
    new_announcements = [
        announcement for announcement in current_announcements
        if announcement not in previous_announcements
    ]

    # Eğer yeni duyuru varsa, e-posta gönder
    if new_announcements:
        send_email(new_announcements)
        previous_announcements = current_announcements

# E-posta gönderen fonksiyon
def send_email(new_announcements):
    sender_email = "@gmail.com"  # Gönderen e-posta adresi
    sender_password = "PASSWORD"      # E-posta adresi şifresi
    recipient_email = "@gmail.com"  # Alıcı e-posta adresi

    subject = "Yeni Duyuru(lar) Var!"
    body = "Yeni duyurular:\n\n" + "\n".join(new_announcements)

    # E-posta oluştur
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    context= ssl.create_default_context()

    # E-postayı gönder
    #try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as server:
        
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("E-posta başarıyla gönderildi.")
    #except Exception as e:
     #   print(f"E-posta gönderilirken hata oluştu: {e}")
if __name__ == "__main__":
    while True:
        check_announcements()
# Programı çalıştıran döngü
