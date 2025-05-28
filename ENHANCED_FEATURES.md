# PIXEL SNAKE GAME - ENHANCED EDITION

## FITUR BARU YANG SUDAH DIIMPLEMENTASIKAN

### 1. VARIASI MAKANAN DENGAN EFEK BERBEDA

#### Makanan Baru:
- **Shrink Food (Makanan Pengecil)**: 
  - Warna: Biru
  - Efek: Membuat ular lebih pendek untuk sementara (10 detik)
  - Poin: 15
  - Tekstur: Pil biru dengan simbol minus

- **Slowmo Food (Makanan Pelambat)**:
  - Warna: Cyan
  - Efek: Melambatkan pergerakan game untuk 15 detik
  - Poin: 20
  - Tekstur: Jam dengan jarum jam

- **Double Score Food (Makanan Pengganda Skor)**:
  - Warna: Emas
  - Efek: Menggandakan skor yang diperoleh untuk 20 detik
  - Poin: 30
  - Tekstur: Bintang emas dengan tulisan "2x"

- **Ghost Food (Makanan Hantu)**:
  - Warna: Biru muda
  - Efek: Memungkinkan ular melewati tubuhnya sendiri untuk 15 detik
  - Poin: 40
  - Tekstur: Hantu semi-transparan

#### Probabilitas Spawn Makanan:
- Normal Food: 5% (setiap 5 makanan normal)
- Special Food: 30%
- Super Food: 20%
- Shrink Food: 15%
- Slowmo Food: 10%
- Double Score Food: 10%
- Ghost Food: 10%

### 2. SISTEM RINTANGAN (OBSTACLES)

#### Jenis Rintangan:
- **Static Obstacles**: Rintangan diam berbentuk batu/bata
- **Moving Obstacles**: Rintangan bergerak dengan efek kristal/energi

#### Fitur Rintangan:
- Spawning otomatis dalam Classic Mode setiap 100 poin
- Maksimal 5 rintangan di layar bersamaan
- Rintangan bergerak dengan AI sederhana (memantul di tepi)
- Tekstur pixel art yang berbeda untuk setiap jenis
- Animasi berkedip untuk rintangan bergerak

#### Mode Game dengan Rintangan:
- **Classic Mode**: Rintangan spawn secara acak
- **Challenge Mode**: Level dengan rintangan yang sudah ditentukan

### 3. SISTEM MENU YANG LENGKAP

#### Menu Utama:
- Start Game
- Game Mode Selection
- High Scores
- Settings
- About
- Quit

#### Game Mode Selection:
- **Classic Mode**: Game tradisional dengan rintangan yang bertambah
- **Time Attack Mode**: Dapatkan skor maksimal dalam 2 menit
- **Challenge Mode**: Level dengan tata letak rintangan tertentu

#### Settings Menu:
- Toggle Sound ON/OFF
- Toggle Music ON/OFF
- Pilihan Difficulty (Easy/Medium/Hard)
- Kembali ke Menu

#### High Scores:
- Menampilkan high score untuk setiap tingkat kesulitan
- Tersimpan secara permanen di file

### 4. ANIMASI TAMBAHAN

#### Animasi Kematian Ular:
- Efek flash merah saat ular mati
- Partikel ledakan kuning keluar dari setiap segmen ular
- Animasi berlangsung 2 detik sebelum game over

#### Animasi Makanan Muncul:
- Lingkaran mengembang saat makanan spawn
- Partikel putih menyebar dari titik spawn
- Efek fade-out untuk partikel

#### Animasi Menu:
- Judul bergerak naik-turun
- Indikator seleksi dengan panah
- Transisi smooth antar menu

### 5. EFEK VISUAL TAMBAHAN

#### Power-up Indicators:
- Tampilan status power-up aktif di layar
- Timer visual untuk makanan khusus
- Perubahan warna kepala ular sesuai power-up

#### Background Effects:
- Tekstur pixel art untuk background
- Efek scanline pada game over
- Overlay semi-transparan untuk pause

#### UI Enhancements:
- Tampilan waktu untuk Time Attack Mode
- Indikator score multiplier
- Status power-up yang sedang aktif

### 6. SISTEM KONTROL YANG DIPERBAIKI

#### Game Controls:
- Arrow keys: Menggerakkan ular
- ESC/P: Pause/Resume game
- Q: Quit ke menu (dari pause)

#### Menu Navigation:
- Arrow keys: Navigasi menu
- Enter/Space: Konfirmasi
- ESC: Kembali ke menu sebelumnya

### 7. SISTEM AUDIO YANG DIPERLUAS

#### Sound Effects Baru:
- Suara berbeda untuk setiap jenis makanan
- Efek suara untuk power-up
- Suara navigasi menu yang responsif

#### Music System:
- Background music yang bisa di-toggle
- Kontrol volume terpisah untuk music dan SFX

### 8. PENYEIMBANGAN GAME

#### Speed System:
- Frame-based movement untuk kontrol yang lebih baik
- Efek slowmo yang mempengaruhi kecepatan game
- Difficulty scaling yang lebih halus

#### Scoring System:
- Poin berbeda untuk setiap jenis makanan
- Sistem multiplier yang stackable
- High score terpisah per difficulty

### 9. STRUCTURE KODE YANG DIPERBAIKI

#### New Files:
- `game_manager.py`: Mengelola state game dan menu
- `obstacles.py`: Sistem rintangan lengkap

#### Enhanced Files:
- `constants.py`: Konstanta baru untuk semua fitur
- `snake.py`: Power-up system dan animasi kematian
- `food.py`: Jenis makanan baru dan spawn animation
- `textures.py`: Tekstur untuk makanan dan rintangan baru

### 10. FITUR PIXEL ART

#### Enhanced Textures:
- Tekstur pixel art untuk semua makanan baru
- Animasi frame-by-frame
- Efek visual yang konsisten dengan tema 8-bit

#### Visual Effects:
- Partikel pixel art
- Scanline effects
- Retro color palette

## CARA BERMAIN

1. **Menu Navigation**: Gunakan arrow keys dan Enter untuk navigasi
2. **Game Modes**: Pilih mode permainan sesuai preferensi
3. **Controls**: Arrow keys untuk menggerak ular, ESC untuk pause
4. **Power-ups**: Kumpulkan makanan khusus untuk efek unik
5. **Obstacles**: Hindari rintangan yang muncul di arena
6. **Scoring**: Dapatkan skor tinggi dengan strategi power-up

## INSTALASI DAN MENJALANKAN

1. Pastikan Python dan pygame terinstall
2. Jalankan: `python src/main.py`
3. Game akan membuka menu utama
4. Pilih mode dan mulai bermain!

Semua fitur telah diimplementasikan dan siap untuk dimainkan!
