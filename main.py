import streamlit as st
import datetime
import time
import pandas as pd
from statistics import mean, mode, median
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import firebase_admin
from google.cloud import firestore, storage
from google.cloud.firestore import Client
from datetime import datetime, timedelta
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Menambahkan custom CSS ke tampilan Streamlit
selected = option_menu( menu_title=None, options=["Siswa", "Guru"],
                        icons=["book", "people"],
                        menu_icon="cast",
                        orientation = "horizontal",
                        styles={
                            "nav-link":{
                                "margin":"0px",
                                "align-items": "flex-start"
                            }
                        }
                        )

if selected == "Siswa":
    import streamlit as st
    import datetime
    import time
    import pandas as pd
    from statistics import mean, mode, median
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    from streamlit_option_menu import option_menu
    from PIL import Image
    import firebase_admin
    from google.cloud import firestore, storage
    from google.cloud.firestore import Client
    from datetime import datetime, timedelta
    from google.oauth2 import service_account
    import json
    
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creads, project="e-statistics2023")

    def get_db():
        db = firestore.Client(credentials=creads, project="e-statistics2023")
        return db 
    
    def home():
        st.title("Latihan")
        menu = ["Data Tunggal", "Data Kelompok"]
        milih = st.selectbox("Pilih data yang akan digunakan", menu)
    
        if milih == "Data Tunggal":
            df = pd.DataFrame(
                [
                    {"Nilai": ""}
                ]
            )
            df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce")  # Convert 'Nilai' column to numeric
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor",hide_index=True,height=280, width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Nilai" in edited_df.columns:
                    ##### Menghitung mean
                    calculated_mean = mean(edited_df["Nilai"])
                    st.success(f"Mean Nilai: {calculated_mean:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    #### Menghitung modus
                    calculated_mode = mode(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_mode:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    #### Menghitung Median
                    calculated_median = median(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_median:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    calculated_std = np.std(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_std:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    calculated_std = np.std(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_std:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    st.write("Nilai Minimum:", np.min(edited_df["Nilai"]))
                    st.write("Nilai Maksimum:", np.max(edited_df["Nilai"]))
    
                else:
                    st.warning("Data kosong atau kolom 'Nilai' belum diisi.")
        elif milih == "Data Kelompok":
            df = pd.DataFrame(
                [
                    {"Interval": "", "Frekuensi": ""}
                ]
            )
            df["Frekuensi"] = pd.to_numeric(df["Frekuensi"], errors="coerce")  # Convert 'Nilai' column to numeric
    
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor", hide_index=True,height=280, width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Frekuensi" in edited_df.columns:
                    # Calculate statistics or any other processing you want
                    st.write("Data yang telah diedit:")
                    st.write(edited_df)
    
                    # Create a histogram using matplotlib
                    with st.expander("Histogram Data Frekuensi"):
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
                        plt.figure(figsize=(8, 6))
                        plt.bar(edited_df['Kategori'], edited_df["Frekuensi"])
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Histogram Data Frekuensi")
                        st.pyplot(plt)
                    # Create a bar chart using seaborn
                    with st.expander("Bar Chart Data Frekuensi"):
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
                        plt.figure(figsize=(8, 6))
                        sns.barplot(y="Kategori", x="Frekuensi", data=edited_df)
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Bar Chart Data Frekuensi")
                        st.pyplot(plt)
    
                    # Create a line chart using matplotlib
                    with st.expander("Line Chart Data Frekuensi"):
                        plt.figure(figsize=(8, 6))
                        plt.plot(edited_df["Kategori"], edited_df["Frekuensi"], marker='o')
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Line Chart Data Frekuensi")
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
    
                    # Pie Chart
                    with st.expander("Pie Chart Data Frekuensi"):
                        labels = edited_df["Kategori"]
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
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
    
                    frekuensi_kumulatif = np.cumsum(edited_df["Frekuensi"])
                    df = edited_df
                    df["Frekuensi Kumulatif"] = frekuensi_kumulatif
                    st.write(df)
    
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
        st.title('Quiz')
        st.write("Isi data terlebih dahulu")
    
        db = get_db()
        questions_ref = db.collection("question")
        questions = questions_ref.get()
    
        nama_text = st.text_input("Nama Lengkap", key="nama_input")
        asal_sekolah_text = st.text_input("Asal Sekolah", key="asal_sekolah_input")
        kelas_text = st.text_input("Kelas", key="kelas_input")
        st.write("------")
        question_data = []
        for question in questions:
            question_data.append(question.to_dict())
    
        questions_and_answers = []
    
        for idx, question in enumerate(question_data):
            st.write(f"Pertanyaan {idx + 1}:", question["soal"])
            st.image(question["foto_url"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            key = f"radio_{idx}"  # Buat key yang unik berdasarkan indeks
            selected_option = st.radio("Pilih Jawaban:", [question["option_A"], question["option_B"], question["option_C"],
                                                          question["option_D"]], key=key)
    
            questions_and_answers.append((question, selected_option))
        total_questions = len(questions_and_answers)
        correct_answers = 0
        nilai = correct_answers / total_questions * 100
    
        end_button = st.button("Selesai")
        if end_button:
            db = get_db()
            post_nilai(db, nama_text, asal_sekolah_text, kelas_text, nilai, correct_answers, total_questions)
    
    def lesson():
        st.title("Statistika Pada Data Tunggal dan Kelompok")
    
        st.markdown(f"""
                    Statistika adalah sebuah ilmu atau metode ilmiah yang mempelajari tentang bagaimana merencanakan, mengumpulkan,
                    mengelola, menginterprestasi kemudian menganalisa data untuk kemudian mempresentasikan hasil data yang diperoleh.
                    Sedangkan Menurut Kamus Besar Bahasa Indonesia (KBBI), statistik didefinisikan sebagai angka-angka atau catatan yang dikumpulkan, dikelompokkan
                    dan ditabulasi sehingga didapatkan informasi berkaitan dengan masalah tertentu. \n
    
                    Data adalah himpunan keterangan atau bilangan dari objek yang diamati. Menurut jenisnya, data dibedakan menjadi: \n
                    a. Data Kuantitatif adalah data yang dapat dinyatakan dengan bilangan. Menurut cara mendapatkan data kuantitatif dibagi 2 yaitu: \n
                    ➢ Data Diskrit atau data Data Cacahan: data yang diperolah dengan cara mencacah atau menghitung satu per satu. \n
                    Contoh : \n
                    • Banyaknya wisatawan berkunjung ke bali di bulan ini 600 orang. \n
                    • Satu kilogram telur berisi 16 butir. \n
                    ➢ Data Kontinu atau Data Ukuran atau Data Timbangan: data yang diperoleh dengan cara mengukur atau menimbang dengan alat ukur yang valid. \n
                    Contoh : \n
                    • Berat badan 3 orang wisatawan adalah 45 kg, 50 kg, 53 kg. \n
                    • Diameter pizza = 72,5 mm. \n
    
                    Data Kualitatif adalah data yang tidak dapat dinyatakan dengan bilangan (menyatakan mutu atau kualitas).\n
                    Contoh :\n
                    • Data jenis kelamin.\n
                    • Data makanan kegemaran wisatawan.\n
    
                    Data yang baru dikumpulkan dan belum diolah disebut data mentah.\n
                    Metode pengumpulan data ada 2 yaitu:\n
                    1. Metode Sampling adalah pengumpulan data dengan meneliti sebagian anggota populasi.\n
                    2. Metode Sensus adalah pengumpulan data dengan meneliti semua anggota populasi.\n
                    Adapun cara untuk mengumpulkan data adalah:\n
                    1. Wawancara (Interview).\n
                    2. Angket (Kuesioner).\n
                    3. Pengamatan (Observasi).\n
                    4. Koleksi (data dari media cetak atau elektronik).\n
                    5. Penyajian Data.\n
    
                    Bantuk Tabel atau daftar tabel \n
                    Pada dasarnya ada 3 macam tabel yaitu \n
                    1. Tabel Baris dan Kolom \n
                    contohnya : \n
                    """)
        st.image("assets/image_1.PNG", caption="Deskripsi Gambar", width=400)
        st.markdown(f""" 
                    2. Tabel Kontigensi \n
                    contohnya : \n
    
        """)
        st.image("assets/image_1.PNG", caption="Deskripsi Gambar", width=400)
        st.markdown(
            """
            ---\n
            Referensi \n
            [1] https://insanpelajar.com/statistik-dan-statistika/ \n
            """
        )
    
    def siswa():
        with st.sidebar:
            # Menambahkan logo perusahaan
            st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
            selected = option_menu(
                menu_title="Main Menu",
                options=["Materi", "Latihan", "Quiz"],
                icons=["book", "calculator", "clipboard"],
                menu_icon="cast",
                styles={
    
                }
    
            )
        if selected == "Quiz":
            exam_ques()
        elif selected == "Latihan":
            home()
        elif selected == "Materi":
            lesson()
    
    if __name__ == "__main__":
        siswa()
if selected == "Guru" :
    client = storage.Client.from_service_account_json("key.json")
    bucket = client.bucket("e-statistics2023.appspot.com")
    def get_db():
        db = storage.Client.from_service_account_json("key.json")
        return db
    def create_question():
        with st.form(key="form"):
            st.subheader("Buat Soal Baru")
            uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])
            question_text = st.text_area("Pertanyaan")
    
            option_a = st.text_input("Pilihan A")
            option_b = st.text_input("Pilihan B")
            option_c = st.text_input("Pilihan C")
            option_d = st.text_input("Pilihan D")
    
            correct_option = st.radio("Jawaban Benar", [option_a, option_b, option_c, option_d])
    
            if st.form_submit_button("Simpan Soal"):
                db = get_db()
                post_question(db, question_text, uploaded_file, option_a, option_b, option_c, option_d,
                              correct_option)
    
    
    def post_question(db, question_text, uploaded_file, option_a, option_b, option_c, option_d, correct_option):
        payload = {
            "soal": question_text,
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
        doc_ref = db.collection("question").document()
        doc_ref.set(payload)
        return
        with st.form(key="form"):
            st.subheader("Buat Soal Baru")
            uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])
            question_text = st.text_area("Pertanyaan")
    
            option_a = st.text_input("Pilihan A")
            option_b = st.text_input("Pilihan B")
            option_c = st.text_input("Pilihan C")
            option_d = st.text_input("Pilihan D")
    
            correct_option = st.radio("Jawaban Benar", [option_a, option_b, option_c, option_d])
    
            if st.form_submit_button("Simpan Soal"):
                db = get_db()
                post_question(db, question_text, uploaded_file, option_a, option_b, option_c, option_d,
                              correct_option)
    
    
    def home():
        st.title("Latihan")
        menu = ["Data Tunggal", "Data Kelompok"]
        milih = st.selectbox("Pilih data yang akan digunakan", menu)
    
        if milih == "Data Tunggal":
            df = pd.DataFrame(
                [
                    {"Nilai": ""}
                ]
            )
            df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce")  # Convert 'Nilai' column to numeric
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor", hide_index=True,height=280, width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Nilai" in edited_df.columns:
                    ##### Menghitung mean
                    calculated_mean = mean(edited_df["Nilai"])
                    st.success(f"Mean Nilai: {calculated_mean:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    #### Menghitung modus
                    calculated_mode = mode(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_mode:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    #### Menghitung Median
                    calculated_median = median(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_median:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    calculated_std = np.std(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_std:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    calculated_std = np.std(edited_df["Nilai"])
                    st.success(f"Mode Nilai: {calculated_std:.2f}")
                    expander = st.expander("See explanation")
                    expander.write(
                        "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                    expander.image(
                        "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                        caption="Ilustrasi Statistika", use_column_width=True)
    
                    st.write("Nilai Minimum:", np.min(edited_df["Nilai"]))
                    st.write("Nilai Maksimum:", np.max(edited_df["Nilai"]))
    
                else:
                    st.warning("Data kosong atau kolom 'Nilai' belum diisi.")
        elif milih == "Data Kelompok":
            df = pd.DataFrame(
                [
                    {"Interval": "", "Frekuensi": ""}
                ]
            )
            df["Frekuensi"] = pd.to_numeric(df["Frekuensi"], errors="coerce")  # Convert 'Nilai' column to numeric
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor", hide_index=True,height=280, width=400)
            end_button = st.button("Selesai")
            if end_button:
                if not edited_df.empty and "Frekuensi" in edited_df.columns:
                    # Calculate statistics or any other processing you want
                    st.write("Data yang telah diedit:")
                    st.write(edited_df)
    
                    # Create a histogram using matplotlib
                    with st.expander("Histogram Data Frekuensi"):
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
                        plt.figure(figsize=(8, 6))
                        plt.bar(edited_df['Kategori'], edited_df["Frekuensi"])
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Histogram Data Frekuensi")
                        st.pyplot(plt)
                    # Create a bar chart using seaborn
                    with st.expander("Bar Chart Data Frekuensi"):
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
                        plt.figure(figsize=(8, 6))
                        sns.barplot(y="Kategori", x="Frekuensi", data=edited_df)
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Bar Chart Data Frekuensi")
                        st.pyplot(plt)
    
                    # Create a line chart using matplotlib
                    with st.expander("Line Chart Data Frekuensi"):
                        plt.figure(figsize=(8, 6))
                        plt.plot(edited_df["Kategori"], edited_df["Frekuensi"], marker='o')
                        plt.xlabel("Kategori")
                        plt.ylabel("Frekuensi")
                        plt.title("Line Chart Data Frekuensi")
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                        st.write(
                            "The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
    
                    # Pie Chart
                    with st.expander("Pie Chart Data Frekuensi"):
                        labels = edited_df["Kategori"]
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
                        st.image(
                            "https://gurubelajarku.com/wp-content/uploads/2019/06/Statistika-Deskriptif-Pie-Chart.jpg",
                            caption="Ilustrasi Statistika", use_column_width=True)
    
                    frekuensi_kumulatif = np.cumsum(edited_df["Frekuensi"])
                    df = edited_df
                    df["Frekuensi Kumulatif"] = frekuensi_kumulatif
                    st.write(df)
    
                else:
                    st.warning("Data kosong atau kolom 'Nilai' belum diisi.")
    
    
    def view_questions():
        st.title("Daftar Soal")
        db = get_db()
        questions_ref = db.collection("question")
        questions = questions_ref.get()
    
        question_data = []
        for question in questions:
            question_dict = question.to_dict()
            question_dict["id"] = question.id  # Simpan ID dokumen dalam dictionary
            question_data.append(question_dict)
    
        for idx, question in enumerate(question_data):
            key = f"radio_{idx + 1}"  # Buat key yang unik berdasarkan indeks
            # Display image from Firebase Storage
            st.write("Pertanyaan:", question["soal"])
            key = f"radio_{idx}"  # Buat key yang unik berdasarkan indekshttps
            st.image(question["foto_url"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            selected_option = st.radio("Pilih Jawaban:", [question["option_A"], question["option_B"], question["option_C"],
                                                          question["option_D"]], key=key)
    
            if st.button(f"Hapus Soal {idx + 1}"):
                # Hapus pertanyaan dari Firebase Firestore berdasarkan ID dokumen
                question_ref = db.collection("question").document(question["id"])
                question_ref.delete()
                st.success("Soal berhasil dihapus!")
    
    
    def exam_ques():
        st.title('Quiz')
    
        db = get_db()
        questions_ref = db.collection("question")
        questions = questions_ref.get()
    
        question_data = []
        for question in questions:
            question_data.append(question.to_dict())
    
        questions_and_answers = []
    
        for idx, question in enumerate(question_data):
            st.write("Pertanyaan:", question["soal"])
            st.image(question["foto_url"], caption=f"Foto Soal {idx + 1}", use_column_width=True)
            key = f"radio_{idx}"  # Buat key yang unik berdasarkan indeks
            selected_option = st.radio("Pilih Jawaban:", [question["option_A"], question["option_B"], question["option_C"],
                                                          question["option_D"]], key=key)
    
            questions_and_answers.append((question, selected_option))
    
        end_button = st.button("Selesai")
        if end_button:
            st.title("Hasil Ujian")
            for idx, (question, selected_option) in enumerate(questions_and_answers):
                if selected_option == question["jawaban"]:
                    st.write(f"Pertanyaan: {idx + 1}")
                    st.success("Benar")
                else:
                    st.error("Salah")
                    st.write("Jawaban yang Benar:", question["jawaban"])
    
    
    def post_materi(db, materi_text, foto_file):
        payload = {
            "soal": materi_text,
            "foto_url": None,
        }
        if uploaded_file is not None:
            # Upload gambar ke Firebase Storage dan dapatkan URL
            # Mengunggah gambar ke Firebase Storage dan dapatkan URL
            blob = bucket.blob("uploads/" + uploaded_file.name)
    
            # Menggunakan BytesIO untuk membaca data gambar
            image_data = uploaded_file.read()
    
            # Mengunggah data gambar ke Firebase Storage
            blob.upload_from_string(image_data, content_type=uploaded_file.type)
            expiration_time = datetime.utcnow() + timedelta(days=3650)  # 10 tahun * 365 hari/tahun
            image_url_with_token = blob.generate_signed_url(expiration=expiration_time)  # URL dengan token akses
    
            payload["foto_url"] = image_url_with_token
        doc_ref = db.collection("postingan").document()
        doc_ref.set(payload)
        return
        with st.form(key="form"):
            st.subheader("Buat Soal Baru")
            uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])
            question_text = st.text_area("Pertanyaan")
    
            if st.form_submit_button("Simpan Soal"):
                db = get_db()
                post_materi(db, materi_text, foto_file)
    
    
    def lesson():
        st.title("Statistika Pada Data Tunggal dan Kelompok")
        st.markdown(f"""
                    Statistika adalah sebuah ilmu atau metode ilmiah yang mempelajari tentang bagaimana merencanakan, mengumpulkan,
                    mengelola, menginterprestasi kemudian menganalisa data untuk kemudian mempresentasikan hasil data yang diperoleh.
                    Sedangkan Menurut Kamus Besar Bahasa Indonesia (KBBI), statistik didefinisikan sebagai angka-angka atau catatan yang dikumpulkan, dikelompokkan
                    dan ditabulasi sehingga didapatkan informasi berkaitan dengan masalah tertentu. \n
    
                    Data adalah himpunan keterangan atau bilangan dari objek yang diamati. Menurut jenisnya, data dibedakan menjadi: \n
                    a. Data Kuantitatif adalah data yang dapat dinyatakan dengan bilangan. Menurut cara mendapatkan data kuantitatif dibagi 2 yaitu: \n
                    ➢ Data Diskrit atau data Data Cacahan: data yang diperolah dengan cara mencacah atau menghitung satu per satu. \n
                    Contoh : \n
                    • Banyaknya wisatawan berkunjung ke bali di bulan ini 600 orang. \n
                    • Satu kilogram telur berisi 16 butir. \n
                    ➢ Data Kontinu atau Data Ukuran atau Data Timbangan: data yang diperoleh dengan cara mengukur atau menimbang dengan alat ukur yang valid. \n
                    Contoh : \n
                    • Berat badan 3 orang wisatawan adalah 45 kg, 50 kg, 53 kg. \n
                    • Diameter pizza = 72,5 mm. \n
    
                    Data Kualitatif adalah data yang tidak dapat dinyatakan dengan bilangan (menyatakan mutu atau kualitas).\n
                    Contoh :\n
                    • Data jenis kelamin.\n
                    • Data makanan kegemaran wisatawan.\n
    
                    Data yang baru dikumpulkan dan belum diolah disebut data mentah.\n
                    Metode pengumpulan data ada 2 yaitu:\n
                    1. Metode Sampling adalah pengumpulan data dengan meneliti sebagian anggota populasi.\n
                    2. Metode Sensus adalah pengumpulan data dengan meneliti semua anggota populasi.\n
                    Adapun cara untuk mengumpulkan data adalah:\n
                    1. Wawancara (Interview).\n
                    2. Angket (Kuesioner).\n
                    3. Pengamatan (Observasi).\n
                    4. Koleksi (data dari media cetak atau elektronik).\n
                    5. Penyajian Data.\n
    
                    Bantuk Tabel atau daftar tabel \n
                    Pada dasarnya ada 3 macam tabel yaitu \n
                    1. Tabel Baris dan Kolom \n
                    contohnya : \n
                    """)
        st.image("assets/image_1.png", caption="Deskripsi Gambar", width=400)
        st.markdown(f""" 
                    2. Tabel Kontigensi \n
                    contohnya : \n
    
        """)
        st.image("assets/image_1.png", caption="Deskripsi Gambar", width=400)
    
    
        st.markdown(
            """
            ---\n
            Referensi \n
            [1] https://insanpelajar.com/statistik-dan-statistika/ \n
            """
        )
    
    def report():
        st.title("Daftar Nilai")
        db = get_db()
        documents_ref = db.collection("nilai")
        documents = documents_ref.stream()
    
        documents_databases = []
        for doc in documents:
            data = doc.to_dict()
            documents_databases.append(data)
    
        # Membuat DataFrame dari data
        df = pd.DataFrame(documents_databases)
        # Tampilkan tabel menggunakan Streamlit
        st.write("Tabel Data dari Firebase Firestore:")
        st.dataframe(df,hide_index=True,width=1000,  height=350)
        csv = df.to_csv().encode('utf-8')
    
        st.download_button(
            label="Download Report",
            data=csv,
            file_name='report.csv',
            mime='text/csv',
        )
    
    
    def login_page():
        username = st.text_input("Username:")
        password = st.text_input("Password: ", type="password")
    
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
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
                with open(file_name) as f :
                    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
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
                # Menambahkan logo perusahaan
                st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
                selected = option_menu(
                    menu_title="Main Menu",
                    options=["Materi", "Latihan", "Quiz", "Tambah Soal", "Daftar Soal", "Nilai Siswa"],
                    icons=["book", "calculator","pen", "clipboard","list","key"],
                    menu_icon="cast",
                    styles={
    
                    }
    
                )
            if selected == "Tambah Soal":
                create_question()
            elif selected == "Quiz":
                exam_ques()
            elif selected == "Latihan":
                home()
            elif selected == "Materi":
                lesson()
            elif selected == "Daftar Soal":
                view_questions()
            elif selected == "Nilai Siswa":
                report()
    
    
            # Display logout button below the page content
            st.button("Logout", on_click=logout)
        else:
            login_page()
    
    if __name__ == "__main__":
        guru()
    
