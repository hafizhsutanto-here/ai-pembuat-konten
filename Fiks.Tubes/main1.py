import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import StringVar, IntVar
import tkinter as tk

from database_konten import database as konten
import algoritma as alg

# =========================================================================
#   IN-MEMORY STORAGE
# =========================================================================
data_kerja = konten.copy()

# =========================================================================
#   SETUP WINDOW UTAMA
# =========================================================================
app = ttk.Window(themename="cosmo")
app.title("🎬 AI Pembuat Konten - Dashboard Tugas Besar")
app.geometry("1100x700")

# =========================================================================
#   HELPER: Tampilkan data ke Treeview
# =========================================================================
def render_tabel(tree, data):
    """Hapus isi tabel lama lalu isi ulang dengan data baru."""
    tree.delete(*tree.get_children())
    for item in data:
        tree.insert("", END, values=(
            item.get('id', ''),
            item.get('judul', ''),
            item.get('category', ''),
            item.get('like', 0),
            item.get('posting_ulang', 0),
            item.get('share', 0),
            item.get('hashtags', ''),
        ))

def buat_treeview(parent):
    """Buat Treeview dengan kolom standar + scrollbar."""
    kolom = ("ID", "Judul", "Kategori", "Like", "Repost", "Share", "Hashtags")
    frame = ttk.Frame(parent)
    frame.pack(fill=BOTH, expand=YES, pady=5)

    tree = ttk.Treeview(frame, columns=kolom, show="headings", bootstyle="info")
    lebar = [40, 280, 100, 60, 60, 60, 260]
    for col, w in zip(kolom, lebar):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor=CENTER if w < 150 else W)

    sb = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side=LEFT, fill=BOTH, expand=YES)
    sb.pack(side=RIGHT, fill=Y)
    return tree

# =========================================================================
#   SIDEBAR KIRI (Navigasi Mode)
# =========================================================================
sidebar = ttk.Frame(app, bootstyle="dark", width=200)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

ttk.Label(sidebar, text="🎬 AI Konten", font=("Helvetica", 13, "bold"),
          bootstyle="inverse-dark").pack(pady=(20, 5), padx=10)
ttk.Label(sidebar, text="Dashboard Tugas Besar", font=("Helvetica", 8),
          bootstyle="inverse-dark").pack(padx=10)
ttk.Separator(sidebar, bootstyle="secondary").pack(fill=X, pady=15, padx=10)

ttk.Label(sidebar, text="🌐 PILIH MODE AKSES:", font=("Helvetica", 9, "bold"),
          bootstyle="inverse-dark").pack(padx=10, anchor=W)

mode_var = StringVar(value="user")

ttk.Radiobutton(sidebar, text="👤 User Mode", variable=mode_var,
                value="user", bootstyle="light").pack(anchor=W, padx=20, pady=3)
ttk.Radiobutton(sidebar, text="🛠️ Admin Mode", variable=mode_var,
                value="admin", bootstyle="light").pack(anchor=W, padx=20, pady=3)

ttk.Separator(sidebar, bootstyle="secondary").pack(fill=X, pady=15, padx=10)
ttk.Label(sidebar, text="💡 Tips: Restart app\nuntuk reset data\nke kondisi awal.",
          font=("Helvetica", 8), bootstyle="inverse-dark", justify=LEFT).pack(padx=12)

# =========================================================================
#   AREA KONTEN KANAN (Notebook/Tab per Mode)
# =========================================================================
main_frame = ttk.Frame(app)
main_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)

# --- Judul Atas ---
ttk.Label(main_frame, text="🎬 AI Pembuat Konten - Dashboard Tugas Besar",
          font=("Helvetica", 14, "bold")).pack(anchor=W)
ttk.Label(main_frame, text="Aplikasi manajemen dan analisis ide konten menggunakan struktur data modular.",
          font=("Helvetica", 9), bootstyle="secondary").pack(anchor=W)
ttk.Separator(main_frame).pack(fill=X, pady=8)

# Frame kontainer yang akan diganti saat mode berubah
content_frame = ttk.Frame(main_frame)
content_frame.pack(fill=BOTH, expand=YES)


