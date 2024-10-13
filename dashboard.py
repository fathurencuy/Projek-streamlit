import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menentukan tema
sns.set_theme(style="whitegrid")

# Memasukkan tabel
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Mengubah nama pada kolom-kolom tertentu agar mudah dipahami
day_df.rename(columns={'dteday':'date', 'yr':'year','mnth':'month', 'weekday': 'days','weathersit':'weather_situation','cnt':'count'}, inplace=True)
hour_df.rename(columns={'dteday':'date', 'yr':'year','mnth':'month', 'hr': 'hours','weekday': 'days','weathersit':'weather_situation','cnt':'count'}, inplace=True)

# Ubah kolom date menjadi tipe datetime
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Mengubah Tipe data menjadi string pada kolom 'year', 'month', 'season', dll
column = ['year', 'month', 'season', 'days', 'weather_situation', 'holiday', 'workingday']
day_df[column] = day_df[column].astype(str)
hour_df[column] = hour_df[column].astype(str)

# Mengubah angka dalam data pada kolom menjadi string
month_names = {str(i): month for i, month in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], start=1)}
day_df['month'].replace(month_names, inplace=True)
hour_df['month'].replace(month_names, inplace=True)

season_names = {'1': 'Spring', '2': 'Summer', '3': 'Fall', '4': 'Winter'}
day_df['season'].replace(season_names, inplace=True)
hour_df['season'].replace(season_names, inplace=True)

days_names = {'0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday', '6': 'Saturday'}
day_df['days'].replace(days_names, inplace=True)
hour_df['days'].replace(days_names, inplace=True)

weather_names = {'1': 'Clear', '2': 'Cloudy', '3': 'Rain'}
day_df['weather_situation'].replace(weather_names, inplace=True)
hour_df['weather_situation'].replace(weather_names, inplace=True)



# Membuat pesan singkat
st.write("""
Tugas Akhir dari Dicoding ini memvisualisasikan data peminjaman sepeda 
menggunakan dataset **Bike Sharing**.
""")

# Visualisasi ke-1
season_data = day_df.groupby('season')['count'].sum().reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6)) 

colors_season = sns.color_palette('Set2', n_colors=4)
ax[0].pie(season_data['count'], labels=season_data['season'], autopct='%1.1f%%', colors=colors_season)
ax[0].set_title('Persentase Penggunaan Sepeda Berdasarkan Musim')

ax[1].axis('tight')
ax[1].axis('off')
table_data = ax[1].table(cellText=season_data.values, colLabels=season_data.columns, loc='center')

st.subheader('total penggunaan sepeda berdasarkan musim')
st.pyplot(fig)  

# Visualisasi ke-2
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weather_situation', y='count', data=day_df, ax=ax)

ax.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
ax.set_xlabel('Jenis Cuaca')
ax.set_ylabel('Jumlah Penyewaan Sepeda')

st.subheader('Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
st.pyplot(fig)  

# Visualisasi ke-3
data_2011 = hour_df[hour_df['date'].dt.year == 2011].copy()
data_2012 = hour_df[hour_df['date'].dt.year == 2012].copy()

data_2011['month'] = data_2011['date'].dt.month
data_2012['month'] = data_2012['date'].dt.month

monthly_counts_2011 = data_2011.groupby('month')['count'].sum().reset_index()
monthly_counts_2012 = data_2012.groupby('month')['count'].sum().reset_index()

monthly_counts_2011['year'] = 2011
monthly_counts_2012['year'] = 2012
combined_counts = pd.concat([monthly_counts_2011, monthly_counts_2012], ignore_index=True)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=combined_counts, x='month', y='count', hue='year', marker='o', ax=ax)

ax.set_title('Perbandingan Penggunaan Sepeda  antara Tahun 2011 dan 2012')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(range(12))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.legend(title='Tahun')

st.subheader('Tren penyewaan sepeda setiap bulan')
st.pyplot(fig)  

# Visualisasi ke-4
total_casual = hour_df['casual'].sum()
total_registered = hour_df['registered'].sum()

labels = ['Casual', 'Registered']
sizes = [total_casual, total_registered]
colors = ['#2ca02c', '#1f77b4']
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')
ax.set_title('Proporsi Penyewaan Sepeda: Casual vs Registered')

st.subheader('Perbandingan jumlah penyewaan antara pengguna lama dan pendaftar')
st.pyplot(fig) 

# Menampilkan DataFrame total counts
data = {
    'Type': ['Casual', 'Registered'],
    'Count': [total_casual, total_registered]
}

total_counts_df = pd.DataFrame(data)
st.write(total_counts_df)  
