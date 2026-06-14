# 🎬 AI Pembuat Konten — Dashboard Sistem Navigasi

Aplikasi desktop berbasis Python dan Tkinter untuk mengelola dan mengeksplorasi database ide konten media sosial. Dilengkapi fitur pencarian, filter, sorting, serta panel admin untuk manajemen data (CRUD).

---

## 📋 Fitur

- **Halaman User** — Jelajahi konten, cari berdasarkan judul atau hashtag, filter per kategori, dan urutkan berdasarkan Likes / Shares / Reposts
- **Halaman Admin** — Tambah, edit, dan hapus konten (memerlukan login)
- **Pencarian Real-time** — Menggunakan algoritma Sequential Search
- **Sorting Cerdas** — Ascending menggunakan Selection Sort, Descending menggunakan Insertion Sort
- **Login Admin** — Sistem autentikasi berbasis username & password
- **UI Kustom** — Background dan tombol berbasis gambar PNG dengan tema gelap (dark mode)

---

## 🗂️ Struktur File

```
├── main.py              # File utama, menjalankan seluruh UI (Tkinter)
├── algoritma.py         # Kumpulan algoritma: search, sort, filter, CRUD
├── database_konten.py   # Database konten dalam format list of dict
├── Users.py             # Data akun admin (username & password)
├── requirements.txt     # Daftar library yang dibutuhkan
│
├── background_login.png
├── background_user.png
├── background_admin.png
├── button_admin.png
├── button_user.png
├── button_login_user.png
├── button_sort.png
├── button_reset.png
├── button_submit.png
└── button_delete.png
```

---

## ⚙️ Instalasi

**1. Pastikan Python sudah terinstall**
Gunakan Python versi 3.8 ke atas. Cek dengan:
```bash
python --version
```

**2. Install library yang dibutuhkan**
```bash
pip install -r requirements.txt
```

---

## ▶️ Cara Menjalankan

```bash
python main.py
```

---

## 🔐 Akun Admin

| Username     | Password     |
|--------------|--------------|
| `admin`      | `admin123`   |
| `superadmin` | `rahasia456` |

---

## 🧠 Algoritma yang Digunakan

| Algoritma          | Digunakan Untuk                                      |
|--------------------|------------------------------------------------------|
| Sequential Search  | Pencarian konten berdasarkan judul atau hashtag      |
| Binary Search      | Pencarian konten berdasarkan ID (data terurut)       |
| Selection Sort     | Mengurutkan data secara **ascending** (Terkecil → Terbesar) |
| Insertion Sort     | Mengurutkan data secara **descending** (Terbesar → Terkecil) |
| Filter Kategori    | Menyaring konten berdasarkan kategori                |

---

## 📦 Kategori Konten

`tips` · `lifestyle` · `productivity` · `education` · `health` · `fashion` · `finance` · `relationship` · `technology`

---

## 🛠️ Teknologi

- **Python 3**
- **Tkinter** — GUI framework bawaan Python
- **Pillow (PIL)** — untuk load dan resize gambar PNG
