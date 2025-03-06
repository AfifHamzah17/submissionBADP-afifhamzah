import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv('main_data.csv')

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

# Visualisasi pertama: Cuaca vs Jumlah Peminjaman Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda')
plt.figure(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df)
plt.title('Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Peminjaman Sepeda')
st.pyplot()

# Visualisasi kedua: Hubungan Durasi Peminjaman dengan Fitur Lainnya
st.subheader('Durasi Peminjaman Sepeda dan Faktor Lainnya')
sns.pairplot(filtered_df[['cnt', 'temp', 'hum', 'windspeed', 'season']], diag_kind='kde')
plt.suptitle('Hubungan Durasi Peminjaman Sepeda dengan Fitur Lainnya', y=1.02)
st.pyplot()

# Bagian analisis regresi linier (opsional)
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

# Kesimpulan
st.subheader('Kesimpulan')
st.write("""
Dari visualisasi dan analisis, dapat disimpulkan bahwa cuaca memiliki pengaruh yang signifikan terhadap jumlah peminjaman sepeda. 
Pada cuaca yang cerah, jumlah peminjaman lebih tinggi dibandingkan dengan hari hujan atau berawan.

Faktor-faktor seperti suhu dan kelembapan mempengaruhi durasi peminjaman sepeda, 
dengan peminjaman yang lebih lama cenderung terjadi pada suhu yang lebih rendah dan kelembapan yang moderat.
""")
