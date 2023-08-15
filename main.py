#### Import module #######
import streamlit as st
import datetime
import time
import pandas as pd
from statistics import mean, mode, median
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import urllib.request
from streamlit_option_menu import option_menu
from PIL import Image
from firebase_admin import credentials, storage
from google.cloud import firestore, storage
from google.cloud.firestore import Client
from datetime import datetime, timedelta
from google.oauth2 import service_account
import json


# -------------- main page-------------#
st.set_page_config(
    page_title="e-statistics2023",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
    }
)


# -----------menu untuk pilihan---------#
selected = st.sidebar.selectbox(
    label="",
    options=["Siswa", "Guru"],
    index=0,  # Default selected option index
    format_func=lambda option: f"📚 {option}" if option == "Siswa" else f"👩‍🏫 {option}",  # Adding icons
)
# ------------Page siswa------------#
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="e-statistics2023")
if selected == "Siswa":

    def get_db():
        db = firestore.Client(credentials=creds, project="e-statistics2023")
        return db



    def home():
        menu = ["Data Tunggal", "Data Kelompok"]
        milih = st.selectbox("Pilih data yang akan digunakan", menu)

        if milih == "Data Tunggal":
            df = pd.DataFrame(
                [
                    {"Nilai": ""}
                ]
            )
            df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce")  # Convert 'Nilai' column to numeric
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor", hide_index=True, height=212,
                                       width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Nilai" in edited_df.columns:
                    # Calculate statistics
                    with st.container():

                        calculated_mean = edited_df["Nilai"].mean()
                        st.write(calculated_mean,"Mean (Rata-rata): Nilai rata-rata dari seluruh data. Dihitung dengan menjumlahkan semua nilai dan kemudian membaginya dengan jumlah data.")
                        st.latex(r"\text{Mean} = \frac{\sum_{i=1}^{n} x_i}{n}")

                        #--------------------#
                        calculated_mode = mode(edited_df["Nilai"])
                        st.write(calculated_mode,"Mode (Modus): Nilai yang paling sering muncul dalam data.")
                        st.latex(r"\text{Mode} = \text{Value(s) with the highest frequency}")

                        # --------------------#
                        calculated_median = edited_df["Nilai"].median()
                        st.write(calculated_median, "Median (Median): Nilai tengah dalam urutan data yang telah diurutkan. Jika data memiliki jumlah ganjil, median adalah nilai tengah. Jika data memiliki jumlah genap, median adalah rata-rata dari dua nilai tengah.")
                        st.latex(r"\text{Median} =\begin{cases} x_{\frac{n+1}{2}}, & \text{if } n \text{ is odd} \\ \frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}, & \text{if } n \text{ is even} \end{cases}")

                        # --------------------#
                        calculated_std = np.std(edited_df["Nilai"])
                        st.write(calculated_std, "Standard Deviation (Deviasi Standar): Ukuran seberapa jauh nilai-nilai dalam data tersebar dari rata-rata. Semakin besar deviasi standar, semakin besar variasi dalam data.")
                        st.latex(r"\text{Standard Deviation} = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \text{Mean})^2}{n}}")

                        # --------------------#
                        calculated_count = edited_df["Nilai"].count()
                        st.write(calculated_count, "Count (Jumlah Data): Jumlah total data yang ada dalam dataset.")
                        st.latex(r"\text{Count} = n")

                        # --------------------#
                        calculated_max = edited_df["Nilai"].max()
                        st.write(calculated_max, "Maximum (Nilai Maksimum): Nilai tertinggi dalam dataset.")

                        # --------------------#
                        calculated_min = edited_df["Nilai"].min()
                        st.write(calculated_min, "Minimum (Nilai Minimum): Nilai terendah dalam dataset.")

                        # --------------------#
                        calculated_q1 = edited_df["Nilai"].quantile(0.25)
                        st.write(calculated_q1,"Q1 (Kuartil 1): Nilai yang membagi 25% data terbawah dari data yang telah diurutkan")
                        st.latex(r"Q1 = x_{\frac{n+1}{4}}")

                        # --------------------#
                        calculated_q3 = edited_df["Nilai"].quantile(0.75)
                        st.write(calculated_q3,"Q3 (Kuartil 3): Nilai yang membagi 75% data terbawah dari data yang telah diurutkan.")
                        st.latex(r"Q3 = x_{\frac{3(n+1)}{4}}")

                        # --------------------#
                        calculated_iqr = calculated_q3 - calculated_q1
                        st.write(calculated_iqr, "IQR (Interquartile Range): Rentang antara Q3 dan Q1, mengukur sebaran data dalam interval kuartil.")
                        st.latex(r"\text{IQR} = Q3 - Q1")

                        num_desils = 100

                        def calculate_desile(Lk, f, fd, i):
                            desile = Lk + ((f / fd) * i)
                            return desile
                        if num_desils:
                            desile_results = []

                            for k in range(1, num_desils + 1):
                                Lk = edited_df["Nilai"].min() + (
                                            (k / num_desils) * (edited_df["Nilai"].max() - edited_df["Nilai"].min()))
                                f = edited_df[edited_df["Nilai"] <= Lk]["Nilai"].count()
                                fd = edited_df["Nilai"].count()
                                i = (edited_df["Nilai"].max() - edited_df["Nilai"].min()) / num_desils

                                desile = calculate_desile(Lk, f, fd, i)
                                desile_results.append(desile)

                        desile_df = pd.DataFrame({
                            'Desil': [f'Desil-{k}' for k in range(1, num_desils + 1)],
                            'Nilai Desil': desile_results
                        })
                        st.write("Desil adalah suatu konsep dalam statistik yang digunakan untuk membagi data menjadi sepuluh bagian yang setiap bagian mewakili persentase tertentu dari total data. Dalam hal ini, desil pertama (D1) mewakili 10% data terbawah, desil kedua (D2) mewakili 20% data terbawah, dan seterusnya. Desil kesepuluh (D10) mewakili 100% data, yaitu keseluruhan data.")
                        st.latex(r"Desil_k = L_k + \left( \frac{f \cdot i}{N} \right) \cdot w")

                        st.write("Hasil Perhitungan Desil:")
                        desile_df
                        # Menghitung jumlah kelas dengan Sturges' Formula

                        def calculate_num_classes(edited_df):
                            n = len(edited_df)
                            k = int(1 + np.log2(n))
                            return k

                        # Fungsi untuk menghitung distribusi frekuensi
                        def calculate_frequency_distribution(edited_df, num_classes):
                            freq_dist = pd.cut(edited_df, bins=num_classes, include_lowest=True)
                            freq_table = pd.value_counts(freq_dist, sort=False).reset_index()
                            freq_table.columns = ['Interval', 'Frekuensi']
                            freq_table['Interval'] = freq_table['Interval'].astype(str)
                            return freq_table
                        num_classes = calculate_num_classes(edited_df)

                        # Menghitung distribusi frekuensi
                        freq_table = calculate_frequency_distribution(edited_df['Nilai'], num_classes)
                        st.title("Distribusi Frekuensi")

                        # Menampilkan informasi distribusi frekuensi
                        st.write("Menentukan Jumlah Kelas (Sturges' Formula):", num_classes)
                        st.latex(r'k = 1 + \log_2(n)')
                        st.write("Tabel Distribusi Frekuensi:")
                        st.write(freq_table)

                        # Membuat histogram menggunakan Matplotlib
                        plt.figure(figsize=(10, 6))
                        plt.hist(edited_df['Nilai'], bins=num_classes, edgecolor='black', alpha=0.7)
                        plt.xlabel("Interval")
                        plt.ylabel("Frekuensi")
                        plt.title("Histogram Distribusi Frekuensi")
                        st.pyplot(plt)

                        # Membuat ogive menggunakan Matplotlib
                        cumulative_freq = np.cumsum(freq_table['Frekuensi'])
                        plt.figure(figsize=(10, 6))
                        plt.plot(freq_table['Interval'], cumulative_freq, marker='o', linestyle='-', color='orange')
                        plt.xlabel("Interval")
                        plt.ylabel("Frekuensi Kumulatif")
                        plt.title("Ogive - Distribusi Kumulatif")
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                else:
                    st.warning("Data kosong atau kolom 'Nilai' belum diisi.")

        elif milih == "Data Kelompok":
            df = pd.DataFrame(
                [
                    {"Interval": "", "Frekuensi": ""}
                ]
            )
            df["Frekuensi"] = pd.to_numeric(df["Frekuensi"], errors="coerce")  # Convert 'Nilai' column to numeric

            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor", hide_index=True, height=212,
                                       width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Frekuensi" in edited_df.columns:
                    # Calculate statistics or any other processing you want
                    with st.container():
                        # Menghitung total frekuensi
                        total_frekuensi = edited_df['Frekuensi'].sum()

                        edited_df['Midpoint'] = [(int(interval.split('-')[0]) + int(interval.split('-')[1])) / 2 for interval in
                                          edited_df['Interval']]
                        frekuensi_kumulatif = np.cumsum(edited_df["Frekuensi"])
                        df = edited_df
                        df["Frekuensi Kumulatif"] = frekuensi_kumulatif
                        st.write(df, hide_index=True)
                        # Menghitung rata-rata tertimbang
                        weighted_sum = sum([midpoint * freq for midpoint, freq in zip(edited_df['Midpoint'], edited_df['Frekuensi'])])
                        weighted_mean = weighted_sum / total_frekuensi
                        st.write(weighted_mean,"Rata-rata (Mean): Rata-rata dari suatu kelompok data kelompok dihitung dengan menjumlahkan seluruh nilai tengah (midpoint) dari interval dan membaginya dengan jumlah frekuensi total")

                        # Menghitung median kelompok
                        cumulative_freq = np.cumsum(edited_df['Frekuensi'])
                        median_class_idx = cumulative_freq[cumulative_freq >= total_frekuensi / 2].idxmax()
                        if median_class_idx == 0:
                            grouped_median = edited_df['Midpoint'][0] + (
                                    (total_frekuensi / 2 - cumulative_freq[0]) / edited_df['Frekuensi'][0]
                            ) * (int(edited_df['Interval'][0].split('-')[1]) - int(edited_df['Interval'][0].split('-')[0]))
                        else:
                            grouped_median = edited_df['Midpoint'][median_class_idx] + (
                                    (total_frekuensi / 2 - cumulative_freq[median_class_idx - 1]) /
                                    edited_df['Frekuensi'][median_class_idx]
                            ) * (int(edited_df['Interval'][median_class_idx].split('-')[1]) - int(
                                edited_df['Interval'][median_class_idx].split('-')[0]))
                        st.write(weighted_mean,"Median: Median kelompok adalah nilai yang terletak di tengah-tengah data yang telah diurutkan. Untuk menghitung median kelompok, Anda perlu mencari interval yang memiliki jumlah frekuensi kumulatif lebih besar dari setengah dari total frekuensi data. Lalu, gunakan formula yang telah dijelaskan sebelumnya untuk menghitung median pada interval tersebut.")
                        # Menghitung modus kelompok
                        index_of_mode_class = edited_df['Frekuensi'].idxmax()
                        lower_bound_mode = int(edited_df['Interval'][index_of_mode_class].split('-')[0])
                        interval_size = int(edited_df['Interval'][1].split('-')[0]) - int(edited_df['Interval'][0].split('-')[0])
                        frequency_of_mode_class = edited_df['Frekuensi'][index_of_mode_class]
                        frequency_of_prev_class = edited_df['Frekuensi'][index_of_mode_class - 1] if index_of_mode_class > 0 else 0
                        frequency_of_next_class = edited_df['Frekuensi'][index_of_mode_class + 1] if index_of_mode_class < len(
                            df) - 1 else 0
                        grouped_mode = lower_bound_mode + ((frequency_of_mode_class - frequency_of_prev_class) / (
                                    (frequency_of_mode_class - frequency_of_prev_class) + (
                                        frequency_of_mode_class - frequency_of_next_class))) * interval_size
                        st.write(grouped_mode,"Modus: Modus kelompok adalah nilai yang memiliki frekuensi tertinggi. Anda dapat menghitung modus dengan mencari interval dengan frekuensi tertinggi.")
                        # Menghitung deviasi standar
                        std_group = np.sqrt(sum(((edited_df['Midpoint'] - weighted_mean) ** 2) * edited_df['Frekuensi']) / total_frekuensi)
                        st.write(std_group,"Deviasi Standar: Deviasi standar kelompok mengukur seberapa jauh nilai-nilai dalam data tersebar dari rata-rata. Rumus deviasi standar kelompok menggambarkan perbedaan antara nilai tengah setiap interval dan rata-rata dari data kelompok.")
                        # Menghitung rentang interkuartil
                        q1_index = cumulative_freq[cumulative_freq >= total_frekuensi * 0.25].index[0]
                        q1_lower = int(edited_df['Interval'][q1_index].split('-')[0])
                        q1_size = int(edited_df['Interval'][1].split('-')[0]) - int(edited_df['Interval'][0].split('-')[0])
                        cumulative_freq_before_q1 = cumulative_freq[q1_index - 1] if q1_index > 0 else 0
                        q1 = q1_lower + ((total_frekuensi * 0.25 - cumulative_freq_before_q1) / edited_df['Frekuensi'][
                            q1_index]) * q1_size
                        st.write(q1 ," Kuartil adalah nilai yang membagi data menjadi empat bagian yang sama besar. Q1 adalah nilai yang membagi 25% data terbawah dari data yang telah diurutkan")

                        q3_index = cumulative_freq[cumulative_freq >= total_frekuensi * 0.75].index[0]
                        q3_lower = int(edited_df['Interval'][q3_index].split('-')[0])
                        q3_size = int(edited_df['Interval'][1].split('-')[0]) - int(edited_df['Interval'][0].split('-')[0])
                        cumulative_freq_before_q3 = cumulative_freq[q3_index - 1] if q3_index > 0 else 0
                        q3 = q3_lower + ((total_frekuensi * 0.75 - cumulative_freq_before_q3) / edited_df['Frekuensi'][
                            q3_index]) * q3_size
                        st.write(q3 ,"S edangkan Q3 membagi 75% data terbawah.")
                        iqr = q3 - q1
                        st.write(iqr, "Rentang Interkuartil (IQR): Rentang antara Q3 dan Q1 mengukur sebaran data dalam interval kuartil.")


                        # Hitung total frekuensi
                        total_frekuensi = sum(frekuensi_kumulatif)
                        # Create a histogram using matplotlib
                        st.write(
                                "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")

                        plt.figure(figsize=(8, 6))
                        plt.bar(edited_df['Interval'], edited_df["Frekuensi"])
                        plt.xlabel("Interval")
                        plt.ylabel("Frekuensi")
                        plt.title("Histogram Data Frekuensi")
                        st.pyplot(plt)

                        # Create a line chart using matplotlib
                        plt.figure(figsize=(8, 6))
                        plt.plot(edited_df["Interval"], edited_df["Frekuensi"], marker='o')
                        plt.xlabel("Interval")
                        plt.ylabel("Frekuensi")
                        plt.title("Line Chart Data Frekuensi")
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                        st.write(
                                "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")

                        # Pie Chart
                        labels = edited_df["Interval"]
                        sizes = edited_df["Frekuensi"]
                        plt.figure(figsize=(8, 8))
                        wedges, texts, autotexts = plt.pie(sizes, autopct='%1.1f%%', startangle=80,
                                                               pctdistance=0.6)
                        plt.title("Pie Chart Data Frekuensi")

                        # Create legend and place it below the pie chart
                        plt.legend(wedges, labels, title="Kategori", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                        st.pyplot(plt)
                        st.write(
                                "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")

                        # Hitung proporsi frekuensi kumulatif
                        cumulative_freq = np.cumsum(edited_df["Frekuensi"])
                        plt.figure(figsize=(10, 6))
                        plt.plot(edited_df["Interval"], cumulative_freq, marker='o', linestyle='-', color='orange')
                        plt.xlabel("Interval")
                        plt.ylabel("Frekuensi Kumulatif")
                        plt.title("Ogive - Distribusi Kumulatif")
                        # Tampilkan grid
                        plt.grid(True)
                        plt.xticks(rotation=45)
                        st.pyplot(plt)


                else:
                    st.warning("Data kosong atau kolom 'Nilai' belum diisi.")

    def post_nilai(db, nama_text, asal_sekolah_text, kelas_text, nilai, correct_answers, total_questions):
        payload = {
            "nama": nama_text,
            "asal_sekolah": asal_sekolah_text,
            "kelas": kelas_text,
            "nilai": nilai,
            "total_benar": correct_answers,
            "total_soal": total_questions
        }
        doc_ref = db.collection("nilai").document()
        doc_ref.set(payload)
        return

    def exam_ques():
        st.write("**Isi biodata terlebih dahulu**")

        db = get_db()
        questions_ref = db.collection("question")
        questions = questions_ref.get()

        nama_text = st.text_input("Nama Lengkap", key="nama_input")
        asal_sekolah_text = st.text_input("Asal Sekolah", key="asal_sekolah_input")
        kelas_text = st.text_input("Kelas", key="kelas_input")
        st.write("------")

        question_data = []
        for question in questions:
            question_dict = question.to_dict()
            question_dict["id"] = question.id  # Simpan ID dokumen dalam dictionary
            question_data.append(question_dict)

        questions_and_answers = []
        for idx, question in enumerate(question_data):
            # Display image from Firebase Storage
            st.write(f"**Pertanyaan soal {idx+1}:**", question["soal"])
            key = f"radio_{idx + 1}"  # Buat key yang unik berdasarkan indekshttps
            if question["foto_url"] is not None:
                st.image(question["foto_url"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            if question["tautan_url_mat"] =="":
                st.write("")
            else :
                st.image(question["tautan_url_mat"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            selected_option = st.radio("**Pilihlah Jawaban yang tepat** :",
                                       [question["option_A"], question["option_B"], question["option_C"],
                                        question["option_D"]], key=key)


            questions_and_answers.append((question, selected_option))
        total_questions = len(questions_and_answers)
        correct_answers = 0
        nilai = correct_answers / total_questions * 100

        end_button = st.button("Selesai")
        if end_button:
            if nama_text == "":
                st.warning("Silahkan lengkapi biodata")
            else :
                db = get_db()
                post_nilai(db, nama_text, asal_sekolah_text, kelas_text, nilai, correct_answers, total_questions)
                st.success("Jawaban telah disimpan")


    def view_lesson():
        db = get_db()
        leassons_ref = db.collection("postingan")
        leassons = leassons_ref.get()

        leasson_data = []
        for leasson in leassons:
            leasson_dict = leasson.to_dict()
            leasson_dict["id"] = leasson.id  # Simpan ID dokumen dalam dictionary
            leasson_data.append(leasson_dict)

        for idx, leasson in enumerate(leasson_data):
            # Display image from Firebase Storage
            st.subheader(f'{idx + 1}. {leasson["judul"]}')
            if leasson["foto_url"] is not None:
                st.image(leasson["foto_url"], use_column_width=True)
             if leasson["tautan_url"] != "":
                if "youtube.com" in leasson["tautan_url"] or "youtu.be" in leasson["tautan_url"]:
                    st.video(leasson["tautan_url"], format="mp4", start_time=0)
                else :
                    st.image(leasson["tautan_url"], use_column_width=True)
            else :
                    st.write("")
            if leasson["penjelasan"] == "":
                st.write("")
            else:
                with st.expander("Penjelasan"):
                    st.write(leasson["penjelasan"])
    def siswa():
        with st.sidebar:
            # Menambahkan logo perusahaan
            st.image("https://raw.githubusercontent.com/ilman79/e-statistics2023/main/assets/logo.png")
            selected = option_menu(
                menu_title=None,
                options=["Materi", "Latihan", "Quiz"],
                icons=["book", "calculator", "clipboard"],
                menu_icon="cast",
                styles={
                    "nav-link-selected": {"background-color": "#00BFFF"}

                }

            )
        if selected == "Quiz":
            exam_ques()
        elif selected == "Latihan":
            home()
        elif selected == "Materi":
            view_lesson()


    if __name__ == "__main__":
        siswa()

# ----------page guru--------#
if selected == "Guru":
    def get_db():
        db = firestore.Client(credentials=creds, project="e-statistics2023")
        return db


    def create_question():
        with st.form(key="form"):
            st.subheader("Buat Soal Baru")
            uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])
            tautan_url_mat = st.text_input("Masukkan link tautan media:")

            question_text = st.text_area("Pertanyaan")

            option_a = st.text_input("Pilihan A")
            option_b = st.text_input("Pilihan B")
            option_c = st.text_input("Pilihan C")
            option_d = st.text_input("Pilihan D")

            correct_option = st.selectbox("Jawaban Benar", ["Pilihan A", "Pilihan B", "Pilihan C", "Pilihan D"])

            if st.form_submit_button("Simpan Soal"):
                db = get_db()
                post_question(db, question_text,tautan_url_mat, uploaded_file, option_a, option_b, option_c, option_d,
                              correct_option)
                st.success("Soal berhasil ditambahkan!")
                st.experimental_rerun()

    def post_question(db, question_text, tautan_url_mat, uploaded_file, option_a, option_b, option_c, option_d, correct_option):
        payload = {
            "soal": question_text,
            "tautan_url_mat":tautan_url_mat,
            "foto_url": None,
            "option_A": option_a,
            "option_B": option_b,
            "option_C": option_c,
            "option_D": option_d,
            "jawaban": correct_option
        }
        if uploaded_file is not None:
            # Upload gambar ke Firebase Storage dan dapatkan URL
            # Mengunggah gambar ke Firebase Storage dan dapatkan URL
            blob = bucket.blob("soal/" + uploaded_file.name)

            # Menggunakan BytesIO untuk membaca data gambar
            image_data = uploaded_file.read()

            # Mengunggah data gambar ke Firebase Storage
            blob.upload_from_string(image_data, content_type=uploaded_file.type)
            expiration_time = datetime.utcnow() + timedelta(days=3650)  # 10 tahun * 365 hari/tahun
            image_url_with_token = blob.generate_signed_url(expiration=expiration_time)  # URL dengan token akses

            payload["foto_url"] = image_url_with_token
        if tautan_url_mat is not None:
            # Upload gambar ke Firebase Storage dan dapatkan URL
            # Mengunggah gambar ke Firebase Storage dan dapatkan URL

            # Menggupload link
            payload["tautan_url_mat"] = tautan_url_mat
        doc_ref = db.collection("question").document()
        doc_ref.set(payload)
        return
    def view_questions():
        db = get_db()
        questions_ref = db.collection("question")
        questions = questions_ref.get()

        question_data = []
        for question in questions:
            question_dict = question.to_dict()
            question_dict["id"] = question.id  # Simpan ID dokumen dalam dictionary
            question_data.append(question_dict)

        for idx, question in enumerate(question_data):
            # Display image from Firebase Storage

            key = f"radio_{idx+ 1}"  # Buat key yang unik berdasarkan indekshttps
            if question["foto_url"] is not None:
                st.image(question["foto_url"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            if question["tautan_url_mat"] == "":
                st.write("")
            else:
                st.image(question["tautan_url_mat"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            st.write(f"**Pertanyaan soal {idx + 1}:**", question["soal"])
            selected_option = st.radio("Pilih Jawaban:",
                                       [question["option_A"], question["option_B"], question["option_C"],
                                        question["option_D"]], key=key)

            if st.button(f"Hapus Soal {idx + 1}"):
                # Hapus pertanyaan dari Firebase Firestore berdasarkan ID dokumen
                question_ref = db.collection("question").document(question["id"])
                question_ref.delete()
                st.success("Soal berhasil dihapus!")
                st.experimental_rerun()


    def create_lesson():
        with st.form(key="form"):
            st.subheader("Buat Materi Baru")
            judul_text = st.text_input("Judul Materi :")
            foto_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])
            tautan_url = st.text_input("Masukkan link tautan media:")
            penjelasan_text = st.text_area("Penjelasan yang akan anda sampaikan berupa text :")

            if st.form_submit_button("Simpan Materi"):
                db = get_db()
                post_materi(db, judul_text, foto_file,tautan_url, penjelasan_text)
                st.success("Berhasil menambahkan materi")
                st.experimental_rerun()


    def post_materi(db, judul_text, foto_file,tautan_url, penjelasan_text):
        payload = {
            "judul": judul_text,
            "foto_url": None,
            "tautan_url" : None,
            "penjelasan" : penjelasan_text
        }
        if foto_file is not None:
            # Upload gambar ke Firebase Storage dan dapatkan URL
            # Mengunggah gambar ke Firebase Storage dan dapatkan URL
            blob = bucket.blob("materi/" + foto_file.name)

            # Menggunakan BytesIO untuk membaca data gambar
            image_data = foto_file.read()

            # Mengunggah data gambar ke Firebase Storage
            blob.upload_from_string(image_data, content_type=uploaded_file.type)
            expiration_time = datetime.utcnow() + timedelta(days=3650)  # 10 tahun * 365 hari/tahun
            image_url_with_token = blob.generate_signed_url(expiration=expiration_time)  # URL dengan token akses

            payload["foto_url"] = image_url_with_token
        if tautan_url is not None:
            # Upload gambar ke Firebase Storage dan dapatkan URL
            # Mengunggah gambar ke Firebase Storage dan dapatkan URL

            # Menggupload link
            payload["tautan_url"] = tautan_url
        doc_ref = db.collection("postingan").document()
        doc_ref.set(payload)
        return
    def view_lesson():
        db = get_db()
        leassons_ref = db.collection("postingan")
        leassons = leassons_ref.get()

        leasson_data = []
        for leasson in leassons:
            leasson_dict = leasson.to_dict()
            leasson_dict["id"] = leasson.id  # Simpan ID dokumen dalam dictionary
            leasson_data.append(leasson_dict)

        for idx, leasson in enumerate(leasson_data):
            # Display image from Firebase Storage
            st.subheader(f'{idx+1}. {leasson["judul"]}')
            if leasson["foto_url"] is not None:
                st.image(leasson["foto_url"], use_column_width=True)
            if leasson["tautan_url"] != "":
                if "youtube.com" in leasson["tautan_url"] or "youtu.be" in leasson["tautan_url"]:
                    st.video(leasson["tautan_url"], format="mp4", start_time=0)
                else :
                    st.image(leasson["tautan_url"], use_column_width=True)
            else :
                    st.write("")
            with st.expander("Penjelasan"):
                st.write(leasson["penjelasan"])
            if st.button(f"Hapus Materi {idx + 1}"):
                # Hapus pertanyaan dari Firebase Firestore berdasarkan ID dokumen
                leasson_ref = db.collection("postingan").document(leasson["id"])
                leasson_ref.delete()
                st.success("Soal berhasil dihapus!")
                st.experimental_rerun()


    def report():
        st.subheader("Daftar Nilai")
        db = get_db()
        documents_ref = db.collection("nilai")
        documents = documents_ref.stream()

        documents_databases = []
        for doc in documents:
            data = doc.to_dict()
            data["id"] = doc.id  # Simpan ID dokumen dalam dictionary
            documents_databases.append(data)

        df = pd.DataFrame(documents_databases)

        # Display the DataFrame
        st.write("Report hasil pengerjaan siswa:")
        st.dataframe(df, width=1000, height=350)

        # Checkbox to select rows for deletion
        if not df.empty:
            selected_rows = st.multiselect("Pilih baris untuk dihapus", df["nama"])

            # Delete selected rows from Firestore
            if st.button("hapus data"):
                for idx in df.index:
                    if df.loc[idx, "nama"] in selected_rows:
                        doc_id = documents_databases[idx]["id"]
                        doc_ref = db.collection("nilai").document(doc_id)
                        doc_ref.delete()
                st.success("Data berhasil dihapus!")
                st.experimental_rerun()

        st.write("-----")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Report",
            data=csv,
            file_name='report.csv',
            mime='text/csv',
        )



    def login_page():
        with st.sidebar:
            st.image("https://raw.githubusercontent.com/ilman79/e-statistics2023/main/assets/logo_2.png")
            st.subheader("Hubungi Kami")
            st.write("Jika Anda memiliki pertanyaan, saran, atau masukan, jangan ragu untuk menghubungi kami:")
            st.write(" :mailbox: : info@e-statistics.com")
            st.markdown(" :phone: : 08089080980980")
            st.write(" :computer: : www.linkedin.com/company/e-statistics")

        st.subheader("Selamat Datang, silahkan login terlebih dahulu")
        st.write("-----")
        username = st.text_input("Username:")
        password = st.text_input("Password: ", type="password")

        if st.button("Login"):

            if authenticate_user(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.experimental_rerun()
                guru()

            else:
                st.error("Invalid username or password.")
        st.write("-----")
        with st.expander(":mailbox: Kontak Email "):
            contact_form = """
        <form action="https://formsubmit.co/gifariilman79@gmail.com" method="POST">
            <input type="hidden" name="_blacklist" value="spammy pattern, banned term, phrase">
            <input type="hidden" name="_subject" value="New Account Register e-statistics2023!">
            <input type="text" name="name" placeholder="Nama Lengkap" required>
            <input type="email" name="email" placeholder="Alamat Email" required>
            <textarea name="message" placeholder="Tulis Pesan `saya ingin mendapatkan akses` "></textarea>
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_autoresponse" value="Terima kasih sudah menghubungi e-statistik, untuk akses username : admin dan password : admin">
            <button type="submit">Send</button>

        </form>

            """

            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

            local_css("style.css")
            st.markdown(contact_form, unsafe_allow_html=True)


    def logout():
        # Reset session state to indicate logout
        st.session_state.logged_in = False
        st.success("Logged out successfully!")


    def authenticate_user(username, password):
        db = get_db()
        admin_ref = db.collection("admin")
        admin_docs = admin_ref.stream()

        for admin_doc in admin_docs:
            admin_data = admin_doc.to_dict()
            if admin_data["username"] == username and admin_data["passward"] == password:
                return True

        return False


    def guru():
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if st.session_state.logged_in:
            with st.sidebar:
                st.image("https://raw.githubusercontent.com/ilman79/e-statistics2023/main/assets/logo_2.png")
                selected = option_menu(
                    menu_title=None,
                    options=["Daftar Materi","Edit Materi", "Tambah Soal", "Daftar Soal", "Nilai Siswa", "Keluar Halaman" ],
                    icons=["book", "pen", "clipboard", "list", "key","window"],
                    menu_icon="cast",
                    styles={
                        "nav-link-selected": {"background-color": "#00BFFF"}

                    }

                )


            if selected == "Tambah Soal":
                create_question()
            elif selected == "Daftar Materi":
                view_lesson()
            elif selected == "Daftar Soal":
                view_questions()
            elif selected == "Nilai Siswa":
                report()
            elif selected == "Edit Materi":
                create_lesson()
            elif selected == "Keluar Halaman":
                logout()
                st.experimental_rerun()
        else:
            login_page()


    if __name__ == "__main__":
        guru()
