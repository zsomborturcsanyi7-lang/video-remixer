import os
import sys
import subprocess
import json
from datetime import datetime

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
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
            print("✓ yt-dlp telepítve")
            return True
        except:
            print("✗ yt-dlp nincs telepítve")
            print("Telepítés: pip install yt-dlp")
            return False
    
    def download_video(self, url):
        """Letölt egy YouTube videót"""
        print(f"Letöltés: {url}")
        
        try:
            # Kimeneti fájl neve
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.config["output_folder"], f"video_{timestamp}.mp4")
            
            # yt-dlp parancs
            cmd = [
                'yt-dlp',
                '-f', 'best[height<=480]',  # Alacsonyabb felbontás
                '-o', output_file,
                url
            ]
            
            print("Letöltés folyamatban... (ez eltarthat pár percig)")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Sikeres letöltés: {output_file}")
                
                # Fájlméret kiírása
                if os.path.exists(output_file):
                    size_mb = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"  Fájlméret: {size_mb:.1f} MB")
                
                return output_file
            else:
                print(f"✗ Hiba: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"✗ Hiba történt: {e}")
            return None
    
    def list_crafting_videos(self):
        """Listázza a crafting videókat"""
        crafting_folder = self.config["crafting_folder"]
        
        if not os.path.exists(crafting_folder):
            print(f"✗ A mappa nem létezik: {crafting_folder}")
            return []
        
        videos = []
        for ext in ['.mp4', '.avi', '.mov', '.mkv']:
            for file in os.listdir(crafting_folder):
                if file.endswith(ext):
                    videos.append(os.path.join(crafting_folder, file))
        
        if videos:
            print(f"✓ Crafting videók ({len(videos)} db):")
            for i, video in enumerate(videos[:5], 1):  # Csak az első 5
                print(f"  {i}. {os.path.basename(video)}")
            if len(videos) > 5:
                print(f"  ... és még {len(videos)-5} db")
        else:
            print("ℹ️ Nincs crafting videó a mappában")
            print(f"  Tedd a videókat ide: {crafting_folder}")
        
        return videos
    
    def create_instructions(self):
        """Létrehoz egy útmutatót"""
        instructions = f"""
        === VIDEO DOWNLOADER - HASZNÁLATI ÚTMUTATÓ ===
        
        1. CRAFTING VIDEÓK:
           - Hozz létre egy mappát: {self.config["crafting_folder"]}
           - Tölts fel saját barkácsolós/kézműves videókat
        
        2. LETÖLTÉS:
           - Add meg a YouTube URL-t
           - A videók itt landolnak: {self.config["output_folder"]}
        
        3. FFMPEG TELEPÍTÉSE (később):
           - Töltsd le: https://ffmpeg.org/download.html
           - Tedd a PATH-ba
           - Utána tudod szerkeszteni a videókat
        
        4. MANUÁLIS SZERKESZTÉS:
           - Használj Shotcut, DaVinci Resolve vagy Windows Video Editor-t
           - Keverd össze a letöltött videót a crafting videóval
        """
        
        instructions_file = os.path.join(os.path.dirname(__file__), "UTMUTATO.txt")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"✓ Útmutató létrehozva: {instructions_file}")
        return instructions_file
    
    def run(self):
        """Futtatja a programot"""
        print("=== SIMPLE VIDEO DOWNLOADER ===\n")
        
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
            print("1. Telepítsd az FFmpeg-et a szerkesztéshez")
            print("2. Tedd crafting videókat a mappába")
            print("3. Szerkeszd össze a videókat")
        
        # Útmutató létrehozása
        self.create_instructions()

def main():
    downloader = SimpleVideoDownloader()
    downloader.run()

if __name__ == "__main__":
    main()