# =========================================================================
#   MODE USER
# =========================================================================
def tampilkan_mode_user():
    for w in content_frame.winfo_children():
        w.destroy()

    ttk.Label(content_frame, text="🔍 Ruang Eksplorasi Ide Konten",
              font=("Helvetica", 12, "bold")).pack(anchor=W, pady=(0, 8))

    # --- Filter Kategori ---
    frame_filter = ttk.LabelFrame(content_frame, text="🎯 Filter Berdasarkan Kategori")
    frame_filter.pack(fill=X, pady=5)

    kat_var = StringVar(value="Semua Kategori")
    kategori_list = ["Semua Kategori","lifestyle", "relationship", "tips", "technology", "fashion", "education", "productivity", "finance", "health"]

    row_kat = ttk.Frame(frame_filter)
    row_kat.pack(fill=X, padx=10, pady=8)
    ttk.Label(row_kat, text="Pilih Kategori:").pack(side=LEFT)
    cb_kat = ttk.Combobox(row_kat, textvariable=kat_var, values=kategori_list,
                          state="readonly", width=20)
    cb_kat.pack(side=LEFT, padx=8)

    lbl_caption = ttk.Label(frame_filter, text="", bootstyle="secondary", font=("Helvetica", 8))
    lbl_caption.pack(anchor=W, padx=10, pady=(0, 5))

    # --- Pencarian ---
    frame_cari = ttk.LabelFrame(content_frame, text="🔎 Pencarian Pintar (Sequential Search)")
    frame_cari.pack(fill=X, pady=5)

    row_cari = ttk.Frame(frame_cari)
    row_cari.pack(fill=X, padx=10, pady=8)
    ttk.Label(row_cari, text="Kata Kunci:").pack(side=LEFT)
    keyword_var = StringVar()
    entry_cari = ttk.Entry(row_cari, textvariable=keyword_var, width=40)
    entry_cari.pack(side=LEFT, padx=8)
    ttk.Label(row_cari, text="(Gunakan '#' untuk cari hashtag)",
              bootstyle="secondary", font=("Helvetica", 8)).pack(side=LEFT)

    # --- Sorting ---
    frame_sort = ttk.LabelFrame(content_frame, text="📊 Urutkan Konten Terpopuler")
    frame_sort.pack(fill=X, pady=5)

    row_sort = ttk.Frame(frame_sort)
    row_sort.pack(fill=X, padx=10, pady=8)
    ttk.Label(row_sort, text="Urutkan berdasarkan:").pack(side=LEFT)
    kriteria_var = StringVar(value="like")
    cb_kriteria = ttk.Combobox(row_sort, textvariable=kriteria_var,
                               values=["like", "share", "posting_ulang"],
                               state="readonly", width=15)
    cb_kriteria.pack(side=LEFT, padx=8)

    urutan_var = StringVar(value="Terbesar ke Terkecil")
    cb_urutan = ttk.Combobox(row_sort, textvariable=urutan_var,
                             values=["Terbesar ke Terkecil (Paling Viral)", "Terkecil ke Terbesar"],
                             state="readonly", width=28)
    cb_urutan.pack(side=LEFT, padx=8)

    btn_sort = ttk.Button(row_sort, text="🚀 Jalankan Sort", bootstyle="primary")
    btn_sort.pack(side=LEFT, padx=8)

    # --- Treeview Hasil ---
    tree = buat_treeview(content_frame)

    def get_data_filtered():
        kat = kat_var.get()
        if kat == "Semua Kategori":
            return data_kerja
        return alg.filter_by_category(data_kerja, kat)

    def refresh_tampilan(*args):
        data_f = get_data_filtered()
        kw = keyword_var.get().strip()
        lbl_caption.config(text=f"Menampilkan {len(data_f)} konten di kategori '{kat_var.get()}'")
        if kw:
            hasil = alg.sequential_search(data_f, kw)
            render_tabel(tree, hasil)
            if not hasil:
                Messagebox.show_warning("Konten tidak ditemukan. Coba kata kunci lain!", title="Tidak Ditemukan")
        else:
            render_tabel(tree, data_f)

    def jalankan_sort():
        data_f = get_data_filtered()
        reverse_val = "Terbesar" in urutan_var.get()
        hasil = alg.selection_sort(data_f, kriteria_var.get(), reverse=reverse_val)
        render_tabel(tree, hasil)

    cb_kat.bind("<<ComboboxSelected>>", refresh_tampilan)
    entry_cari.bind("<KeyRelease>", refresh_tampilan)
    btn_sort.config(command=jalankan_sort)

    refresh_tampilan()


