# Facade-Labs

Selamat datang di **Facade-Labs**, sebuah platform simulasi keamanan web yang dirancang untuk mengasah kemampuan Anda dalam mendeteksi dan mengeksploitasi kerentanan *Insecure Direct Object Reference* (IDOR).

Platform ini berisi **15 skenario** yang beragam, mulai dari tingkat dasar hingga pakar, mencakup berbagai vektor serangan yang ditemukan di aplikasi web modern. Dibuat oleh **ThisOchi**.

## Fitur Utama

* **15 Skenario IDOR:** Mencakup berbagai sistem, dari ID numerik klasik hingga manipulasi JWT dan Mass Assignment.
* **3 Tingkat Kesulitan:** Skenario dibagi menjadi *Foundation*, *Advanced*, dan *Expert Tier* untuk pembelajaran yang terstruktur.
* **Antarmuka Profesional:** Desain yang bersih dan modern untuk pengalaman belajar yang fokus.
* **Dukungan Docker:** Jalankan seluruh lab dengan dua perintah sederhana menggunakan Docker.

---

## Pemasangan (Installation)

Ada dua cara untuk menjalankan Facade-Labs di komputer Anda. Metode menggunakan **Docker adalah yang paling direkomendasikan** karena lebih mudah dan cepat.

### Metode 1: Menggunakan Docker (Direkomendasikan)

Metode ini membungkus seluruh aplikasi ke dalam sebuah kontainer, sehingga Anda tidak perlu menginstal Python atau library lainnya secara manual.

#### **Prasyarat:**
* [Git](https://git-scm.com/) terinstal.
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) terinstal dan berjalan.

#### **Langkah-langkah:**

1.  **Clone Repository Ini**
    Buka terminal atau Git Bash dan jalankan perintah berikut:
    ```bash
    git clone https://github.com/OchiWebs/Facade-Labs.git
    cd facade-labs
    ```

2.  **Build Docker Image**
    Perintah ini akan membaca `Dockerfile` dan membangun image yang berisi semua kebutuhan aplikasi.
    ```bash
    docker build -t facade-labs .
    ```

3.  **Jalankan Docker Container**
    Setelah image selesai dibuat, jalankan sebagai kontainer:
    ```bash
    docker run -p 80:5000 -d --name facade-container facade-labs
    ```
    * `-p 80:5000`: Meneruskan lalu lintas dari port 80 di komputer Anda ke port 5000 di dalam kontainer.
    * `-d`: Menjalankan kontainer di latar belakang.

4.  **Akses Labs**
    Buka browser Anda dan kunjungi **http://localhost**. Platform Facade-Labs siap digunakan! 

---

### Metode 2: Pemasangan Manual (Tanpa Docker)

Gunakan metode ini jika Anda tidak ingin atau tidak bisa menggunakan Docker.

#### **Prasyarat:**
* [Git](https://git-scm.com/) terinstal.
* [Python 3.7+](https://www.python.org/downloads/) terinstal.

#### **Langkah-langkah:**

1.  **Clone Repository Ini**
    ```bash
    git clone https://github.com/OchiWebs/Facade-Labs.git
    cd facade-labs
    ```

2.  **(Opsional) Buat Virtual Environment**
    Ini adalah praktik terbaik untuk menjaga dependensi proyek tetap terisolasi.
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **Instal Dependensi Python**
    Perintah ini akan menginstal Flask dan PyJWT dari file `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Flask**
    Pastikan Anda sudah melakukan perubahan `host='0.0.0.0'` pada `app.py` jika ingin diakses dari jaringan lain. Untuk penggunaan lokal, `localhost` sudah cukup.
    ```bash
    python app.py
    ```

5.  **Akses Labs**
    Buka browser Anda dan kunjungi alamat yang muncul di terminal, biasanya **http://127.0.0.1:5000**. Platform Facade-Labs siap digunakan! 

---

## Ringkasan Skenario Simulasi

| Tier        | ID      | Nama Skenario              | Vektor Utama                      |
|-------------|---------|----------------------------|-----------------------------------|
| **Foundation** | S-01    | Numeric IDOR               | URL Path (Angka)                  |
|             | S-02    | UUID IDOR                  | URL Path (UUID)                   |
|             | S-03    | Query Parameter IDOR       | URL Query String                  |
|             | S-04    | API Endpoint IDOR          | API Response (JSON)               |
|             | S-05    | Base64 Encoded IDOR        | Encoding Lemah                    |
| **Advanced** | S-06    | POST Body IDOR             | Request Body (JSON)               |
|             | S-07    | Filename IDOR              | Tebakan Nama File                 |
|             | S-08    | Blind Action IDOR          | Aksi Tanpa Feedback               |
|             | S-09    | Secondary Parameter IDOR   | Parameter Filter                  |
|             | S-10    | Custom HTTP Header IDOR    | Header Non-Standar                |
| **Expert** | S-11    | Multi-Step IDOR            | Rantai Request Logis              |
|             | S-12    | JWT Payload IDOR           | Manipulasi Token                  |
|             | S-13    | Predictable Hash IDOR      | Replikasi Algoritma Hash          |
|             | S-14    | Mass Assignment IDOR       | Injeksi Field JSON                |
|             | S-15    | Wildcard API IDOR          | Endpoint API Tidak Terdokumentasi |

---

Dibuat dengan semangat berbagi oleh **ThisOchi**.
