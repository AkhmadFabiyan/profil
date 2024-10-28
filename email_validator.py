import requests
from bs4 import BeautifulSoup

def is_email_available(email):
    session = requests.Session()
    login_url = "https://accounts.google.com/ServiceLogin"
    
    # Memuat halaman login Google
    response = session.get(login_url)
    
    # Membuat payload untuk pengecekan email
    payload = {
        'identifier': email,
        'continue': "https://www.google.com",
        'flowName': "GlifWebSignIn",
        'flowEntry': "ServiceLogin"
    }

    # Kirim permintaan POST untuk cek ketersediaan email
    response = session.post(login_url, data=payload)
    
    # Periksa respons
    if "Couldn't find your Google Account" in response.text:
        return True  # Email tersedia
    else:
        return False  # Email tidak tersedia