# =========================================================================
#   MODE ADMIN
# =========================================================================
def tampilkan_mode_admin():
    for w in content_frame.winfo_children():
        w.destroy()

    ttk.Label(content_frame, text="🛠️ Panel Kontrol Admin (Manajemen Data)",
              font=("Helvetica", 12, "bold")).pack(anchor=W, pady=(0, 8))

    # --- Tabel Database Utama ---
    frame_db = ttk.LabelFrame(content_frame, text="📊 Database Utama Saat Ini")
    frame_db.pack(fill=BOTH, expand=YES, pady=5)
    tree_admin = buat_treeview(frame_db)
    render_tabel(tree_admin, data_kerja)

    ttk.Separator(content_frame).pack(fill=X, pady=8)

    # 2 Kolom bawah: Insert | Update/Delete
    frame_bawah = ttk.Frame(content_frame)
    frame_bawah.pack(fill=X)

    kolom_kiri = ttk.LabelFrame(frame_bawah, text="➕ Tambah Konten Baru")
    kolom_kiri.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))

    kolom_kanan = ttk.LabelFrame(frame_bawah, text="📝 Edit / 🗑️ Hapus Konten")
    kolom_kanan.pack(side=LEFT, fill=BOTH, expand=YES, padx=(5, 0))

    # --- KOLOM KIRI: INSERT ---
    def buat_row(parent, label, widget_fn, **kw):
        f = ttk.Frame(parent)
        f.pack(fill=X, padx=8, pady=3)
        ttk.Label(f, text=label, width=12, anchor=E).pack(side=LEFT)
        w = widget_fn(f, **kw)
        w.pack(side=LEFT, fill=X, expand=YES, padx=(5, 0))
        return w

    judul_var   = StringVar()
    kat_var2    = StringVar(value="kesehatan")
    like_var    = IntVar(value=0)
    share_var   = IntVar(value=0)
    repost_var  = IntVar(value=0)
    tag_var     = StringVar(value="#explorepage")
    cap_var     = StringVar()

    buat_row(kolom_kiri, "Judul:", ttk.Entry, textvariable=judul_var)
    buat_row(kolom_kiri, "Kategori:", ttk.Combobox,
             textvariable=kat_var2, state="readonly",
             values=["kesehatan", "perkuliahan", "keuangan", "lifestyle",
                     "relationship", "tips", "productivity"])
    buat_row(kolom_kiri, "Likes:", ttk.Entry, textvariable=like_var)
    buat_row(kolom_kiri, "Shares:", ttk.Entry, textvariable=share_var)
    buat_row(kolom_kiri, "Reposts:", ttk.Entry, textvariable=repost_var)
    buat_row(kolom_kiri, "Hashtags:", ttk.Entry, textvariable=tag_var)
    buat_row(kolom_kiri, "Caption:", ttk.Entry, textvariable=cap_var)

    def simpan_konten_baru():
        if not judul_var.get().strip():
            Messagebox.show_error("Judul tidak boleh kosong!", title="Gagal")
            return
        item_baru = {
            "judul": judul_var.get(), "category": kat_var2.get(),
            "like": like_var.get(), "share": share_var.get(),
            "posting_ulang": repost_var.get(),
            "hashtags": tag_var.get(), "caption": cap_var.get()
        }
        alg.insert_content(data_kerja, item_baru)
        render_tabel(tree_admin, data_kerja)
        refresh_id_dropdown()
        judul_var.set("")
        cap_var.set("")
        Messagebox.show_info("Konten baru berhasil ditambahkan!", title="Sukses")

    ttk.Button(kolom_kiri, text="💾 Simpan Konten Baru",
               bootstyle="success", command=simpan_konten_baru).pack(pady=8)

    # --- KOLOM KANAN: UPDATE / DELETE ---
    id_target_var = StringVar()

    f_id = ttk.Frame(kolom_kanan)
    f_id.pack(fill=X, padx=8, pady=5)
    ttk.Label(f_id, text="Pilih ID:", width=12, anchor=E).pack(side=LEFT)
    cb_id = ttk.Combobox(f_id, textvariable=id_target_var, state="readonly", width=10)
    cb_id.pack(side=LEFT, padx=5)

    def refresh_id_dropdown():
        cb_id["values"] = [str(item['id']) for item in data_kerja]

    refresh_id_dropdown()

    # Field edit
    judul_edit_var  = StringVar()
    kat_edit_var    = StringVar()
    like_edit_var   = IntVar()
    share_edit_var  = IntVar()
    repost_edit_var = IntVar()
    tag_edit_var    = StringVar()
    cap_edit_var    = StringVar()

    buat_row(kolom_kanan, "Judul:", ttk.Entry, textvariable=judul_edit_var)
    buat_row(kolom_kanan, "Kategori:", ttk.Combobox,
             textvariable=kat_edit_var, state="readonly",
             values=["kesehatan", "perkuliahan", "keuangan", "lifestyle",
                     "relationship", "tips", "productivity"])
    buat_row(kolom_kanan, "Likes:", ttk.Entry, textvariable=like_edit_var)
    buat_row(kolom_kanan, "Shares:", ttk.Entry, textvariable=share_edit_var)
    buat_row(kolom_kanan, "Reposts:", ttk.Entry, textvariable=repost_edit_var)
    buat_row(kolom_kanan, "Hashtags:", ttk.Entry, textvariable=tag_edit_var)
    buat_row(kolom_kanan, "Caption:", ttk.Entry, textvariable=cap_edit_var)

    def load_data_ke_form(*args):
        id_str = id_target_var.get()
        if not id_str:
            return
        idx = alg.find_index_by_id(data_kerja, int(id_str))
        if idx == -1:
            return
        d = data_kerja[idx]
        judul_edit_var.set(d['judul'])
        kat_edit_var.set(d['category'])
        like_edit_var.set(d['like'])
        share_edit_var.set(d['share'])
        repost_edit_var.set(d['posting_ulang'])
        tag_edit_var.set(d['hashtags'])
        cap_edit_var.set(d.get('caption', ''))

    cb_id.bind("<<ComboboxSelected>>", load_data_ke_form)

    def simpan_edit():
        id_str = id_target_var.get()
        if not id_str:
            Messagebox.show_warning("Pilih ID terlebih dahulu!", title="Peringatan")
            return
        dict_update = {
            "judul": judul_edit_var.get(), "category": kat_edit_var.get(),
            "like": like_edit_var.get(), "share": share_edit_var.get(),
            "posting_ulang": repost_edit_var.get(),
            "hashtags": tag_edit_var.get(), "caption": cap_edit_var.get()
        }
        alg.update_content(data_kerja, int(id_str), dict_update)
        render_tabel(tree_admin, data_kerja)
        Messagebox.show_info(f"Data ID {id_str} berhasil diperbarui!", title="Sukses")

    def hapus_konten():
        id_str = id_target_var.get()
        if not id_str:
            Messagebox.show_warning("Pilih ID terlebih dahulu!", title="Peringatan")
            return
        konfirmasi = Messagebox.yesno(f"Yakin hapus konten ID {id_str}?", title="Konfirmasi Hapus")
        if konfirmasi == "Yes":
            alg.delete_content(data_kerja, int(id_str))
            render_tabel(tree_admin, data_kerja)
            refresh_id_dropdown()
            id_target_var.set("")
            Messagebox.show_info(f"Konten ID {id_str} berhasil dihapus.", title="Terhapus")

    frame_btn = ttk.Frame(kolom_kanan)
    frame_btn.pack(pady=8)
    ttk.Button(frame_btn, text="💾 Simpan Perubahan",
               bootstyle="warning", command=simpan_edit).pack(side=LEFT, padx=5)
    ttk.Button(frame_btn, text="❌ Hapus Konten",
               bootstyle="danger", command=hapus_konten).pack(side=LEFT, padx=5)


# =========================================================================
#   SWITCH MODE (Radiobutton)
# =========================================================================
def on_mode_change(*args):
    if mode_var.get() == "user":
        tampilkan_mode_user()
    else:
        tampilkan_mode_admin()

mode_var.trace_add("write", on_mode_change)

# Tampilkan mode awal
tampilkan_mode_user()

app.mainloop()