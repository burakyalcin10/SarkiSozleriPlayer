import whisper
import vlc
import time
import sys
from pathlib import Path
import torch
import numpy as np
import requests
import zipfile
import os
import subprocess
import re
from colorama import init, Fore, Back, Style

# Renkli çıktı için colorama'yı başlat
init()

def setup_ffmpeg():
    print(f"{Fore.YELLOW}FFmpeg kuruluyor...{Style.RESET_ALL}")
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        print(f"{Fore.GREEN}FFmpeg zaten kurulu.{Style.RESET_ALL}")
        return True
    except FileNotFoundError:
        pass
    
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    print(f"{Fore.YELLOW}FFmpeg indiriliyor...{Style.RESET_ALL}")
    
    try:
        response = requests.get(ffmpeg_url, stream=True)
        with open("ffmpeg.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"{Fore.YELLOW}FFmpeg çıkarılıyor...{Style.RESET_ALL}")
        with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
            zip_ref.extractall("ffmpeg")
        
        ffmpeg_exe = None
        for root, dirs, files in os.walk("ffmpeg"):
            if "ffmpeg.exe" in files:
                ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
                break
        
        if ffmpeg_exe:
            os.rename(ffmpeg_exe, "ffmpeg.exe")
            print(f"{Fore.GREEN}FFmpeg kurulumu tamamlandı.{Style.RESET_ALL}")
            return True
            
    except Exception as e:
        print(f"{Fore.RED}FFmpeg kurulumu başarısız oldu: {e}{Style.RESET_ALL}")
        return False

def temizle_sozler(text):
    # Gereksiz metinleri temizle
    text = re.sub(r'abone ol.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'like.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'subscribe.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'follow.*', '', text, flags=re.IGNORECASE)
    
    # Noktalama işaretlerini düzelt
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def get_lyrics_with_timing(audio_path):
    print(f"{Fore.CYAN}Şarkı sözleri çıkarılıyor, lütfen bekleyin...{Style.RESET_ALL}")
    
    # Whisper modelini yükle (orta boy model, daha doğru sonuçlar)
    model = whisper.load_model("medium")
    
    # Ses dosyasını analiz et
    result = model.transcribe(audio_path, language="tr")
    
    # Sonuçları düzenle ve kelimelere ayır
    segments_with_timing = []
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"].strip()
        if text:
            # Sözleri temizle
            cleaned_text = temizle_sozler(text)
            if cleaned_text:
                # Metni kelimelere ayır
                words = cleaned_text.split()
                # Her kelime için yaklaşık zaman hesapla
                word_duration = (end_time - start_time) / len(words)
                
                # Her kelime için zamanı ayarla
                words_with_timing = []
                for i, word in enumerate(words):
                    word_time = start_time + (i * word_duration)
                    words_with_timing.append((word_time, word))
                
                segments_with_timing.append((start_time, end_time, words_with_timing))
    
    return segments_with_timing

def format_line(words, current_word_index=-1):
    # Satırı formatla
    line = ""
    for i, word in enumerate(words):
        if i == current_word_index:
            line += f"{Fore.YELLOW}{Style.BRIGHT}{word}{Style.RESET_ALL} "
        else:
            line += f"{Fore.CYAN}{word}{Style.RESET_ALL} "
    return f"♪ {line.strip()} ♪"

def play_song_with_lyrics(audio_path):
    try:
        if not setup_ffmpeg():
            print(f"{Fore.RED}FFmpeg kurulumu başarısız oldu. Program sonlandırılıyor.{Style.RESET_ALL}")
            return
            
        segments_with_timing = get_lyrics_with_timing(audio_path)
        
        # VLC player'ı başlat
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(audio_path)
        player.set_media(media)
        
        player.play()
        time.sleep(1)
        
        # Şarkı sözlerini zamanlamalı göster
        start_time = time.time()
        displayed_lines = []
        
        for segment_start, segment_end, words_with_timing in segments_with_timing:
            # Satırdaki kelimeleri al
            words = [word for _, word in words_with_timing]
            
            # Her kelime için
            for i, (word_time, _) in enumerate(words_with_timing):
                current_time = time.time() - start_time
                if current_time < word_time:
                    time.sleep(word_time - current_time)
                
                # Terminal ekranını temizle
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Başlık göster
                print(f"\n{Back.BLUE}{Fore.WHITE} 🎵 Şarkı Sözleri 🎵 {Style.RESET_ALL}\n")
                
                # Önceki satırları göster
                for old_line in displayed_lines[-3:]:  # Son 3 satırı göster
                    print(f"{Fore.LIGHTBLACK_EX}{old_line}{Style.RESET_ALL}")
                
                # Aktif satırı göster
                current_line = format_line(words, i)
                print(current_line)
            
            # Satır tamamlandığında listeye ekle
            displayed_lines.append(format_line(words))
        
        while player.is_playing():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Bir hata oluştu: {e}{Style.RESET_ALL}")
    finally:
        if 'player' in locals():
            player.stop()
        
        # Geçici dosyaları temizle
        if os.path.exists("ffmpeg.zip"):
            os.remove("ffmpeg.zip")
        if os.path.exists("ffmpeg"):
            import shutil
            shutil.rmtree("ffmpeg")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Kullanım: python sarki_sozleri_v5.py sarki.mp3{Style.RESET_ALL}")
        sys.exit(1)
        
    audio_path = sys.argv[1]
    
    if not Path(audio_path).exists():
        print(f"{Fore.RED}Hata: {audio_path} dosyası bulunamadı!{Style.RESET_ALL}")
        sys.exit(1)
    
    play_song_with_lyrics(audio_path) 