import os
import sys
import subprocess
import json
from datetime import datetime
import re

class SimpleVideoDownloader:
    def __init__(self):
        self.config = {
            "output_folder": "C:\\Users\\iga\\Desktop\\downloaded_videos",
            "crafting_folder": "C:\\Users\\iga\\Desktop\\crafting_videos"
        }
        
        # Mappák létrehozása
        os.makedirs(self.config["output_folder"], exist_ok=True)
        os.makedirs(self.config["crafting_folder"], exist_ok=True)
    
    def check_requirements(self):
        """Ellenőrzi az yt-dlp telepítését"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            print(f"✓ yt-dlp telepítve (verzió: {version})")
            return True
        except:
            print("✗ yt-dlp nincs telepítve")
            print("Telepítés: pip install yt-dlp")
            return False
    
    def fix_shorts_url(self, url):
        """YouTube Shorts URL-t alakít át normál videó URL-lé"""
        # YouTube Shorts: https://www.youtube.com/shorts/VIDEO_ID
        # Normál videó: https://www.youtube.com/watch?v=VIDEO_ID
        
        shorts_pattern = r"youtube\.com/shorts/([a-zA-Z0-9_-]+)"
        match = re.search(shorts_pattern, url)
        
        if match:
            video_id = match.group(1)
            normal_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"Shorts URL átalakítva: {normal_url}")
            return normal_url
        
        return url
    
    def download_video(self, url):
        """Letölt egy YouTube videót"""
        # Shorts URL javítása
        url = self.fix_shorts_url(url)
        print(f"Letöltés: {url}")
        
        try:
            # Kimeneti fájl neve
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.config["output_folder"], f"video_{timestamp}")
            
            # yt-dlp parancs - több formátummal próbálkozik
            cmd = [
                'yt-dlp',
                '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # 720p max
                '--merge-output-format', 'mp4',
                '-o', f"{output_file}.%(ext)s",
                '--no-warnings',  # Kevesebb figyelmeztetés
                url
            ]
            
            print("Letöltés folyamatban... (ez eltarthat pár percig)")
            print("Ha nem működik, próbáld ezt a parancsot kézzel:")
            print(" ".join(cmd))
            print()
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Megkeressük a letöltött fájlt
                for ext in ['.mp4', '.webm', '.mkv']:
                    possible_file = f"{output_file}{ext}"
                    if os.path.exists(possible_file):
                        final_file = possible_file
                        break
                else:
                    # Ha nem találjuk, keressük a mappában
                    for file in os.listdir(self.config["output_folder"]):
                        if file.startswith(f"video_{timestamp}"):
                            final_file = os.path.join(self.config["output_folder"], file)
                            break
                    else:
                        final_file = None
                
                if final_file and os.path.exists(final_file):
                    size_mb = os.path.getsize(final_file) / (1024 * 1024)
                    print(f"✓ Sikeres letöltés: {final_file}")
                    print(f"  Fájlméret: {size_mb:.1f} MB")
                    return final_file
                else:
                    print("✓ Letöltés sikeres, de a fájl nem található")
                    print(f"  Stdout: {result.stdout[:200]}...")
                    return None
            else:
                print(f"✗ Hiba történt")
                print(f"  Stderr: {result.stderr[:500]}")
                
                # Alternatív próbálkozás egyszerűbb formátummal
                print("\nAlternatív letöltés próbálkozása...")
                cmd_simple = [
                    'yt-dlp',
                    '-f', 'worst',  # Legkisebb minőség
                    '-o', f"{output_file}.%(ext)s",
                    url
                ]
                
                result2 = subprocess.run(cmd_simple, capture_output=True, text=True)
                if result2.returncode == 0:
                    print("✓ Alternatív letöltés sikerült!")
                    # Fájl keresése
                    for file in os.listdir(self.config["output_folder"]):
                        if file.startswith(f"video_{timestamp}"):
                            final_file = os.path.join(self.config["output_folder"], file)
                            size_mb = os.path.getsize(final_file) / (1024 * 1024)
                            print(f"  Fájl: {final_file}")
                            print(f"  Méret: {size_mb:.1f} MB")
                            return final_file
                
                return None
                
        except Exception as e:
            print(f"✗ Kivétel történt: {e}")
            return None
    
    def list_crafting_videos(self):
        """Listázza a crafting videókat"""
        crafting_folder = self.config["crafting_folder"]
        
        if not os.path.exists(crafting_folder):
            print(f"ℹ️ Hozd létre a mappát: {crafting_folder}")
            try:
                os.makedirs(crafting_folder, exist_ok=True)
                print(f"✓ Mappa létrehozva: {crafting_folder}")
            except:
                print(f"✗ Nem sikerült létrehozni a mappát")
            return []
        
        videos = []
        for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            for file in os.listdir(crafting_folder):
                if file.endswith(ext):
                    videos.append(os.path.join(crafting_folder, file))
        
        if videos:
            print(f"✓ Crafting videók ({len(videos)} db):")
            for i, video in enumerate(videos[:5], 1):
                print(f"  {i}. {os.path.basename(video)}")
            if len(videos) > 5:
                print(f"  ... és még {len(videos)-5} db")
        else:
            print("ℹ️ Nincs crafting videó a mappában")
            print(f"  Tedd a videókat ide: {crafting_folder}")
            print("  (saját készítésű barkácsolós/kézműves videók)")
        
        return videos
    
    def create_instructions(self):
        """Létrehoz egy útmutatót"""
        instructions = f"""
        === VIDEO DOWNLOADER - HASZNÁLATI ÚTMUTATÓ ===
        
        LETÖLTÉS:
        1. Normál YouTube videó URL-t adj meg (nem Shorts)
           Példa: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        
        2. Ha Shorts URL-t adsz meg, automatikusan átalakítom
        
        3. A letöltött videók itt landolnak:
           {self.config["output_folder"]}
        
        CRAFTING VIDEÓK:
        1. Hozz létre egy mappát:
           {self.config["crafting_folder"]}
        
        2. Tölts fel saját barkácsolós/kézműves videókat
           - Saját készítésű legyen!
           - Ne copyrightolt anyagot!
        
        SZERKESZTÉS:
        1. Telepítsd az FFmpeg-et: https://ffmpeg.org/download.html
        
        2. Használj ingyenes videószerkesztőt:
           - Shotcut: https://shotcut.org/
           - DaVinci Resolve: https://www.blackmagicdesign.com/products/davinciresolve
           - Windows Video Editor (beépített)
        
        3. Keverd össze a letöltött videót a crafting videóval
        
        PROBLÉMÁK:
        - Ha nem működik, frissítsd az yt-dlp-t:
          pip install --upgrade yt-dlp
        
        - Ha még mindig nem működik, próbáld ezt a parancsot kézzel:
          yt-dlp -f best[height<=720] -o "video.%(ext)s" URL_CÍME
        """
        
        instructions_file = os.path.join(os.path.dirname(__file__), "UTMUTATO_V2.txt")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n✓ Útmutató létrehozva: {instructions_file}")
        return instructions_file
    
    def run(self):
        """Futtatja a programot"""
        print("=== SIMPLE VIDEO DOWNLOADER v2 ===\n")
        
        # Ellenőrzés
        if not self.check_requirements():
            print("\nTelepítsd az yt-dlp-t: pip install yt-dlp")
            return
        
        # Crafting videók listázása
        self.list_crafting_videos()
        
        # URL bekérése
        print("\n" + "="*50)
        
        url = None
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = input("\nYouTube URL (vagy Enter a kilépéshez): ").strip()
        
        if not url:
            print("Kilépés...")
            self.create_instructions()
            return
        
        # Letöltés
        downloaded = self.download_video(url)
        
        if downloaded:
            print("\n" + "="*50)
            print("✓ KÉSZ!")
            print(f"Videó letöltve: {downloaded}")
            print("\nKövetkező lépések:")
            print("1. Hozz létre crafting videókat")
            print("2. Telepítsd az FFmpeg-et vagy videószerkesztőt")
            print("3. Szerkeszd össze a videókat")
        else:
            print("\n" + "="*50)
            print("✗ A letöltés nem sikerült")
            print("Próbáld:")
            print("1. Másik YouTube videóval")
            print("2. Frissítsd az yt-dlp-t: pip install --upgrade yt-dlp")
            print("3. Próbáld kézzel: yt-dlp URL_CÍME")
        
        # Útmutató létrehozása
        self.create_instructions()

def main():
    downloader = SimpleVideoDownloader()
    downloader.run()

if __name__ == "__main__":
    main()