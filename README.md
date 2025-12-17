# Type Or Die

**Type Or Die** adalah game survival mengetik cepat (typing game) yang dibangun menggunakan **Python** dan library **Pygame**. Pemain berperan sebagai survivor yang harus bertahan hidup dari serangan gelombang zombie dengan cara mengetik kata-kata yang muncul di atas kepala mereka.

Proyek ini dikembangkan sebagai Tugas Akhir mata kuliah Pemrograman Berorientasi Objek (PBO), menerapkan prinsip-prinsip OOP.

## 🎮 Fitur Utama

- **Mekanik Mengetik Cepat**: Ketik kata dengan akurat untuk menembak dan mengalahkan zombie.
- **Sistem Gelombang Dinamis**: Menggunakan `AIDirector` untuk mengatur spawn rate dan kecepatan zombie yang semakin sulit seiring bertambahnya skor.
- **Visual & Animasi**:
  - Animasi sprite karakter dan zombie yang halus.
  - Efek partikel ledakan saat zombie mati atau pemain kalah.
  - Visualisasi HP Bar dan Laser Sight dinamis (berubah warna saat membidik).
  - Dukungan resolusi Fullscreen (1920x1080 Scaled).
- **Sistem Skor**: Penyimpanan High Score lokal menggunakan JSON.
- **Manajemen State**: Transisi mulus antara Menu, Gameplay, Pengaturan, dan Game Over.

## 🛠️ Instalasi & Cara Menjalankan

Pastikan Anda telah menginstal **Python 3.10** atau lebih baru.

1.  **Buat Virtual Environment** (Disarankan):

    ```bash
    # Linux / Mac
    python -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

2.  **Instal Dependensi**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Game**:
    ```bash
    python main.py
    ```

## 📂 Struktur Kode & Arsitektur

Proyek ini dirancang dengan struktur modular yang rapi, memisahkan logika inti, entitas game, dan tampilan (state).

### 1. Core (`core/`)

Bagian ini berisi logika dasar engine permainan.

- **`game.py`**: Mengelola **Game Loop** utama, inisialisasi Pygame, dan manajemen transisi antar state.
- **`state.py`**: _Abstract Base Class_ yang menerapkan **State Pattern**. Setiap halaman (Menu, Game, dll) mewarisi kelas ini.
- **`director.py`**: **AI Director** yang mengontrol ritme permainan (pacing), menentukan kapan dan seberapa cepat zombie muncul.
- **`score_manager.py`**: Menangani penyimpanan dan pembacaan skor tertinggi dari file `highscores.json`.
- **`animation.py`**: Modul utilitas untuk memuat dan memproses frame animasi dari file GIF/Sprite.

### 2. Entities (`entities/`)

Objek-objek interaktif dalam permainan.

- **`character.py`**: Kelas induk untuk semua karakter hidup.
- **`player.py`**: Mengatur logika pemain, input keyboard, sistem HP, dan animasi menembak.
- **`zombie.py`**: Mengatur logika musuh, pergerakan, deteksi kata yang diketik, dan animasi kematian/ledakan.
- **`projectile.py`**: Objek peluru visual yang bergerak dari pemain ke target.
- **`factory.py`**: Menerapkan **Factory Pattern** untuk pembuatan objek (Player & Zombie) secara terpusat.

### 3. States (`states/`)

Implementasi konkret dari setiap tampilan permainan.

- **`menu_state.py`**: Menu utama (Mulai, Setting, Keluar).
- **`game_state.py`**: Logika inti gameplay (Update loop, rendering objek, input handling).
- **`settings_state.py`**: Menu pengaturan untuk mengubah tingkat kesulitan atau volume.
- **`game_over_state.py`**: Layar akhir permainan yang menampilkan skor akhir.

### 4. Root Files

- **`main.py`**: Titik masuk (Entry Point) aplikasi.
- **`settings.py`**: Menyimpan konstanta global seperti Resolusi Layar, Warna, Path Aset, dan FPS.

## 🧩 Design Patterns

Kode ini menerapkan beberapa Design Pattern:

1.  **State Pattern**: Digunakan untuk mengelola alur permainan. `Game` class memegang referensi ke `State` saat ini, memungkinkan pergantian tampilan tanpa logika `if-else` yang rumit.
2.  **Factory Pattern**: `EntityFactory` digunakan untuk menginstansiasi objek game kompleks seperti Zombie dan Player, memisahkan logika pembuatan dari logika penggunaan.
3.  **Singleton (via Static Methods)**: `ScoreManager` menggunakan metode statis untuk diakses dari mana saja tanpa perlu instansiasi berulang.

## ⌨️ Kontrol

- **Keyboard (A-Z)**: Ketik huruf sesuai kata di atas kepala zombie untuk menyerang.
- **Enter**: Konfirmasi pilihan di menu.
- **Panah Atas / Bawah**: Navigasi menu.
- **Panah Kiri / Kanan**: Mengubah nilai slider di pengaturan.
- **Esc / Quit**: Keluar dari permainan.

---

_Dikembangkan oleh Fatih & Rhama - Semester 3 PBO FP_
