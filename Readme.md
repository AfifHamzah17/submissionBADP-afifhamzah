# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek
Ini adalah analisis data terkait dengan dataset Bike Sharing. Tujuan utama dari proyek ini adalah untuk menjawab beberapa pertanyaan bisnis terkait dengan pengaruh cuaca terhadap jumlah peminjaman sepeda dan faktor-faktor yang mempengaruhi durasi peminjaman sepeda. Proyek ini dilengkapi dengan dashboard interaktif menggunakan Streamlit.

## Fitur
- **Visualisasi**: Menampilkan pengaruh cuaca terhadap jumlah peminjaman sepeda dan hubungan durasi peminjaman dengan fitur lainnya.
- **Model Prediksi**: Menggunakan regresi linier untuk memprediksi jumlah peminjaman sepeda berdasarkan beberapa fitur.
- **Filter Data**: Pengguna dapat memfilter data berdasarkan rentang waktu dengan menggunakan fitur kalender di sidebar.
- **Unduh Data**: Pengguna dapat mengunduh data yang difilter dalam format CSV.

## Persyaratan Sistem

Untuk menjalankan proyek ini, Anda perlu menyiapkan lingkungan pengembangan terlebih dahulu.

### Setup Environment - Anaconda
1. Buat environment baru di Anaconda:
   ```bash
	conda create --name main-ds python=3.9
2. Aktifkan environment yang baru dibuat:
   ```bash
	conda activate main-ds
3. Instal dependensi dari requirements.txt:
   ```bash
	pip install -r requirements.txt

### Setup Environment - Shell/Terminal
1. Buat direktori untuk proyek ini:
   ```bash
	mkdir proyek_analisis_data
	cd proyek_analisis_data
2. Instal dependensi menggunakan pipenv:
   ```bash
	pipenv install
	pipenv shell
3. Instal dependensi dari requirements.txt:
   ```bash
	pip install -r requirements.txt

### Menjalankan Aplikasi Streamlit
Setelah semua dependensi terinstal, Anda bisa menjalankan aplikasi Streamlit dengan perintah berikut:
   ```bash
	streamlit run dashboard.py 
## Deskripsi Aplikasi

Aplikasi ini menyediakan antarmuka interaktif menggunakan Streamlit yang memungkinkan pengguna untuk:

- Melihat visualisasi data seperti pengaruh cuaca terhadap jumlah peminjaman sepeda.
- Memilih rentang waktu tertentu untuk memfilter data yang ditampilkan.
- Melihat hasil model prediksi regresi linier yang digunakan untuk memprediksi jumlah peminjaman sepeda.
- Mengunduh data yang sudah difilter dalam format CSV.

## Model Prediksi

Model yang digunakan adalah regresi linier untuk memprediksi jumlah peminjaman sepeda berdasarkan beberapa fitur seperti suhu, kelembapan, dan kecepatan angin.

## Lisensi

Proyek ini dilisensikan di bawah MIT License.

## Kontribusi

Kami menyambut kontribusi dari siapa pun. Jika Anda ingin berkontribusi, silakan buat pull request atau hubungi kami untuk informasi lebih lanjut.