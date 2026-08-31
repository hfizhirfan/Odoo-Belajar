# Odoo Custom Addons & Learning Portfolio

Repository ini berisi kumpulan modul kustom (*custom addons*) Odoo v17 yang dikembangkan untuk pembelajaran dan simulasi kasus industri ERP nyata.

---

## 📦 Daftar Modul Kustom (`custom_addons/`)

### 1. `ksi_service_center` (Service Center & Warranty Management)
Modul simulasi untuk manajemen perbaikan perangkat keras & klaim garansi (studi kasus IT Solution / Partner Axioo):
- **Master Perangkat:** Katalog model laptop & masa garansi default.
- **Tiket Servis:** Penomoran otomatis (`ir.sequence`), tracking nomor seri (SN), dan penghitungan masa garansi otomatis.
- **Suku Cadang & Biaya:** Penggantian spare parts (`One2many`), kalkulasi subtotal, dan perhitungan biaya akhir otomatis.
- **Alur Kerja (Workflow):** Statusbar tiket (*Draft* -> *In Progress* -> *Waiting Parts* -> *Done* -> *Delivered*).
- **Validasi Bisnis:** Validasi pengisian hasil diagnosa teknisi sebelum tiket diselesaikan (`@api.constrains`).

### 2. `library_management` (Manajemen Perpustakaan)
Modul pengelolaan data buku, kategori, anggota, dan sirkulasi peminjaman buku:
- Relasi kategori buku (`Many2one` & `One2many`), penghitungan jumlah buku otomatis.
- Nomor anggota & transaksi peminjaman otomatis via `ir.sequence`.
- Batasan data (*SQL Constraints*) untuk ISBN unik dan tahun terbit.

### 3. `om_hospital` (Hospital Management)
Modul dasar pengenalan struktur Odoo:
- Master data pasien, tree view, form view, hak akses (*ACL*), dan menu navigasi.

---

## 🚀 Cara Menjalankan Modul

1. Pastikan Odoo Server dan PostgreSQL sudah aktif.
2. Konfigurasikan file `odoo.conf`:
   ```ini
   [options]
   addons_path = addons,custom_addons
   ```
3. Update App List di Odoo Developer Mode lalu install modul yang diinginkan.

---

**Author:** Hafizh Irfansyah  
**License:** LGPL-3
