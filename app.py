from flask import Flask, render_template, request, redirect, url_for
import random
import os
import string
from datetime import datetime
import calendar
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Lokasi file data nama
NAMES_FILE = 'data/names.txt'

# Direktori untuk menyimpan profil yang dihasilkan
GENERATED_DIR = 'generated_profiles'

# Membuat direktori jika belum ada
if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)

# Fungsi untuk memuat nama dari file
def load_names():
    with open(NAMES_FILE, 'r') as file:
        names = [line.strip() for line in file.readlines()]
    return names

# Fungsi untuk menghasilkan kode acak unik
def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Fungsi untuk menghasilkan profil
def generate_profile(choice):
    names = load_names()
    
    # Pilih nama depan dan nama belakang secara acak
    first_name = random.choice(names)
    last_name = random.choice([name for name in names if name != first_name])
    
    # Generate email dan password
    random_number = random.randint(10, 99)
    unique_code = generate_random_code()  # Menghasilkan kode acak unik
    email = f"{first_name.lower()}{last_name.lower()}{random_number}@gmail.com"
    password = f"{first_name.lower()}{unique_code}{last_name.lower()}{random_number}"
    
    # Generate tanggal pembuatan akun
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Untuk menghindari masalah dengan Februari
    account_creation_date = datetime(year, month, day).strftime(f'%d {calendar.month_name[month]} %Y')
    
    # Profil yang dihasilkan
    profile = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'account_creation_date': account_creation_date,
        'choice': choice  # Tambahkan pilihan pengguna ke profil
    }
    
    return profile

# Fungsi untuk mengirim email
def send_email(profile, recipient_email):
    # Konfigurasi email (gunakan SMTP Gmail sebagai contoh)
    sender_email = "akhmadfabiyanmail@gmail.com"
    sender_password = "muyl xlus ajdd rixf"
    
    # Mendapatkan tanggal saat ini
    current_date = datetime.now().strftime('%d %B %Y')  # Format tanggal saat ini
    
    # Membuat subjek email dengan menyertakan tanggal
    subject = f"Profil Pengguna yang Dihasilkan pada {current_date}"
    
    # Body email
    body = f"""
    Berikut adalah detail profil yang dihasilkan:
    
    Nama Depan: {profile['first_name']}
    Nama Belakang: {profile['last_name']}
    Email: {profile['email']}
    Kata Sandi: {profile['password']}
    Tanggal Pembuatan Akun: {profile['account_creation_date']}
    Pilihan: {profile['choice']}
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Lampirkan body pesan
    msg.attach(MIMEText(body, 'plain'))
    
    # Konfigurasi server SMTP dan kirim email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route utama
@app.route('/')
def index():
    return render_template('index.html', profile=None)

# Route untuk generate profil
@app.route('/generate', methods=['POST'])
def generate():
    choice = request.form.get('choice')
    profile = generate_profile(choice)
    return render_template('index.html', profile=profile)

# Route untuk menyimpan profil
@app.route('/save', methods=['POST'])
def save():
    profile = request.form.to_dict()

    # Dapatkan tanggal saat ini untuk nama folder
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Buat path untuk sub-direktori berdasarkan tanggal
    dated_dir = os.path.join(GENERATED_DIR, current_date)

    # Pastikan sub-direktori berdasarkan tanggal ada
    if not os.path.exists(dated_dir):
        os.makedirs(dated_dir)

    # Tentukan nama file dan path lengkap
    file_name = f"{profile['first_name']}_{profile['last_name']}.txt"
    file_path = os.path.join(dated_dir, file_name)

    # Simpan profil ke dalam file
    with open(file_path, 'w') as file:
        file.write(f"Nama Depan: {profile['first_name']}\n")
        file.write(f"Nama Belakang: {profile['last_name']}\n")
        file.write(f"Email: {profile['email']}\n")
        file.write(f"Kata Sandi: {profile['password']}\n")
        file.write(f"Tanggal Pembuatan Akun: {profile['account_creation_date']}\n")
        file.write(f"Pilihan: {profile['choice']}\n")  # Simpan pilihan pengguna

    # Kirim email ke alamat yang ditentukan
    recipient_email = "akhmadfabiyanmail@gmail.com"  # Ubah sesuai dengan email penerima
    send_email(profile, recipient_email)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
