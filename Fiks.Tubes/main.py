import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

# IMPORT DATA DAN ALGORITMA KAMU
from database_konten import database
import algoritma

# IMPORT DATA AKUN ADMIN (USERNAME & PASSWORD)
from Users import ADMIN_ACCOUNTS

# =========================================================================
#  KONFIGURASI UKURAN RESOLUSI GLOBAL
# =========================================================================
BG_WIDTH = 1000
BG_HEIGHT = 1050

WIN_WIDTH = 1015  
WIN_HEIGHT = 750  

class TampilBackgroundScrollable:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 AI Pembuat Konten - Dashboard Sistem Navigasi")
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.root.resizable(False, True)
        
        # Atur tema Treeview agar gelap senada dengan background mockup
        self.setup_style_tabel()
        
        # 1. Load Gambar Background Utama (.png)
        self.bg_login = self.load_bg("background_login.png")
        self.bg_user = self.load_bg("background_user.png") 
        self.bg_admin = self.load_bg("background_admin.png")
        
        # 2. Load Gambar Tombol Kustom (.png)
        self.img_btn_admin = self.load_icon("button_admin.png", ukuran=(150, 100))
        self.img_btn_user = self.load_icon("button_user.png", ukuran=(150, 100))
        self.img_btn_login = self.load_icon("button_login_user.png", ukuran=(230, 40))
        self.img_btn_sort_real = self.load_icon("button_sort.png", ukuran=(125, 25))
        self.img_btn_reset_real = self.load_icon("button_reset.png", ukuran=(70, 25))
        
        self.img_btn_submit = self.load_icon("button_submit.png", ukuran=(128, 28))
        self.img_btn_delete = self.load_icon("button_delete.png", ukuran=(128, 28))
        
        # --- VARIABEL LOGIKA STATUS (STATE SYSTEM) ---
        self.sudah_login = False    
        self.mode_aktif = "user"    
        
        # Data aktif yang sedang dimanipulasi (Pencarian/Sortir/CRUD)
        self.data_sekarang = database
        
        # 3. Membuat Master Canvas Utama untuk Scrollbar Background
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 4. Buat Frame di dalam Canvas utama untuk menampung halaman aktif
        self.container = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((0, 0), window=self.container, anchor="nw")
        
        self.container.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.root.bind_all("<MouseWheel>", self.jalankan_scroll_global)

        self.root.option_add("*TCombobox*Listbox.background", "#240046") # Background list melorot
        self.root.option_add("*TCombobox*Listbox.foreground", "white")   # Warna font list melorot
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#4613B5") # Warna saat disorot/hover
        self.root.option_add("*TCombobox*Listbox.selectForeground", "white")
        
        # Jalankan Halaman USER Pertama Kali saat Startup
        self.buka_halaman_user()

    def setup_style_tabel(self):
        """Mengatur desain visual tabel Treeview agar bernuansa gelap (Dark Mode)."""
        style = ttk.Style()
        style.theme_use("default")
        
        # Konfigurasi Body Tabel
        style.configure("Treeview",
                        background="#0B071E",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#0B071E",
                        borderwidth=0,
                        relief="flat",
                        font=("Sf Pro Display medium", 10,"normal"))
        
        # Efek saat baris data dipilih/diklik
        style.map("Treeview", background=[("selected", "#3B0066")])
        
        # Konfigurasi Header Tabel
        style.configure("Treeview.Heading",
                        background="#1A1235",
                        foreground="white",
                        font=("Sf Pro Display medium", 10, "normal"),
                        borderwidth=0)
        
        # Mengatur warna dasar Combobox via Ttk Style
        style.configure("TCombobox",
                        fieldbackground="#190E3F",  
                        background="#4613B5",       
                        foreground="white",         
                        arrowcolor="white",         
                        borderwidth=0,
                        relief="flat")
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#190E3F")],
                  foreground=[("readonly", "white")])

    def jalankan_scroll_global(self, e):
        widget_fokus = self.root.winfo_containing(e.x_root, e.y_root)
        if widget_fokus and "treeview" in str(widget_fokus).lower():
            return
        self.main_canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    def load_bg(self, nama_file):
        try:
            folder_aktif = os.path.dirname(os.path.abspath(__file__))
            path_lengkap = os.path.join(folder_aktif, nama_file)
            if not os.path.exists(path_lengkap):
                return None
            img = Image.open(path_lengkap)
            img = img.resize((BG_WIDTH, BG_HEIGHT), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"❌ Gagal load background [{nama_file}]: {e}")
            return None

    def load_icon(self, nama_file, ukuran):
        try:
            folder_aktif = os.path.dirname(os.path.abspath(__file__))
            path_lengkap = os.path.join(folder_aktif, nama_file)
            if not os.path.exists(path_lengkap):
                return None
            img = Image.open(path_lengkap)
            img = img.resize(ukuran, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"❌ Gagal load gambar tombol [{nama_file}]: {e}")
            return None

    def reset_halaman(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.main_canvas.yview_moveto(0)

    # =========================================================================
    #  🛠️ FUNGSI WIDGET TABEL SCROLL TREEVIEW
    # =========================================================================
    def buat_tabel_scroll_konten(self, container_frame, page_canvas, x=30, y=520, width=910, height=360):
        frame_tabel = tk.Frame(container_frame, bg="#0B071E")
        page_canvas.create_window(x, y, window=frame_tabel, anchor="nw", width=width, height=height)
        
        kolom = ("id", "judul", "kategori", "likes", "reposts", "shares", "hashtags")
        tabel = ttk.Treeview(frame_tabel, columns=kolom, show="headings", selectmode="browse")
        
        tabel_scroll = tk.Scrollbar(frame_tabel, orient="vertical", command=tabel.yview)
        tabel_scroll.pack(side="right", fill="y")
        tabel.configure(yscrollcommand=tabel_scroll.set)
        tabel.pack(side="left", fill="both", expand=True)
        
        tabel.heading("id", text="ID")
        tabel.heading("judul", text="Judul Konten")
        tabel.heading("kategori", text="Kategori")
        tabel.heading("likes", text="Likes")
        tabel.heading("reposts", text="Reposts")
        tabel.heading("shares", text="Shares")
        tabel.heading("hashtags", text="Hashtags")
        
        tabel.column("id", width=45, anchor="center")
        tabel.column("judul", width=250, anchor="w")
        tabel.column("kategori", width=95, anchor="center")
        tabel.column("likes", width=75, anchor="center")
        tabel.column("reposts", width=80, anchor="center")
        tabel.column("shares", width=75, anchor="center")
        tabel.column("hashtags", width=260, anchor="w")
        
        return tabel

    def isi_data_ke_tabel(self, tabel, daftar_data):
        tabel.delete(*tabel.get_children())
        for item in daftar_data:
            tabel.insert("", "end", values=(
                item['id'], item['judul'], item['category'],
                item['like'], item['posting_ulang'], item['share'],
                item['hashtags']
            ))

    # =========================================================================
    #  1. LOGIKA HALAMAN GERBANG LOGIN
    # =========================================================================
    def buka_halaman_login(self):
        self.reset_halaman()
        page_canvas = tk.Canvas(self.container, width=BG_WIDTH, height=BG_HEIGHT, highlightthickness=0)
        page_canvas.pack()
        
        if self.bg_login:
            page_canvas.create_image(0, 0, image=self.bg_login, anchor="nw")
            
        entry_user = tk.Entry(self.container, font=("Sf Pro Display medium", 11,"bold"), bd=0, bg="white", fg="black")
        page_canvas.create_window(500, 728, window=entry_user, width=230, height=26)
        
        entry_pass = tk.Entry(self.container, font=("Sf Pro Display medium", 11,"bold"), show="*", bd=0, bg="white", fg="black")
        page_canvas.create_window(500, 775, window=entry_pass, width=230, height=26)

        def proses_masuk_aplikasi():
            u = entry_user.get().strip()
            p = entry_pass.get().strip()
            if u in ADMIN_ACCOUNTS and ADMIN_ACCOUNTS[u] == p:
                messagebox.showinfo("Sukses", "Login Admin Berhasil!")
                self.sudah_login = True  
                self.buka_halaman_admin() 
            else:
                messagebox.showerror("Gagal", "Username atau Password Admin salah!")

        btn_submit = tk.Button(self.container, text="Masuk Admin ➔]", bg="#3B0066", fg="white", 
                               font=("Sf Pro Display medium", 10, "normal"), bd=0, cursor="hand2", command=proses_masuk_aplikasi)
        page_canvas.create_window(500, 835, window=btn_submit, width=230, height=40)

        def aksi_klik_sakelar_login():
            self.mode_aktif = "user"      
            self.buka_halaman_user()      

        gambar_awal = self.img_btn_admin 
        
        self.tombol_sakelar1 = page_canvas.create_image(500, 290, image=gambar_awal, anchor="center")
        page_canvas.tag_bind(self.tombol_sakelar1, "<Button-1>", lambda event: aksi_klik_sakelar_login())
        page_canvas.tag_bind(self.tombol_sakelar1, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
        page_canvas.tag_bind(self.tombol_sakelar1, "<Leave>", lambda event: page_canvas.config(cursor=""))

        self.tombol_sakelar2 = page_canvas.create_image(90, 560, image=gambar_awal, anchor="center")
        page_canvas.tag_bind(self.tombol_sakelar2, "<Button-1>", lambda event: aksi_klik_sakelar_login())
        page_canvas.tag_bind(self.tombol_sakelar2, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
        page_canvas.tag_bind(self.tombol_sakelar2, "<Leave>", lambda event: page_canvas.config(cursor=""))

        if self.img_btn_login:
            self.tombol_login_user = page_canvas.create_image(500, 885, image=self.img_btn_login, anchor="center")
            page_canvas.tag_bind(self.tombol_login_user, "<Button-1>", lambda event: aksi_klik_sakelar_login())
            page_canvas.tag_bind(self.tombol_login_user, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(self.tombol_login_user, "<Leave>", lambda event: page_canvas.config(cursor=""))

    # =========================================================================
    #  2. LOGIKA HALAMAN DASHBOARD USER (EXPLORATION)
    # =========================================================================
    def buka_halaman_user(self):
        self.reset_halaman()
        
        page_canvas = tk.Canvas(self.container, width=BG_WIDTH, height=BG_HEIGHT, highlightthickness=0)
        page_canvas.pack()
        
        if self.bg_user:
            page_canvas.create_image(0, 0, image=self.bg_user, anchor="nw")
            
        tabel_user = self.buat_tabel_scroll_konten(self.container, page_canvas, x=35, y=758, width=910, height=240)
        self.isi_data_ke_tabel(tabel_user, self.data_sekarang)

        entry_cari = tk.Entry(self.container, font=("Sf Pro Display medium", 11,"normal"), bd=0, bg="white", fg="black")
        page_canvas.create_window(160, 700, window=entry_cari, width=250, height=17)
        
        def fungsi_pencarian_realtime(event):
            keyword = entry_cari.get().strip()
            if keyword == "":
                self.data_sekarang = database.copy()
            else:
                self.data_sekarang = algoritma.sequential_search(database, keyword)
            self.isi_data_ke_tabel(tabel_user, self.data_sekarang)
            
        entry_cari.bind("<KeyRelease>", fungsi_pencarian_realtime)

        combo_kat = ttk.Combobox(self.container, values=["Semua Kategori", "tips", "lifestyle", "productivity", "education", "health", "fashion", "finance", "relationship"], state="readonly", font=("Sf Pro Display medium", 8,"normal"))
        combo_kat.set("Semua Kategori")
        page_canvas.create_window(385, 702, window=combo_kat, width=155, height=20)
        
        combo_urut = ttk.Combobox(self.container, values=["Likes", "Reposts", "Shares"], state="readonly", font=("Sf Pro Display medium", 8,"normal"))
        combo_urut.set("Likes")
        page_canvas.create_window(515, 702, window=combo_urut, width=85, height=20)
        
        combo_arah = ttk.Combobox(self.container, values=["Terbesar → Terkecil", "Terkecil → Terbesar"], state="readonly", font=("Sf Pro Display medium", 8,"normal"))
        combo_arah.set("Terbesar → Terkecil")
        page_canvas.create_window(655, 702, window=combo_arah, width=165, height=20)

        def jalankan_proses_sortir():
            kat = combo_kat.get()
            if kat != "Semua Kategori":
                data_filter = algoritma.filter_by_category(database, kat)
            else:
                data_filter = database.copy()
                
            key_map = {"Likes": "like", "Reposts": "posting_ulang", "Shares": "share"}
            sort_key = key_map[combo_urut.get()]
            is_reverse = (combo_arah.get() == "Terbesar → Terkecil")
            
            self.data_sekarang = algoritma.sort_data(data_filter, sort_key, reverse=is_reverse)
            self.isi_data_ke_tabel(tabel_user, self.data_sekarang)

        def jalankan_reset_data():
            entry_cari.delete(0, tk.END)
            combo_kat.set("Semua Kategori")
            combo_urut.set("Likes")
            combo_arah.set("Terbesar → Terkecil")
            self.data_sekarang = database.copy()
            self.isi_data_ke_tabel(tabel_user, self.data_sekarang)

        if self.img_btn_sort_real:
            btn_sort = page_canvas.create_image(810, 700, image=self.img_btn_sort_real, anchor="center")
            page_canvas.tag_bind(btn_sort, "<Button-1>", lambda event: jalankan_proses_sortir())
            page_canvas.tag_bind(btn_sort, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_sort, "<Leave>", lambda event: page_canvas.config(cursor=""))

        if self.img_btn_reset_real:
            btn_reset = page_canvas.create_image(910, 700, image=self.img_btn_reset_real, anchor="center")
            page_canvas.tag_bind(btn_reset, "<Button-1>", lambda event: jalankan_reset_data())
            page_canvas.tag_bind(btn_reset, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_reset, "<Leave>", lambda event: page_canvas.config(cursor=""))

        def navigasi_dari_user():
            if self.sudah_login: self.buka_halaman_admin()
            else: self.mode_aktif = "admin"; self.buka_halaman_login()

        if self.img_btn_user:
            btn_user_nav1 = page_canvas.create_image(500, 290, image=self.img_btn_user, anchor="center")
            page_canvas.tag_bind(btn_user_nav1, "<Button-1>", lambda event: navigasi_dari_user())
            page_canvas.tag_bind(btn_user_nav1, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_user_nav1, "<Leave>", lambda event: page_canvas.config(cursor=""))

            btn_user_nav2 = page_canvas.create_image(90, 560, image=self.img_btn_user, anchor="center")
            page_canvas.tag_bind(btn_user_nav2, "<Button-1>", lambda event: navigasi_dari_user())
            page_canvas.tag_bind(btn_user_nav2, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_user_nav2, "<Leave>", lambda event: page_canvas.config(cursor=""))

    # =========================================================================
    #  3. LOGIKA HALAMAN DASHBOARD ADMIN (DI-REAKTIFKAN PENUH DENGAN MODEL CLASS)
    # =========================================================================
    def buka_halaman_admin(self):
        self.reset_halaman()
        page_canvas = tk.Canvas(self.container, width=BG_WIDTH, height=BG_HEIGHT, highlightthickness=0)
        page_canvas.pack()
        
        if self.bg_admin:
            page_canvas.create_image(0, 0, image=self.bg_admin, anchor="nw")

        # =====================================================================
        # 🟢 A. FORM TAMBAH KONTEN / INSERT (SISI KIRI MOCKUP)
        # =====================================================================
        judul_var   = tk.StringVar()
        kat_var2    = tk.StringVar(value="tips")
        like_var    = tk.IntVar(value=0)
        share_var   = tk.IntVar(value=0)
        repost_var  = tk.IntVar(value=0)
        tag_var     = tk.StringVar(value="#explorepage")
        cap_var     = tk.StringVar()

        entry_add_judul = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=judul_var)
        page_canvas.create_window(180, 744, window=entry_add_judul, width=120, height=18)

        combo_add_kat = ttk.Combobox(self.container, textvariable=kat_var2, state="readonly", font=("Sf Pro Display medium", 10,"normal"),
                                     values=["tips", "lifestyle", "productivity", "education", "health", "fashion", "finance", "relationship"])
        page_canvas.create_window(390, 744, window=combo_add_kat, width=130, height=18)

        entry_add_likes = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=like_var)
        page_canvas.create_window(135, 787, window=entry_add_likes, width=50, height=18)

        entry_add_shares = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=share_var)
        page_canvas.create_window(278, 787, window=entry_add_shares, width=50, height=18)

        entry_add_reposts = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white", textvariable=repost_var)
        page_canvas.create_window(425, 787, window=entry_add_reposts, width=50, height=18)

        entry_add_tags = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="white", fg="black",  textvariable=tag_var)
        page_canvas.create_window(290, 827, window=entry_add_tags, width=310, height=18)

        entry_add_caption = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="white", fg="black",  textvariable=cap_var)
        page_canvas.create_window(285, 880, window=entry_add_caption, width=310, height=40)

        def simpan_konten_baru():
            if not_judul_var := judul_var.get().strip():
                pass
            else:
                messagebox.showerror("Gagal", "Judul tidak boleh kosong!")
                return
            try:
                item_baru = {
                    "judul": judul_var.get().strip(), "category": kat_var2.get(),
                    "like": int(like_var.get()), "share": int(share_var.get()),
                    "posting_ulang": int(repost_var.get()),
                    "hashtags": tag_var.get().strip(), "caption": cap_var.get().strip()
                }
                algoritma.insert_content(self.data_sekarang, item_baru)
                refresh_id_dropdown()
                
                judul_var.set("")
                cap_var.set("")
                like_var.set(0); share_var.set(0); repost_var.set(0)
                messagebox.showinfo("Sukses", "Konten baru berhasil ditambahkan!")
            except ValueError:
                messagebox.showerror("Error", "Likes, Shares, dan Reposts harus berupa angka!")

        if self.img_btn_submit:
            btn_add_save = page_canvas.create_image(253, 940, image=self.img_btn_submit, anchor="center")
            page_canvas.tag_bind(btn_add_save, "<Button-1>", lambda event: simpan_konten_baru())
            page_canvas.tag_bind(btn_add_save, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_add_save, "<Leave>", lambda event: page_canvas.config(cursor=""))

        # =====================================================================
        # 🔵 B. FORM EDIT & HAPUS / UPDATE & DELETE (SISI KANAN MOCKUP)
        # =====================================================================
        id_target_var = tk.StringVar()

        cb_id = ttk.Combobox(self.container, textvariable=id_target_var, state="readonly", font=("Segoe UI", 10))
        page_canvas.create_window(740, 708, window=cb_id, width=400, height=24)

        def refresh_id_dropdown():
            cb_id["values"] = [str(item['id']) for item in self.data_sekarang]

        refresh_id_dropdown()

        judul_edit_var  = tk.StringVar()
        kat_edit_var    = tk.StringVar()
        like_edit_var   = tk.IntVar()
        share_edit_var  = tk.IntVar()
        repost_edit_var = tk.IntVar()
        tag_edit_var    = tk.StringVar()
        cap_edit_var    = tk.StringVar()

        # Mengubah bg menjadi ungu gelap (#190E3F) dan fg menjadi putih (white)
        entry_edit_judul = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=judul_edit_var)
        page_canvas.create_window(650, 745, window=entry_edit_judul, width=120, height=18)

        combo_edit_kat = ttk.Combobox(self.container, textvariable=kat_edit_var, state="readonly", font=("Sf Pro Display medium", 10,"normal"),
                                      values=["tips", "lifestyle", "productivity", "education", "health", "fashion", "finance", "relationship"])
        page_canvas.create_window(860, 745, window=combo_edit_kat, width=130, height=18)

        entry_edit_likes = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=like_edit_var)
        page_canvas.create_window(615, 787, window=entry_edit_likes, width=50, height=18)

        entry_edit_shares = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white",  textvariable=share_edit_var)
        page_canvas.create_window(753, 787, window=entry_edit_shares, width=50, height=18)

        entry_edit_reposts = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="#190E3F", fg="white", textvariable=repost_edit_var)
        page_canvas.create_window(900, 787, window=entry_edit_reposts, width=50, height=18)

        entry_edit_tags = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="white", fg="black",  textvariable=tag_edit_var)
        page_canvas.create_window(770, 827, window=entry_edit_tags, width=310, height=18)

        entry_edit_caption = tk.Entry(self.container, font=("Sf Pro Display medium", 10,"normal"), bd=0, bg="white", fg="black",  textvariable=cap_edit_var)
        page_canvas.create_window(770, 880, window=entry_edit_caption, width=310, height=40)

        def load_data_ke_form(*args):
            id_str = id_target_var.get()
            if not id_str:
                return
            idx = algoritma.find_index_by_id(self.data_sekarang, int(id_str))
            if idx == -1:
                return
            d = self.data_sekarang[idx]
            judul_edit_var.set(d['judul'])
            kat_edit_var.set(d['category'])
            like_edit_var.set(d['like'])
            share_edit_var.set(d['share'])
            repost_edit_var.set(d['posting_ulang'])
            cap_edit_var.set(d.get('caption', ''))
            tag_edit_var.set(d['hashtags'])

        cb_id.bind("<<ComboboxSelected>>", load_data_ke_form)

        def simpan_edit():
            id_str = id_target_var.get()
            if not id_str:
                messagebox.showwarning("Peringatan", "Pilih ID terlebih dahulu!")
                return
            try:
                dict_update = {
                    "judul": judul_edit_var.get().strip(), "category": kat_edit_var.get(),
                    "like": int(like_edit_var.get()), "share": int(share_edit_var.get()),
                    "posting_ulang": int(repost_edit_var.get()),
                    "hashtags": tag_edit_var.get().strip(), "caption": cap_edit_var.get().strip()
                }
                algoritma.update_content(self.data_sekarang, int(id_str), dict_update)
                messagebox.showinfo("Sukses", f"Data ID {id_str} berhasil diperbarui!")
            except ValueError:
                messagebox.showerror("Error", "Format input angka tidak valid!")

        def hapus_konten():
            id_str = id_target_var.get()
            if not id_str:
                messagebox.showwarning("Peringatan", "Pilih ID terlebih dahulu!")
                return
            if messagebox.askyesno("Konfirmasi Hapus", f"Yakin hapus konten ID {id_str}?"):
                algoritma.delete_content(self.data_sekarang, int(id_str))
                refresh_id_dropdown()
                id_target_var.set("")
                
                judul_edit_var.set(""); kat_edit_var.set("")
                like_edit_var.set(0); share_edit_var.set(0); repost_edit_var.set(0)
                tag_edit_var.set(""); cap_edit_var.set("")
                messagebox.showinfo("Terhapus", f"Konten ID {id_str} berhasil dihapus.")

        if self.img_btn_submit:
            btn_edit_save = page_canvas.create_image(665, 940, image=self.img_btn_submit, anchor="center")
            page_canvas.tag_bind(btn_edit_save, "<Button-1>", lambda event: simpan_edit())
            page_canvas.tag_bind(btn_edit_save, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_edit_save, "<Leave>", lambda event: page_canvas.config(cursor=""))

        if self.img_btn_delete:
            btn_edit_delete = page_canvas.create_image(812, 940, image=self.img_btn_delete, anchor="center")
            page_canvas.tag_bind(btn_edit_delete, "<Button-1>", lambda event: hapus_konten())
            page_canvas.tag_bind(btn_edit_delete, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_edit_delete, "<Leave>", lambda event: page_canvas.config(cursor=""))

        # =====================================================================
        # 🔄 C. NAVIGATION BUTTONS (BACK BOLAK-BALIK HALAMAN)
        # =====================================================================
        def navigasi_dari_admin():
            if self.sudah_login: self.buka_halaman_user()
            else: self.buka_halaman_login()   
            
        if self.img_btn_admin:
            btn_admin_nav1 = page_canvas.create_image(500, 290, image=self.img_btn_admin, anchor="center")
            page_canvas.tag_bind(btn_admin_nav1, "<Button-1>", lambda event: navigasi_dari_admin())
            page_canvas.tag_bind(btn_admin_nav1, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_admin_nav1, "<Leave>", lambda event: page_canvas.config(cursor=""))

            btn_admin_nav2 = page_canvas.create_image(90, 560, image=self.img_btn_admin, anchor="center")
            page_canvas.tag_bind(btn_admin_nav2, "<Button-1>", lambda event: navigasi_dari_admin())
            page_canvas.tag_bind(btn_admin_nav2, "<Enter>", lambda event: page_canvas.config(cursor="hand2"))
            page_canvas.tag_bind(btn_admin_nav2, "<Leave>", lambda event: page_canvas.config(cursor=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = TampilBackgroundScrollable(root)
    root.mainloop()
