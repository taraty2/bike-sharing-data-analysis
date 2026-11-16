# Bike Sharing Data Analysis Dashboard

## Deskripsi Project
Project ini bertujuan untuk menganalisis pola penggunaan layanan Bike Sharing berdasarkan data penyewaan sepeda Capital Bikeshare di Washington D.C. selama periode 2011–2012.

Analisis dilakukan untuk mengidentifikasi tren penyewaan sepeda berdasarkan waktu, kondisi cuaca, serta karakteristik pengguna. Hasil analisis disajikan dalam bentuk visualisasi interaktif menggunakan Streamlit Dashboard.

## Business Questions
1. Bagaimana tren jumlah penyewaan sepeda setiap bulan selama tahun 2011–2012?
2. Pada jam berapa jumlah rata-rata penyewaan sepeda mencapai titik tertinggi dan terendah?
3. Bagaimana rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca?
4. Bagaimana perbandingan jumlah penyewaan sepeda oleh pengguna casual dan registered pada hari kerja dan hari libur?

## Dataset
Dataset yang digunakan adalah **Bike Sharing Dataset** dari Capital Bikeshare, dengan dua file utama:
- `day.csv`: Data penyewaan sepeda berdasarkan hari.
- `hour.csv`: Data penyewaan sepeda berdasarkan jam.

Periode data: Januari 2011 – Desember 2012.

## Project Structure
```text
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── day_data.csv
│   └── hour_data.csv
├── data/
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Tools & Libraries
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

## How to Run the Dashboard

1. Clone repository ini:
   ```bash
   git clone <repository-url>
   ```

2. Masuk ke folder project:
   ```bash
   cd <repository-folder>
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan dashboard:
   ```bash
   python -m streamlit run dashboard/dashboard.py
   ```

5. Buka URL lokal yang ditampilkan di terminal untuk melihat dashboard.

## Author
**[Tara Tabriza Rachman]**

Data Analysis Project – Asah Dicoding