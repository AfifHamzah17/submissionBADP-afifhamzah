import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Atur agar tidak muncul warning deprecation
# st.set_option('deprecation.showPyplotGlobalUse', False)

# ========================================================
# Proyek Analisis Data: Bike Sharing Dataset
# Nama: Afif Hamzah  
# Email: a281ybm018@devacademy.id  
# ID Dicoding: afifhamzah17
# ========================================================

st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.markdown("""
**Nama:** Afif Hamzah  
**Email:** a281ybm018@devacademy.id  
**ID Dicoding:** afifhamzah17  

## Menentukan Pertanyaan Bisnis
1. Bagaimana pengaruh cuaca terhadap jumlah peminjaman sepeda dalam dataset Bike Sharing?
2. Apa faktor yang mempengaruhi durasi peminjaman sepeda?
""")

# ========================================================
# Fungsi Memuat Data dari main_data.csv
# ========================================================
@st.cache_data
def load_data():
    # Memuat data dari file main_data.csv (hasil gabungan day_df dan hour_df)
    df = pd.read_csv("main_data.csv", parse_dates=['dteday'])
    # Mapping untuk kolom season dan weathersit agar lebih informatif
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_mapping = {
        1: 'Clear/Few Clouds', 
        2: 'Mist/Cloudy', 
        3: 'Light Rain/Snow', 
        4: 'Heavy Rain/Snow'
    }
    df['season_name'] = df['season'].map(season_mapping)
    df['weather_desc'] = df['weathersit'].map(weather_mapping)
    return df

# Muat data dari main_data.csv
df = load_data()

# ========================================================
# Pisahkan Data menjadi Daily dan Hourly
# ========================================================
# Pada penggabungan, data harian tidak memiliki kolom 'hr' (bernilai NaN)
day_df = df[df['hr'].isna()].copy()
# Data per jam memiliki nilai pada kolom 'hr'
hour_df = df[df['hr'].notna()].copy()

# ========================================================
# Sidebar: Tampilan Data Mentah dan Fitur Interaktif
# ========================================================

# Tampilkan logo di sidebar
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

# Tampilkan data mentah (seluruh data) jika checkbox dicentang
if st.sidebar.checkbox("Tampilkan Data Mentah (Daily)"):
    st.sidebar.subheader("Data Harian (day_df)")
    st.sidebar.dataframe(day_df)  # tampilkan seluruh data (scrollable)

if st.sidebar.checkbox("Tampilkan Data Mentah (Hourly)"):
    st.sidebar.subheader("Data Per Jam (hour_df)")
    st.sidebar.dataframe(hour_df)

# Fitur interaktif: Memilih rentang waktu berdasarkan kolom 'dteday'
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

select_all_button = st.sidebar.button('Pilih Semua Data')

st.sidebar.write(f"Rentang waktu yang dipilih: {start_date} hingga {end_date}")

# ========================================================
# Exploratory Data Analysis (EDA)
# ========================================================
st.header("Exploratory Data Analysis (EDA)")

st.subheader("1. Analisis Univariate: Distribusi Data")
fig_dist, ax_dist = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(day_df['cnt'], kde=True, color='skyblue', ax=ax_dist[0])
ax_dist[0].set_title('Distribusi Peminjaman Sepeda (Harian)')
ax_dist[0].set_xlabel('Jumlah Peminjaman (cnt)')
sns.histplot(hour_df['cnt'], kde=True, color='salmon', ax=ax_dist[1])
ax_dist[1].set_title('Distribusi Peminjaman Sepeda (Per Jam)')
ax_dist[1].set_xlabel('Jumlah Peminjaman (cnt)')
plt.tight_layout()
st.pyplot(fig_dist)

