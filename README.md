# 🎵 Türkçe Şarkı Sözü Gösterici

Bu program, MP3 formatındaki Türkçe şarkıları çalarken sözlerini otomatik olarak algılayıp zamanlamalı bir şekilde gösteren bir Python uygulamasıdır.

## 🚀 Özellikler

- 🎯 Şarkı sözlerini otomatik algılama
- 🎵 Sözleri kelime kelime zamanlamalı gösterim
- 📝 Satır satır görüntüleme
- 🌈 Renkli terminal arayüzü
- 🔍 Akıllı söz temizleme ve filtreleme
- 🎼 VLC ile şarkı çalma

## 📋 Gereksinimler

```bash
pip install -r requirements.txt
```

Ayrıca sisteminizde VLC Media Player yüklü olmalıdır.

## 💻 Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/kullaniciadi/sarki-sozleri-gosterici.git
cd sarki-sozleri-gosterici
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

3. VLC Media Player'ı yükleyin:
- Windows: [VLC İndirme Sayfası](https://www.videolan.org/vlc/download-windows.html)
- Linux: `sudo apt-get install vlc`
- macOS: `brew install vlc`

## 🎮 Kullanım

```bash
python sarki_sozleri_v5.py sarki.mp3
```

## 🛠️ Nasıl Çalışır?

1. Program önce FFmpeg'i kontrol eder ve gerekirse otomatik olarak yükler
2. OpenAI Whisper modelini kullanarak şarkı sözlerini algılar
3. Sözleri zamanlamalı olarak işler
4. VLC ile şarkıyı çalar
5. Sözleri kelime kelime, renkli ve formatlı şekilde gösterir

## 📦 Proje Yapısı

- `sarki_sozleri_v5.py`: Ana program dosyası
- `requirements.txt`: Gerekli Python paketleri
- `README.md`: Proje dokümantasyonu

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: XYZ'`)
4. Branch'inizi push edin (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## ✨ Teşekkürler

- [OpenAI Whisper](https://github.com/openai/whisper) - Ses tanıma için
- [python-vlc](https://github.com/oaubert/python-vlc) - Medya oynatma için
- [colorama](https://github.com/tartley/colorama) - Renkli terminal çıktısı için 