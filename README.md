# Modul Pemesanan Ruangan

Modul ini adalah modul Odoo untuk mengelola pemesanan ruangan. Modul ini memungkinkan pengguna untuk membuat dan mengelola data ruangan serta pemesanan ruangan.

## Fitur

- Mengelola data ruangan (nama ruangan, kapasitas, lokasi)
- Membuat dan mengelola pemesanan ruangan
- Status pemesanan (Draft, Confirmed, Cancelled)

## Instalasi

1. Salin folder `room_booking` ke direktori `addons` Odoo Anda.
2. Restart server Odoo Anda.
3. Masuk ke antarmuka Odoo sebagai administrator.
4. Pergi ke menu `Aplikasi` dan klik `Perbarui Daftar Aplikasi`.
5. Cari `Room Booking` dan klik `Instal`.

## Penggunaan

1. Setelah modul diinstal, Anda akan melihat menu `Room Booking` di antarmuka Odoo.
2. Di bawah menu `Room Booking`, Anda dapat mengelola data ruangan dan pemesanan ruangan.
3. Untuk menambahkan ruangan baru, klik `Master Ruangan` dan kemudian klik `Buat`.
4. Untuk membuat pemesanan ruangan, klik `Pemesanan Ruangan` dan kemudian klik `Buat`.

## Struktur Direktori

- `models/`: Berisi definisi model untuk ruangan dan pemesanan ruangan.
  - `room_master.py`: Model untuk data ruangan.
  - `room_booking.py`: Model untuk pemesanan ruangan.
- `views/`: Berisi definisi tampilan untuk ruangan dan pemesanan ruangan.
  - `room_master_views.xml`: Tampilan untuk data ruangan.
  - `room_booking_views.xml`: Tampilan untuk pemesanan ruangan.
  - `menu.xml`: Definisi menu untuk modul.
  - `action.xml`: Definisi aksi untuk modul.
- `data/`: Berisi data awal untuk modul.
  - `room_booking_sequence.xml`: Definisi urutan untuk pemesanan ruangan.

## Lisensi

Modul ini dilisensikan di bawah lisensi MIT. Lihat file `LICENSE` untuk informasi lebih lanjut.