import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv(r"day_data.csv")
hour_df = pd.read_csv(r"hour_data.csv")

st.title('Bike Sharing Analysis')

day_df["dteday"]=pd.to_datetime(day_df["dteday"])
hour_df["dteday"]=pd.to_datetime(hour_df["dteday"])

tab1, tab2, tab3, tab4 = st.tabs(["Data", "Rata-rata per Bulan", "Rush Hour pada Hari Kerja dan Hari Libur/Weekend", "Rata-rata Penyewaan per Jam Berdasarkan Kategori"])

with tab1:
    st.header("Data yang digunakan")
    st.write("Data sudah melalui proses assesing dan cleaning")
    st.write(day_df)
    st.caption("Data per Hari")
    st.write(hour_df)
    st.caption("Data per Jam")

with tab2:
    st.subheader("Rata-rata per Bulan (2011-2012)")
    
    # Menampilkan rata-rata penyewaan sepeda pada satu bulan tertentu
    monthly_day_df = day_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
    })
    monthly_day_df.index = monthly_day_df.index.strftime('%Y-%m')
    monthly_day_df = monthly_day_df.reset_index()
    monthly_day_df.rename(columns={
        "cnt": "total_rental"
    }, inplace=True)

    # Mengubah nama kolom 'index' (yang berasal dari dteday) menjadi 'Bulan'
    monthly_day_df.rename(columns={"dteday": "Bulan", "total_rental": "Total Rental"}, inplace=True)

    # Membuat filter dropdown untuk memilih bulan
    selected_month = st.selectbox(label = "Pilih bulan:", options= (monthly_day_df['Bulan']))

    # Filter data berdasarkan bulan yang dipilih
    filtered_data = monthly_day_df[monthly_day_df['Bulan'] == selected_month]

    # Menampilkan data yang difilter
    st.write(f"Data untuk bulan: {selected_month}")
    st.dataframe(filtered_data)

    st.subheader("Tren Rata-rata Banyak Penyewaan per Bulan (2011-2012)")
    # Menampilkan tren rata-rata banyak penyewaan per bulan
    plt.figure(figsize=(18, 5))
    plt.plot(monthly_day_df["Bulan"], monthly_day_df["Total Rental"], marker='o', linewidth=2, color="#72BCD4")
    plt.title("Rata-rata Banyak Penyewaan per Bulan (2011-2012)", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xticks(rotation=45)
    plt.xlabel("Bulan", fontsize=15)
    plt.ylabel("Banyak Penyewaan", fontsize=15)
    plt.grid()

    # Show plot in Streamlit
    st.pyplot(plt)
    

with tab3:
    st.subheader("Tren Rata-rata Penyewaan Sepeda per Jam pada Hari Kerja dan Hari Libur/Weekend (2011-2012)")
    # Memisahkan data berdasarkan hari kerja
    hari_kerja_df = hour_df.query('workingday == 1')
    avg_hari_kerja_df = hari_kerja_df.groupby('hr').agg({"cnt": "mean"})

    # Memisahkan data berdasarkan hari libur atau weekend  
    hari_libur_df = hour_df.query('workingday == 0')
    avg_hari_libur_df = hari_libur_df.groupby('hr').agg({"cnt": "mean"})
        
    # Membuat plot untuk hari kerja dan hari libur atau weekend
    plt.figure(figsize=(12, 5))
    plt.plot(avg_hari_kerja_df.index, avg_hari_kerja_df['cnt'], label='Hari Kerja', color='blue')
    plt.plot(avg_hari_libur_df.index, avg_hari_libur_df['cnt'], label='Hari Libur/Weekend', color='red')
    plt.title('Perbandingan Rata-Rata Banyak Penyewaan Sepeda per Jam (2011-2012)', size=20)
    plt.xlabel('Jam',size=12)
    plt.ylabel('Banyak penyewaan',size=12)
    plt.legend()
    plt.xticks(range(24))
    plt.grid(True)   

    st.pyplot(plt)

  
    st.subheader("Perbandingan Rata-rata Penyewaan per Jam antara Hari Kerja dan Hari Libur/Weekend (2011-2012)")
    # Membuat dropdown (selectbox) untuk memilih jam tertentu
    selected_hour = st.selectbox(
       'Pilih Jam:',
        range(24) # Opsi jam dari 0 hingga 23
    )

    # Filter data berdasarkan jam yang dipilih
    avg_kerja_selected = avg_hari_kerja_df.loc[selected_hour]
    avg_libur_selected = avg_hari_libur_df.loc[selected_hour]

    # Membuat plot berdasarkan pilihan pengguna
    plt.figure(figsize=(12, 5))

    plt.figure(figsize=(12, 5))
    plt.bar(['Hari Kerja', 'Hari Libur/Weekend'], [avg_kerja_selected['cnt'], avg_libur_selected['cnt']], color=['blue', 'red'])

    plt.title(f'Perbandingan Rata-Rata Banyak Penyewaan Sepeda pada Jam {selected_hour} (2011-2012)', size=20)
    plt.ylabel('Banyak Penyewaan', size=12)
    plt.grid(True, axis='y')
    
    # Menampilkan plot di Streamlit
    st.pyplot(plt)

with tab4 :
    st.subheader("Tren Rata-rata Penyewaan Per Jam Berdasarkan Kategori Musim (2011-2012)")
    # Membuat dropdown (selectbox) untuk memilih kategori musim
    selected_season = st.selectbox(
        'Pilih Musim:',
        ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']  # Opsi kategori musim
    )

    # Filter data berdasarkan kategori musim yang dipilih
    filtered_season_df = hour_df[hour_df['season_category'] == selected_season]

    # Kelompokkan data berdasarkan jam dan hitung rata-rata penyewaan
    avg_by_hour = filtered_season_df.groupby('hr')['cnt'].mean()

    # Buat plot menggunakan Seaborn
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=avg_by_hour.index, y=avg_by_hour.values, marker='o')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Banyak Penyewaan per Jam')
    plt.title(f'Rata-rata Banyak Penyewaan Sepeda per Jam pada {selected_season} (2011-2012)')
    plt.xticks(range(24))

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader("Perbandingan Rata-rata Penyewaan per Jam Berdasarkan Kategori Musim (2011-2012)")
    # Membuat kolom 'season_category' untuk kategori musim
    hour_df['season_category'] = pd.cut(hour_df['season'], bins=[0, 1, 2, 3, 4], labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])

    # Membuat dropdown (selectbox) untuk memilih jam
    selected_hour2 = st.selectbox('Pilih Jam :', range(24))  # Opsi jam dari 0 hingga 23

    # Filter data untuk jam yang dipilih
    filtered_hour_df = hour_df[hour_df['hr'] == selected_hour2]

    # Kelompokkan data berdasarkan kategori musim dan hitung rata-rata penyewaan pada jam yang dipilih
    avg_by_season = filtered_hour_df.groupby('season_category')['cnt'].mean()

    # Buat plot menggunakan Seaborn
    plt.figure(figsize=(12, 8))
    sns.barplot(x=avg_by_season.index, y=avg_by_season.values)
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Banyak Penyewaan per Jam')
    plt.title(f'Rata-rata Banyak Penyewaan Sepeda pada Jam {selected_hour2} Berdasarkan Kategori Musim (2011-2012)')
    
    # Tambahkan label di atas setiap bar
    for i in range(len(avg_by_season)):
        plt.text(i, avg_by_season.values[i] -1, round(avg_by_season.values[i], 0), ha='center',va="center" )

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader("Tren Rata-rata Penyewaan per Jam Berdasarkan Kategori Cuaca (2011-2012)")
    # Cerah/Sedikit Berawan', 'Berkabut/Berawan', 'Salju Ringan/Hujan Ringan', 'Hujan Berat/Salju Tebal'
    # Membuat dropdown (selectbox) untuk memilih kategori musim
    selected_weather = st.selectbox(
        'Pilih Cuaca:',
        ['Cerah/Sedikit Berawan', 'Berkabut/Berawan', 'Salju Ringan/Hujan Ringan', 'Hujan Berat/Salju Tebal']
    )

    # Filter data berdasarkan kategori musim yang dipilih
    filtered_weather_df = hour_df[hour_df['weather_category'] == selected_weather]

    # Kelompokkan data berdasarkan jam dan hitung rata-rata penyewaan
    avg_by_hour = filtered_weather_df.groupby('hr')['cnt'].mean()

    # Buat plot menggunakan Seaborn
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=avg_by_hour.index, y=avg_by_hour.values, marker='o')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Banyak Penyewaan per Jam')
    plt.title(f'Rata-rata Banyak Penyewaan Sepeda per Jam pada Cuaca {selected_weather} (2011-2012)')
    plt.xticks(range(24))

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader("Perbandingan Rata-rata Penyewaan per Jam Berdasarkan Kategori Cuaca (2011-2012)")
    # Membuat kolom 'season_category' untuk kategori musim
    hour_df['season_category'] = pd.cut(hour_df['season'], bins=[0, 1, 2, 3, 4], labels=['Cerah/Sedikit Berawan', 'Berkabut/Berawan', 'Salju Ringan/Hujan Ringan', 'Hujan Berat/Salju Tebal'])

    # Membuat dropdown (selectbox) untuk memilih jam
    selected_hour3 = st.selectbox('Pilih  Jam :', range(24))  # Opsi jam dari 0 hingga 23

    # Filter data untuk jam yang dipilih
    filtered_hour_df = hour_df[hour_df['hr'] == selected_hour3]

    # Kelompokkan data berdasarkan kategori musim dan hitung rata-rata penyewaan pada jam yang dipilih
    avg_by_weather = filtered_hour_df.groupby('weather_category')['cnt'].mean()

    # Buat plot menggunakan Seaborn
    plt.figure(figsize=(12, 5))
    sns.barplot(x=avg_by_weather.index, y=avg_by_weather.values)
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Banyak Penyewaan per Jam')
    plt.title(f'Rata-rata Banyak Penyewaan Sepeda pada Jam {selected_hour3} Berdasarkan Kategori Cuaca (2011-2012)')
    
    # Tambahkan label di atas setiap bar
    for i in range(len(avg_by_weather)):
        plt.text(i, avg_by_weather.values[i] - 1, round(avg_by_weather.values[i], 0), ha='center', va='center')

    # Tampilkan plot di Streamlit
    st.pyplot(plt)
