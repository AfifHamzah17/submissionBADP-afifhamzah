import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv('./dashboard/main_data.csv')

# Mengubah kolom 'dteday' menjadi tipe datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Menentukan rentang tanggal minimum dan maksimum
min_date = df['dteday'].min()
max_date = df['dteday'].max()

# Sidebar filter rentang waktu
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Button untuk memilih seluruh data
    select_all_button = st.button('Pilih Semua Data')
    
    # Menampilkan rentang tanggal yang dipilih
    st.write(f"Rentang waktu yang dipilih: {start_date} hingga {end_date}")

# Jika tombol "Pilih Semua Data" ditekan, set filtered_df untuk seluruh data
if select_all_button:
    filtered_df = df
else:
    # Filter data berdasarkan rentang waktu yang dipilih
    filtered_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
                     (df["dteday"] <= pd.to_datetime(end_date))]

# Set title for the Streamlit dashboard
st.title('Bike Sharing Data Analysis')

# Menampilkan seluruh data yang difilter dalam bentuk tabel (scrollable)
st.subheader('Data Awal (Filtered)')
st.dataframe(filtered_df)

# Fitur untuk mengunduh data dalam format CSV
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button(
    label="Unduh Data CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# **Visualisasi pertama: Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda**
st.subheader('Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda')
plt.figure(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df)
plt.title('Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot()

# **Insight pertama:**
# - Jumlah peminjaman sepeda lebih tinggi pada cuaca cerah dibandingkan dengan hari hujan atau berawan.
# - Cuaca cerah mendorong orang untuk lebih sering meminjam sepeda, sementara cuaca buruk dapat mengurangi minat peminjaman sepeda.

# **Visualisasi kedua: Hubungan Durasi Peminjaman dengan Fitur Lainnya**
st.subheader('Durasi Peminjaman Sepeda dan Faktor Lainnya')
sns.pairplot(filtered_df[['cnt', 'temp', 'hum', 'windspeed', 'season']], diag_kind='kde')
plt.suptitle('Hubungan Durasi Peminjaman Sepeda dengan Fitur Lainnya', y=1.02)
st.pyplot()

# **Visualisasi ketiga: Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Musim**
st.subheader('Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Musim')
season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_avg)
plt.title('Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Peminjaman')
st.pyplot()

# **Insight kedua:**
# - Jumlah peminjaman sepeda cenderung lebih tinggi pada musim semi dan panas, dibandingkan dengan musim gugur dan dingin.
# - Cuaca yang lebih hangat mendorong penggunaan sepeda lebih sering.

# **Bagian analisis regresi linier (opsional)**
st.subheader('Model Prediksi Jumlah Peminjaman')
X = filtered_df[['temp', 'hum', 'windspeed', 'season']]
y = filtered_df['cnt']

# Membagi data menjadi training dan testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model regresi linier
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluasi model
st.write(f"Model R^2 pada data test: {model.score(X_test, y_test)}")

# **Kesimpulan**
st.subheader('Kesimpulan')
st.write("""
Berdasarkan analisis yang dilakukan, berikut adalah kesimpulan yang didapat pada analisis:

**1. Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda:**
    Cuaca memainkan peran penting dalam jumlah peminjaman sepeda. Pada hari cerah, jumlah peminjaman lebih tinggi dibandingkan dengan hari hujan atau berawan. Ini menunjukkan bahwa cuaca cerah mendorong orang untuk lebih sering meminjam sepeda.

**2. Faktor yang Mempengaruhi Durasi Peminjaman Sepeda:**
      Beberapa faktor yang mempengaruhi durasi peminjaman sepeda termasuk suhu, kelembapan, dan musim. Durasi peminjaman cenderung lebih lama pada suhu yang lebih rendah dan kelembapan yang moderat.

**3. Model Prediksi Jumlah Peminjaman Sepeda:**
    Model regresi linier yang dibangun menggunakan fitur suhu, kelembapan, kecepatan angin, dan musim menunjukkan bahwa fitur-fitur ini dapat digunakan untuk memprediksi jumlah peminjaman sepeda dengan tingkat akurasi yang cukup baik (R² = 0.5348). Meskipun model ini masih memiliki ruang untuk perbaikan, hasil ini memberikan wawasan yang berguna untuk perencanaan dan pengelolaan sistem penyewaan sepeda.
""")