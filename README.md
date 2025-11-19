# Type Or Die — Pygame

Langkah memulai

1. Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instal dependensi (termasuk tools pengembangan / testing):

```bash
pip install -r requirements.txt
```

3. Jalankan game:

```bash
python main.py
```

## Project structure and file responsibilities

Berikut penjelasan tiap file/folder di proyek ini dan apa fungsinya:

- `main.py`

  - Entry point aplikasi. Memulai `Game` dengan initial state (`MenuState`).
  - Singkat: startup + run loop.

- `settings.py`

  - Semua konstanta global (lebar/tinggi layar, FPS, warna, posisi default, spawn timer).
  - Gunakan file ini untuk mengatur parameter gameplay (difficulty, spawn rate).

- `core/`

  - `core/state.py` — base class `State` (abstract). Kontrak: setiap state harus implement `handle_event(event)`, `update(dt)`, dan `draw(screen)`.
  - `core/game.py` — pengelola state dan loop utama. Menerima class state awal dan memiliki method `change_state`, `quit`, dll.

- `states/`

  - `menu_state.py` — tampilan dan input pada menu utama. Menangani transisi ke `GameState`.
  - `game_state.py` — logika permainan utama: spawn zombie, memproses input typing, update & check game over.
  - `game_over_state.py` — menampilkan skor akhir dan mengijinkan pemain kembali ke menu.

- `entities/`

  - `character.py` — `Character` base yang turunan `pygame.sprite.Sprite` untuk reuse collider/image.
  - `player.py` — `Player` menyimpan typed buffer, method `type_char`/`clear_typed` dan menggambar UI.
  - `zombie.py` — `Zombie` punya `word`, `progress`, `speed`, dan method `type_char`, `is_dead`, `draw`.
  - `factory.py` — `EntityFactory` untuk membuat player/zombie; memudahkan spawn dengan konfigurasi default.

- `assets/`
  - Tempat menyimpan image, font, dan sound. Template awal kosong — isi dengan art & audio.

## Contracts / Expectations

- State

  - Input: `handle_event(self, event)` menerima event Pygame.
  - Update: `update(self, dt)` menerima delta-time (detik) untuk update logika.
  - Draw: `draw(self, screen)` menerima `pygame.Surface` untuk menggambar.

- Entity

  - `Character` harus menjadi `pygame.sprite.Sprite`, memiliki `image` dan `rect`.
  - `Player` & `Zombie` mempunyai API minimal: `update(dt)` + specialized methods (`type_char`, `is_dead`, `draw` pada `Zombie`).

- Factory
  - `EntityFactory.create_player()` -> `Player`
  - `EntityFactory.create_zombie()` -> `Zombie`

Jika kamu mengganti interface ini, pastikan `GameState` masih memanggil method yang benar atau perbarui `GameState`.

## Cara menambah `State`

1. Buat file baru di `states/` misal `pause_state.py`.
2. Turunkan dari `State` dan implement `handle_event`, `update`, `draw`.
3. Pada saat transisi, panggil `game.change_state(PauseState)` dari state aktif.

## Cara menambah perilaku Zombie (Strategy)

1. Buat interface `Behavior` (method: `update(zombie, dt)`), tambahkan folder `entities/behaviors/`.
2. Implement beberapa kelas behavior: `Walk`, `Chase`, `Sprint`.
3. Tambahkan property `behavior` pada `Zombie` dan delegasikan gerakan ke `self.behavior.update(self, dt)`.
4. Factory bisa memilih behavior berdasarkan difficulty random/level.

## Testing

- Gunakan `pytest` untuk unit tests pada factory/logic: contoh tes spawn, tes `type_char` untuk `Zombie`.

Cara membuat & menjalankan `pytest` singkat:


1. Struktur test (letakkan di `tests/`):

```
tests/
  test_factory.py
  test_zombie_typing.py
  ...
```

2. Contoh test (file `tests/test_example.py`):

```python
def test_math_small():
    assert 1 + 1 == 2
```

3. Headless Pygame pada CI / terminal: di file test yang butuh pygame, set env var sebelum import:

```python
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame
```

4. Menjalankan test:

```bash
pytest -q
```

5. Menjalankan test tertentu / single test:

```bash
pytest tests/test_zombie_typing.py -q
pytest tests/test_zombie_typing.py::test_zombie_typing_progress -q
pytest -k "zombie and typing" -q
```
