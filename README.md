# YouTube Video Készítő — Automatikus Videó Remixelő

**Verzió:** 1.0  
**Szerző:** Zsombi & Hermes Agent (Nous Research)  
**Státusz:** Működő prototípus

---

## Leírás

A **YouTube Video Készítő** egy automatikus videó remixelő eszköz, amely YouTube videókat tölt le, feldolgoz és újrakever. A program az **yt-dlp**-t használja letöltésre és az **FFmpeg**-et vágásra, keverésre és effektek alkalmazására. A projekt része egy egyszerű letöltő eszköz is (`simple_video_downloader.py`).

---

## Fájlszerkezet

```
youtube video készitö/
│
├── video_remixer.py            # Fő remixelő program (235 sor)
├── simple_video_downloader.py  # Egyszerű YouTube letöltő
├── run_remixer.bat             # Windows indító script
├── video_remixer_config.json   # Konfigurációs fájl
└── requirements.txt            # Python függőségek
```

---

## Használat

### Gyors indítás

```bash
# Windows batch fájl
run_remixer.bat

# URL paraméterrel
run_remixer.bat "https://www.youtube.com/watch?v=..."
```

### Kézi indítás

```bash
# Függőségek telepítése
pip install -r requirements.txt

# Remixelő indítása
python video_remixer.py

# URL átadása
python video_remixer.py "https://www.youtube.com/watch?v=..."
```

### Konfiguráció

A `video_remixer_config.json` fájlban állítható be:

- `output_folder` — Kimeneti mappa
- `temp_folder` — Ideiglenes fájlok mappája
- `crafting_videos_folder` — Alap videók mappája
- YouTube API beállítások

---

## Munkafolyamat

1. **Videó keresés** — YouTube-on népszerű videó keresése (API vagy URL)
2. **Letöltés** — yt-dlp segítségével
3. **Feldolgozás** — FFmpeg vágás, keverés, effektek
4. **Kimenet** — Új videó mentése az output mappába

---

## Függőségek

### Python
- **Python** 3.8+
- **google-api-python-client** — YouTube API
- **google-auth-oauthlib** — Hitelesítés
- **google-auth-httplib2** — HTTP transzport
- **yt-dlp** — Letöltés
- **FFmpeg** — Videó feldolgozás (rendszer szinten telepítendő)

### Rendszer
- **FFmpeg** (`ffmpeg` parancs elérhető legyen a PATH-ban)
- **yt-dlp** (`yt-dlp` parancs)

---

## Fejlesztő

Zsombi & Hermes Agent (Nous Research) (AI asszisztens segítségével)
