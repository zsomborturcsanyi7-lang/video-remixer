import os
import json
import random
import subprocess
import shutil
from datetime import datetime
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class VideoRemixer:
    def __init__(self, config_path="video_remixer_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.setup_folders()
        
    def setup_folders(self):
        """Létrehozza a szükséges mappákat"""
        folders = [
            self.config['output_folder'],
            self.config['temp_folder'],
            self.config['crafting_videos_folder']
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    def search_popular_video(self):
        """YouTube-on keres népszerű videót"""
        print("YouTube videó keresése...")
        
        # Egyszerűbb megoldás: yt-dlp használata trending videókhoz
        try:
            # Ez csak példa - a valóságban YouTube API-t kellene használni
            print("MEGJEGYZÉS: YouTube API kulcs szükséges a kereséshez")
            print("Átmeneti megoldás: kézzel adj meg egy YouTube URL-t")
            return None
        except Exception as e:
            print(f"Hiba a keresés közben: {e}")
            return None
    
    def download_video(self, video_url):
        """Letölt egy videót yt-dlp-val"""
        print(f"Videó letöltése: {video_url}")
        
        try:
            output_template = os.path.join(self.config['temp_folder'], '%(title)s.%(ext)s')
            
            cmd = [
                'yt-dlp',
                '-f', 'best[height<=720]',  # 720p max
                '-o', output_template,
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Megkeressük a letöltött fájlt
                for file in os.listdir(self.config['temp_folder']):
                    if file.endswith(('.mp4', '.webm', '.mkv')):
                        return os.path.join(self.config['temp_folder'], file)
            else:
                print(f"Hiba a letöltés közben: {result.stderr}")
                
        except Exception as e:
            print(f"Hiba: {e}")
        
        return None
    
    def get_crafting_video(self):
        """Visszaad egy crafting/barkácsolós videót a mappából"""
        crafting_folder = self.config['crafting_videos_folder']
        
        if not os.path.exists(crafting_folder):
            print(f"Crafting mappa nem létezik: {crafting_folder}")
            return None
        
        video_files = []
        for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            video_files.extend([f for f in os.listdir(crafting_folder) if f.endswith(ext)])
        
        if not video_files:
            print("Nincs crafting videó a mappában!")
            return None
        
        selected = random.choice(video_files)
        return os.path.join(crafting_folder, selected)
    
    def remix_videos(self, main_video, crafting_video):
        """Összekever két videót FFmpeg-gel"""
        print("Videók remixelése...")
        
        if not main_video or not crafting_video:
            print("Hiányzó videófájl!")
            return None
        
        output_path = os.path.join(
            self.config['output_folder'],
            f"remix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        )
        
        try:
            # 1. Kivágunk 30 másodpercet a fő videóból
            temp_main = os.path.join(self.config['temp_folder'], "temp_main.mp4")
            cmd1 = [
                self.config['ffmpeg_path'],
                '-i', main_video,
                '-t', '30',  # 30 másodperc
                '-c', 'copy',
                temp_main
            ]
            
            # 2. Kivágunk 30 másodpercet a crafting videóból
            temp_craft = os.path.join(self.config['temp_folder'], "temp_craft.mp4")
            cmd2 = [
                self.config['ffmpeg_path'],
                '-i', crafting_video,
                '-t', '30',
                '-c', 'copy',
                temp_craft
            ]
            
            # 3. Két videó egymás mellett (side by side)
            cmd3 = [
                self.config['ffmpeg_path'],
                '-i', temp_main,
                '-i', temp_craft,
                '-filter_complex', 
                '[0:v]scale=640:360[0scaled];[1:v]scale=640:360[1scaled];[0scaled][1scaled]hstack=inputs=2[v]',
                '-map', '[v]',
                '-map', '0:a',
                '-t', '30',
                output_path
            ]
            
            # Parancsok futtatása
            for cmd in [cmd1, cmd2, cmd3]:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"FFmpeg hiba: {result.stderr}")
                    return None
            
            print(f"Remix elkészült: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Hiba a remixelés közben: {e}")
            return None
    
    def upload_to_youtube(self, video_path, title="Remixed Video", description="Automatically remixed video"):
        """Feltölti a videót YouTube-ra"""
        print("MEGJEGYZÉS: YouTube feltöltéshez OAuth hitelesítés szükséges")
        print("A feltöltés kihagyva a biztonság kedvéért")
        
        # Itt jönne a YouTube Data API v3 kód
        # De OAuth hitelesítés nélkül nem működik
        return False
    
    def cleanup(self):
        """Kitörli az ideiglenes fájlokat"""
        print("Takarítás...")
        try:
            if os.path.exists(self.config['temp_folder']):
                shutil.rmtree(self.config['temp_folder'])
                os.makedirs(self.config['temp_folder'], exist_ok=True)
        except Exception as e:
            print(f"Hiba a takarítás közben: {e}")
    
    def run(self, youtube_url=None):
        """Futtatja a teljes folyamatot"""
        print("=== Video Remixer indítása ===")
        
        # 1. Videó letöltése
        if youtube_url:
            main_video = self.download_video(youtube_url)
        else:
            print("Kérlek, adj meg egy YouTube URL-t!")
            youtube_url = input("YouTube URL: ")
            main_video = self.download_video(youtube_url)
        
        if not main_video:
            print("Nem sikerült letölteni a videót!")
            return
        
        # 2. Crafting videó kiválasztása
        crafting_video = self.get_crafting_video()
        if not crafting_video:
            print("Nincs crafting videó!")
            return
        
        # 3. Videók remixelése
        remixed_video = self.remix_videos(main_video, crafting_video)
        
        if remixed_video:
            print(f"Sikeresen elkészült a remix: {remixed_video}")
            
            # 4. YouTube feltöltés (jelenleg kihagyva)
            # upload_success = self.upload_to_youtube(remixed_video)
            # if upload_success:
            #     print("Sikeres YouTube feltöltés!")
            # else:
            #     print("YouTube feltöltés sikertelen")
        
        # 5. Takarítás
        self.cleanup()
        print("=== Kész ===")

def main():
    # Ellenőrizzük az FFmpeg-et
    if not shutil.which('ffmpeg'):
        print("HIBA: FFmpeg nincs telepítve vagy nincs a PATH-ban!")
        print("Töltse le innen: https://ffmpeg.org/download.html")
        return
    
    # Ellenőrizzük az yt-dlp-t
    if not shutil.which('yt-dlp'):
        print("HIBA: yt-dlp nincs telepítve!")
        print("Telepítés: pip install yt-dlp")
        return
    
    remixer = VideoRemixer()
    
    # Kérdezzük meg, van-e YouTube URL
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        remixer.run(url)
    else:
        remixer.run()

if __name__ == "__main__":
    main()