st.subheader("2. Analisis Bivariate: Hubungan Antar Variabel")
st.markdown("**Boxplot jumlah peminjaman berdasarkan kondisi cuaca (weathersit) di data harian**")
fig_box, ax_box = plt.subplots(figsize=(8, 6))
sns.boxplot(x='weathersit', y='cnt', data=day_df, palette='Set3', ax=ax_box)
ax_box.set_title('Boxplot Peminjaman Sepeda per Kondisi Cuaca')
ax_box.set_xlabel('Weathersit (1: Clear/Few Clouds, 2: Mist/Cloudy, 3: Light Rain/Snow, 4: Heavy Rain/Snow)')
ax_box.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_box)

st.markdown("**Scatter Plot hubungan antara suhu (temp) dan jumlah peminjaman di data per jam**")
fig_scatter1, ax_scatter1 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='temp', y='cnt', data=hour_df, alpha=0.5, color='purple', ax=ax_scatter1)
ax_scatter1.set_title('Hubungan Suhu dan Peminjaman Sepeda (Per Jam)')
ax_scatter1.set_xlabel('Suhu (temp)')
ax_scatter1.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_scatter1)

st.markdown("**Scatter Plot hubungan antara suhu yang dirasakan (atemp) dan jumlah peminjaman**")
fig_scatter2, ax_scatter2 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='atemp', y='cnt', data=hour_df, alpha=0.5, color='green', ax=ax_scatter2)
ax_scatter2.set_title('Hubungan Suhu Dirasakan dan Peminjaman Sepeda (Per Jam)')
ax_scatter2.set_xlabel('Suhu Dirasakan (atemp)')
ax_scatter2.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_scatter2)

st.markdown("**Scatter Plot hubungan antara kelembapan (hum) dan jumlah peminjaman di data harian**")
fig_scatter3, ax_scatter3 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='hum', y='cnt', data=day_df, alpha=0.5, color='orange', ax=ax_scatter3)
ax_scatter3.set_title('Hubungan Kelembapan dan Peminjaman Sepeda (Harian)')
ax_scatter3.set_xlabel('Kelembapan (hum)')
ax_scatter3.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_scatter3)

st.subheader("3. Agregasi Data Berdasarkan Kategori")
st.markdown("**Agregasi berdasarkan kondisi cuaca (weathersit)**")
weather_group = day_df.groupby('weathersit')['cnt'].agg(['mean', 'median', 'std']).reset_index()
st.write("---- Agregasi Peminjaman Sepeda Berdasarkan Kondisi Cuaca (weathersit) ----")
st.write(weather_group)

st.markdown("**Agregasi berdasarkan musim**")
season_group = day_df.groupby('season')['cnt'].agg(['mean', 'median', 'std']).reset_index()
st.write("---- Agregasi Peminjaman Sepeda Berdasarkan Musim ----")
st.write(season_group)

st.markdown("**Agregasi berdasarkan hari kerja (workingday)**")
workingday_group = day_df.groupby('workingday')['cnt'].agg(['mean', 'median', 'std']).reset_index()
st.write("---- Agregasi Peminjaman Sepeda Berdasarkan Hari Kerja ----")
st.write(workingday_group)

st.subheader("4. Analisis Korelasi: Heatmap")
fig_heat, ax_heat = plt.subplots(figsize=(10, 8))
corr_matrix = day_df.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax_heat)
ax_heat.set_title('Heatmap Korelasi Variabel (day_df)')
st.pyplot(fig_heat)

st.subheader("5. Boxplot Berdasarkan Musim")
fig_season, ax_season = plt.subplots(figsize=(8, 6))
sns.boxplot(x='season_name', y='cnt', data=day_df, palette='pastel', ax=ax_season)
ax_season.set_title('Boxplot Peminjaman Sepeda per Musim')
ax_season.set_xlabel('Musim')
ax_season.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_season)

# ========================================================
# Visualization & Explanatory Analysis
# ========================================================
st.header("Visualization & Explanatory Analysis")

