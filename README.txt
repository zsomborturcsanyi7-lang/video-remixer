 === VIDEO REMIXER - AUTOMATIKUS YOUTUBE REMIX KÉSZÍTŐ ===

EZ CSAK OKTATÁSI CÉLÚ! A YouTube copyright szabályzatát be kell tartani!

=== ELŐZETES KÖVETELMÉNYEK ===

1. Python 3.8 vagy újabb
2. FFmpeg telepítve (https://ffmpeg.org/download.html)
   - Töltsd le és tedd a PATH-ba
   - Vagy módosítsd a config fájlban az ffmpeg_path értékét
3. YouTube API kulcs (opcionális, kereséshez)

=== TELEPÍTÉS ===

1. Futtasd a run_remixer.bat fájlt (telepíti a csomagokat)
2. Vagy kézzel: pip install -r requirements.txt

=== KONFIGURÁCIÓ ===

1. Szerkeszd a video_remixer_config.json fájlt:
   - youtube_api_key: YouTube Data API v3 kulcs (opcionális)
   - crafting_videos_folder: Mappa, ahol a barkácsolós/crafting videók vannak
   - output_folder: Kimeneti mappa a remixelt videóknak

2. Hozz létre egy "crafting_videos" mappát, és tölts fel bele néhány
   barkácsolós, kézműves vagy "sastyfieng" videót (saját tartalom!)

=== HASZNÁLAT ===

1. Alap futtatás (kézi URL megadással):
   python video_remixer.py

2. URL megadással:
   python video_remixer.py "https://www.youtube.com/watch?v=..."

3. Batch fájllal:
   run_remixer.bat
   VAGY
   run_remixer.bat "https://www.youtube.com/watch?v=..."

=== MŰKÖDÉS ===

1. Letölt egy YouTube videót (yt-dlp)
2. Kiválaszt egy véletlenszerű crafting videót a mappából
3. FFmpeg-gel összekeveri a két videót (side-by-side)
4. Elmenti a remixelt videót
5. YouTube feltöltés JELENLEG NEM AKTÍV (OAuth hitelesítés kell)

=== FONTOS FIGYELMEZTETÉSEK ===

1. COPYRIGHT: Még remixelt tartalomra is kaphatsz copyright strike-ot!
   - Csak saját tartalmat vagy kreatív közös tartalmat használj
   - Ellenőrizd a YouTube Fair Use policy-ját

2. A crafting videóknak SAJÁTnak kell lenniük, vagy royalty-free-nek

3. YouTube API kvóták korlátozzák a keresést

4. Ez csak egy technikai demonstráció, ne használd tömeges tartalomgyártásra!

=== HIBAELHÁRÍTÁS ===

- "FFmpeg not found": Telepítsd az FFmpeg-et és tedd PATH-ba
- "No crafting videos": Tölts fel videókat a crafting_videos mappába
- Download error: Ellenőrizd az internetkapcsolatot és az URL-t

=== KÖVETKEZŐ LÉPÉSEK (ha komolyan akarod használni) ===

1. Szerezz YouTube API kulcsot: https://console.cloud.google.com/
2. Állítsd be az OAuth hitelesítést a YouTube feltöltéshez
3. Bővítsd a remixelési lehetőségeket (több effekt, hangkeverés)
4. Implementálj tartalomfelismerést a copyright elkerülésére