import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
day_df = pd.read_csv('./data/day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk pemilihan tanggal dan filter lainnya
st.sidebar.title('Filter')

# Filter tanggal di sidebar
start_date = st.sidebar.date_input("Tanggal Mulai", value=day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", value=day_df['dteday'].max())

# Checkbox untuk memilih semua data
all_data = st.sidebar.checkbox('Tampilkan Semua Data')

# Tombol submit
submit = st.sidebar.button('Terapkan Filter')

# Jika "Tampilkan Semua Data" dipilih, tampilkan seluruh data, jika tidak, gunakan filter tanggal
if all_data:
    filtered_df = day_df
else:
    if submit:
        filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
    else:
        filtered_df = day_df

# Judul Dashboard
st.title('Dashboard Penyewaan Sepeda')

# Layout tab untuk analisis berbeda
tab1, tab2, tab3 = st.tabs(["Pengaruh Cuaca", "Perbandingan Hari Kerja vs Akhir Pekan", "Pengaruh Suhu, Kelembapan, dan Kecepatan Angin"])

# Tab 1: Pengaruh Cuaca Terhadap Penyewaan Sepeda
with tab1:
    st.header('Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda')
    
    # Penjelasan
    st.write("""
    Pada grafik ini Menunjukan bahwa langit yang cerah dan sedikit berawan banyak dipilih oleh pelanggan untuk menyewa sepeda. 
    Hal ini menunjukan kecenderungan pada cuaca yang cerah, dan melihat kondisi cuaca berawan dan mendung cenderung masih diminati.
    Pada hujan ringan ataupun salju ringan masih memiliki peminatan terhadap penyewaan sepeda, berbeda dengan hujan lebat atau hujan salju lebat 
    yang sama sekali tidak diminati. Hal ini menjelaskan bahwa ketika cuaca sedang tidak baik akan berdampak pula terhadap layanan bike sharing ini.
    """)
    
    # Mengelompokkan data berdasarkan kondisi cuaca dan menghitung rata-rata penyewaan
    weather_effect = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_labels = {1: 'Cerah', 2: 'Berawan/Mendung', 3: 'Hujan Ringan/Salju Ringan', 4: 'Hujan Lebat/Salju Lebat'}
    weather_effect['weathersit'] = weather_effect['weathersit'].map(weather_labels)
    
    # Plotting
    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='cnt', data=weather_effect, palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

# Tab 2: Perbandingan Penyewaan Sepeda Hari Kerja vs Akhir Pekan
with tab2:
    st.header('Perbedaan Jumlah Penyewaan Sepeda Antara Hari Kerja dan Akhir Pekan')
    
    # Penjelasan
    st.write("""
    Perbedaan jumlah sepeda yang disewakan pada hari kerja dan akhir pekan tidak jauh berbeda. 
    Dengan data yang sudah diperoleh, bisa disimpulkan bahwa banyaknya penyewaan sepeda pada hari kerja 
    kemungkinan besar disebabkan oleh aktivitas pergi dan pulang kerja. Hal ini memberikan pengaruh besar 
    pada perbandingan antara hari kerja dan hari libur.
    """)
    
    # Mengelompokkan data berdasarkan hari kerja dan akhir pekan, menghitung rata-rata penyewaan
    weekday_effect = filtered_df.groupby('weekday')['cnt'].mean().reset_index()
    weekday_labels = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    weekday_effect['weekday'] = weekday_effect['weekday'].map(weekday_labels)
    
    # Plotting
    fig, ax = plt.subplots()
    sns.barplot(x='weekday', y='cnt', data=weekday_effect, palette='viridis', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Hari')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

# Tab 3: Pengaruh Suhu, Kelembapan, dan Kecepatan Angin
with tab3:
    st.header('Pengaruh Suhu, Kelembapan, dan Kecepatan Angin Terhadap Penyewaan Sepeda')
    
    # Penjelasan
    st.write("""
    - Hubungan antara suhu dan penyewaan sepeda memiliki pengaruh yang signifikan. Orang-orang cenderung menyukai suhu yang hangat untuk menyewa sepeda dibandingkan dengan suhu yang dingin.
    - Hubungan antara kelembapan dan penyewaan sepeda tidak terlalu berpengaruh. Orang-orang cenderung menyewa sepeda saat kelembapan berada di level menengah.
    - Hubungan antara kecepatan angin dan penyewaan sepeda juga memperlihatkan bahwa orang cenderung menyewa sepeda saat kecepatan angin berada di level sepoi-sepoi.
    """)
    
    # Plotting hubungan Suhu, Kelembapan, dan Kecepatan Angin
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Suhu vs Penyewaan
    sns.scatterplot(x='temp', y='cnt', data=filtered_df, color='b', ax=axes[0])
    axes[0].set_title('Pengaruh Suhu terhadap Penyewaan Sepeda')
    axes[0].set_xlabel('Suhu (Normalisasi)')
    axes[0].set_ylabel('Penyewaan Sepeda')
    
    # Kelembapan vs Penyewaan
    sns.scatterplot(x='hum', y='cnt', data=filtered_df, color='g', ax=axes[1])
    axes[1].set_title('Pengaruh Kelembapan terhadap Penyewaan Sepeda')
    axes[1].set_xlabel('Kelembapan (Normalisasi)')
    axes[1].set_ylabel('Penyewaan Sepeda')
    
    # Kecepatan Angin vs Penyewaan
    sns.scatterplot(x='windspeed', y='cnt', data=filtered_df, color='r', ax=axes[2])
    axes[2].set_title('Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda')
    axes[2].set_xlabel('Kecepatan Angin (Normalisasi)')
    axes[2].set_ylabel('Penyewaan Sepeda')
    
    st.pyplot(fig)
