import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Menentukan tema
sns.set_theme(style="whitegrid")

# Memasukkan tabel
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

# Mengubah tipe data
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season'] = df_day['season'].map(season_mapping)
df_hour['season'] = df_hour['season'].map(season_mapping)

# Mengubah tipe data cuaca
weather_mapping = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Snow/Rain'}
df_day['weathersit'] = df_day['weathersit'].map(weather_mapping)
df_hour['weathersit'] = df_hour['weathersit'].map(weather_mapping)

# Membuat judul
st.title('Bike Sharing Data Visualizations')

# Membuat pesan singkat
st.write("""
Tugas Akhir dari Dicoding ini memvisualisasikan data peminjaman sepeda 
menggunakan dataset **Bike Sharing**.
""")

# Menampilkan Visualisasi Sepeda Berdasarkan Jam dan Musim
st.subheader('Penggunaan Sepeda Berdasarkan Jam dan Musim')
plt.figure(figsize=(14,6))
sns.lineplot(x='hr', y='cnt', hue='season', data=df_hour)
plt.title('Penggunaan Sepeda Berdasarkan Jam dan Musim')
plt.xlabel('Jam')
plt.ylabel('Jumlah Peminjaman Sepeda (cnt)')
st.pyplot(plt)
plt.close()

# Menampilkan Visualisasi Peminjaman Sepeda Berdasarkan Total Peminjaman dari Waktu ke Waktu
st.subheader('Penggunaan Sepeda Sepanjang Waktu')
plt.figure(figsize=(14, 6))
sns.lineplot(data=df_day, x='dteday', y='cnt')
plt.title('Penggunaan Sepeda Sepanjang Waktu')
plt.xlabel('Tahun')
plt.ylabel('Total Rental Sepeda')
st.pyplot(plt)
plt.close()

# Menampilkan Visualisasi Sepeda Berdasarkan Cuaca
st.subheader('Penggunaan Sepeda Berdasarkan Cuaca')
weather_counts = df_day.groupby('weathersit')['cnt'].sum().reset_index()
weather_counts['cnt'] = weather_counts['cnt'] / 1000
plt.figure(figsize=(14,6))
sns.barplot(x='weathersit', y='cnt', data=weather_counts, palette='Set2')
plt.title('Penggunaan Sepeda Berdasarkan Cuaca', fontsize=16, weight='bold')
plt.xlabel('Situasi Cuaca', fontsize=12)
plt.ylabel('Jumlah Peminjaman Sepeda (cnt/1000)', fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
st.pyplot(plt)
plt.close()