st.subheader("Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda")
st.markdown("Mapping ulang agar label kondisi cuaca lebih rapi:")
day_df['weather_desc'] = day_df['weathersit'].map({
    1: 'Clear/Few Clouds', 
    2: 'Mist/Cloudy', 
    3: 'Light Rain/Snow', 
    4: 'Heavy Rain/Snow'
})
fig_viz1, ax_viz1 = plt.subplots(figsize=(8, 6))
sns.boxplot(x='weather_desc', y='cnt', data=day_df, palette='Set2', ax=ax_viz1)
ax_viz1.set_title('Boxplot Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
ax_viz1.set_xlabel('Kondisi Cuaca')
ax_viz1.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_viz1)

st.markdown("Barplot rata-rata peminjaman per kondisi cuaca:")
avg_by_weather = day_df.groupby('weather_desc')['cnt'].mean().reset_index()
fig_viz1b, ax_viz1b = plt.subplots(figsize=(8, 6))
sns.barplot(x='weather_desc', y='cnt', data=avg_by_weather, palette='Set2', ax=ax_viz1b)
ax_viz1b.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
ax_viz1b.set_xlabel('Kondisi Cuaca')
ax_viz1b.set_ylabel('Rata-rata Jumlah Peminjaman (cnt)')
st.pyplot(fig_viz1b)

st.subheader("Pertanyaan 2: Faktor yang Mempengaruhi Durasi (Jumlah) Peminjaman Sepeda")
st.markdown("**Scatter plot antara suhu (temp) dan jumlah peminjaman**")
fig_viz2, ax_viz2 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='temp', y='cnt', data=day_df, color='blue', alpha=0.7, ax=ax_viz2)
ax_viz2.set_title('Hubungan antara Suhu (temp) dan Jumlah Peminjaman')
ax_viz2.set_xlabel('Suhu (temp)')
ax_viz2.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_viz2)

st.markdown("**Scatter plot antara kelembapan (hum) dan jumlah peminjaman**")
fig_viz3, ax_viz3 = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='hum', y='cnt', data=day_df, color='red', alpha=0.7, ax=ax_viz3)
ax_viz3.set_title('Hubungan antara Kelembapan (hum) dan Jumlah Peminjaman')
ax_viz3.set_xlabel('Kelembapan (hum)')
ax_viz3.set_ylabel('Jumlah Peminjaman (cnt)')
st.pyplot(fig_viz3)

st.markdown("**Pairplot untuk variabel lingkungan dan jumlah peminjaman**")
fig_pair = sns.pairplot(day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']], diag_kind='kde')
plt.suptitle('Pairplot Variabel Lingkungan dan Jumlah Peminjaman', y=1.02)
st.pyplot(fig_pair)

st.subheader("Analisis Lanjutan (Opsional)")
fig_corr_adv, ax_corr_adv = plt.subplots(figsize=(10, 8))
corr_matrix_adv = day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(corr_matrix_adv, annot=True, cmap='coolwarm', ax=ax_corr_adv)
ax_corr_adv.set_title('Heatmap Korelasi Variabel Lingkungan dan Jumlah Peminjaman')
st.pyplot(fig_corr_adv)

# ========================================================
# Conclusion
# ========================================================
st.header("Conclusion")
st.markdown("""
**Conclusion Pertanyaan 1:**  
Kondisi cuaca memiliki pengaruh yang signifikan terhadap jumlah peminjaman sepeda. Visualisasi boxplot dan barplot menunjukkan bahwa kondisi cuaca yang cerah (Clear/Few Clouds) menghasilkan peminjaman yang lebih tinggi, sedangkan kondisi cuaca yang buruk (Heavy Rain/Snow) menurunkan peminjaman sepeda.

**Conclusion Pertanyaan 2:**  
Faktor lingkungan seperti suhu, suhu yang dirasakan, kelembapan, dan kecepatan angin mempengaruhi jumlah peminjaman sepeda. Suhu yang lebih tinggi berkorelasi positif dengan peminjaman, sementara kelembapan dan kecepatan angin yang tinggi berkorelasi negatif.
""")
