# 🎤 Edge-TTS API

Professional Text-to-Speech API. 250+ ovoz, 50+ tilni qo'llab-quvvatlaydi.

**API URL:** `https://edgettsapi.vercel.app`

## 🚀 Tezkor Boshlash

### cURL

```bash
curl "https://edgettsapi.vercel.app/tts?text=Salom dunyo&voice=uz-UZ-MadinaNeural" --output audio.mp3
```

### JavaScript

```javascript
fetch('https://edgettsapi.vercel.app/tts?text=Salom&voice=uz-UZ-MadinaNeural')
  .then(res => res.blob())
  .then(blob => {
    const audio = new Audio(URL.createObjectURL(blob));
    audio.play();
  });
```

### Python

```python
import requests

response = requests.get('https://edgettsapi.vercel.app/tts', params={
    'text': 'Salom dunyo',
    'voice': 'uz-UZ-MadinaNeural'
})

with open('audio.mp3', 'wb') as f:
    f.write(response.content)
```

## 📚 Endpointlar

| Endpoint | Metod | Tavsif |
|----------|-------|--------|
| `/` | GET | API ma'lumotlari |
| `/health` | GET | Status tekshirish |
| `/tts` | GET/POST | Ovozga aylantirish |
| `/voices` | GET | Barcha ovozlar |
| `/voices/{til}` | GET | Til bo'yicha ovozlar |
| `/voice/{nom}` | GET | Ovoz ma'lumoti |
| `/languages` | GET | Barcha tillar |
| `/uzbek-voices` | GET | O'zbek ovozlari |

## 🎯 Asosiy Misollar

### 1. Oddiy TTS

```bash
curl "https://edgettsapi.vercel.app/tts?text=Hello World" -o output.mp3
```

### 2. O'zbek tilida

```bash
curl "https://edgettsapi.vercel.app/tts?text=Assalomu alaykum&voice=uz-UZ-MadinaNeural" -o uzbek.mp3
```

### 3. Tezlik va balandlik bilan

```bash
curl "https://edgettsapi.vercel.app/tts?text=Fast speech&voice=en-US-JennyNeural&rate=+50%&volume=+20%&pitch=+10Hz" -o fast.mp3
```

### 4. POST metodi

```bash
curl -X POST "https://edgettsapi.vercel.app/tts" \
  -H "Content-Type: application/json" \
  -d '{"text":"Salom","voice":"uz-UZ-MadinaNeural","rate":"+20%"}' -o post.mp3
```

## 💻 JavaScript Misollar

### Oddiy audio ijro

```javascript
async function speak(text, voice = 'uz-UZ-MadinaNeural') {
  const url = `https://edgettsapi.vercel.app/tts?text=${encodeURIComponent(text)}&voice=${voice}`;
  const res = await fetch(url);
  const blob = await res.blob();
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();
}

speak('Salom dunyo');
```

### Yuklab olish

```javascript
async function downloadAudio(text, voice, filename = 'audio.mp3') {
  const url = `https://edgettsapi.vercel.app/tts?text=${encodeURIComponent(text)}&voice=${voice}`;
  const res = await fetch(url);
  const blob = await res.blob();
  
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
}

downloadAudio('Test audio', 'en-US-JennyNeural', 'my-audio.mp3');
```

### POST metodi

```javascript
async function speakPost(text, options = {}) {
  const response = await fetch('https://edgettsapi.vercel.app/tts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      voice: options.voice || 'uz-UZ-MadinaNeural',
      rate: options.rate || '+0%',
      volume: options.volume || '+0%',
      pitch: options.pitch || '+0Hz'
    })
  });
  
  const blob = await response.blob();
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();
}

speakPost('Hello', { voice: 'en-US-JennyNeural', rate: '+20%' });
```

### HTML forma

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>TTS Demo</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; padding: 10px; margin: 10px 0; }
        select, button { padding: 10px; margin: 5px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>🎤 Text to Speech</h1>
    
    <textarea id="text" rows="4" placeholder="Matnni kiriting...">Salom dunyo!</textarea>
    
    <select id="voice">
        <option value="uz-UZ-MadinaNeural">🇺🇿 O'zbek (Madina)</option>
        <option value="uz-UZ-SardorNeural">🇺🇿 O'zbek (Sardor)</option>
        <option value="en-US-JennyNeural">🇺🇸 English (Jenny)</option>
        <option value="en-US-GuyNeural">🇺🇸 English (Guy)</option>
        <option value="ru-RU-SvetlanaNeural">🇷🇺 Русский (Светлана)</option>
        <option value="ru-RU-DmitryNeural">🇷🇺 Русский (Дмитрий)</option>
    </select>
    
    <div>
        <label>Tezlik: <input type="range" id="rate" min="-50" max="100" value="0"> <span id="rateVal">+0%</span></label>
    </div>
    
    <button onclick="speak()">🔊 Ijro qilish</button>
    <button onclick="download()">💾 Yuklab olish</button>
    
    <script>
        const rateInput = document.getElementById('rate');
        const rateVal = document.getElementById('rateVal');
        
        rateInput.addEventListener('input', (e) => {
            const val = e.target.value;
            rateVal.textContent = (val >= 0 ? '+' : '') + val + '%';
        });
        
        async function speak() {
            const text = document.getElementById('text').value;
            const voice = document.getElementById('voice').value;
            const rate = rateInput.value >= 0 ? `+${rateInput.value}%` : `${rateInput.value}%`;
            
            const url = `https://edgettsapi.vercel.app/tts?text=${encodeURIComponent(text)}&voice=${voice}&rate=${rate}`;
            
            try {
                const res = await fetch(url);
                const blob = await res.blob();
                const audio = new Audio(URL.createObjectURL(blob));
                audio.play();
            } catch (err) {
                alert('Xatolik: ' + err.message);
            }
        }
        
        async function download() {
            const text = document.getElementById('text').value;
            const voice = document.getElementById('voice').value;
            const rate = rateInput.value >= 0 ? `+${rateInput.value}%` : `${rateInput.value}%`;
            
            const url = `https://edgettsapi.vercel.app/tts?text=${encodeURIComponent(text)}&voice=${voice}&rate=${rate}`;
            
            try {
                const res = await fetch(url);
                const blob = await res.blob();
                
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'audio.mp3';
                a.click();
            } catch (err) {
                alert('Xatolik: ' + err.message);
            }
        }
    </script>
</body>
</html>
```

## 🐍 Python Misollar

### Oddiy foydalanish

```python
import requests

def text_to_speech(text, voice='uz-UZ-MadinaNeural', filename='output.mp3'):
    url = 'https://edgettsapi.vercel.app/tts'
    params = {'text': text, 'voice': voice}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'✅ Saqlandi: {filename}')
    else:
        print(f'❌ Xatolik: {response.status_code}')

# Foydalanish
text_to_speech('Salom dunyo', 'uz-UZ-MadinaNeural', 'uzbek.mp3')
```

### POST metodi

```python
import requests

def tts_advanced(text, voice='uz-UZ-MadinaNeural', rate='+0%', volume='+0%', pitch='+0Hz'):
    url = 'https://edgettsapi.vercel.app/tts'
    
    data = {
        'text': text,
        'voice': voice,
        'rate': rate,
        'volume': volume,
        'pitch': pitch
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f'Xatolik: {response.status_code}')

# Foydalanish
audio = tts_advanced('Hello World', voice='en-US-JennyNeural', rate='+20%')
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### Ko'p tillar

```python
import requests

texts = {
    'uz-UZ-MadinaNeural': 'Salom dunyo',
    'en-US-JennyNeural': 'Hello World',
    'ru-RU-SvetlanaNeural': 'Привет мир',
    'de-DE-KatjaNeural': 'Hallo Welt',
    'fr-FR-DeniseNeural': 'Bonjour le monde'
}

for voice, text in texts.items():
    response = requests.get(
        'https://edgettsapi.vercel.app/tts',
        params={'text': text, 'voice': voice}
    )
    
    filename = f"{voice.split('-')[0]}.mp3"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'✅ {filename}')
```

### Asinxron (asyncio)

```python
import aiohttp
import asyncio

async def async_tts(text, voice='uz-UZ-MadinaNeural'):
    url = 'https://edgettsapi.vercel.app/tts'
    params = {'text': text, 'voice': voice}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception(f'Xatolik: {response.status}')

async def main():
    audio = await async_tts('Salom', 'uz-UZ-MadinaNeural')
    with open('output.mp3', 'wb') as f:
        f.write(audio)
    print('✅ Tayyor!')

asyncio.run(main())
```

## 🔊 Ovozlar ro'yxati

### O'zbek ovozlarini olish

```bash
curl "https://edgettsapi.vercel.app/uzbek-voices"
```

```javascript
fetch('https://edgettsapi.vercel.app/uzbek-voices')
  .then(res => res.json())
  .then(data => console.log(data));
```

```python
import requests
voices = requests.get('https://edgettsapi.vercel.app/uzbek-voices').json()
print(voices)
```

### Barcha ovozlar

```bash
curl "https://edgettsapi.vercel.app/voices"
```

### Til bo'yicha

```bash
# Ingliz tili
curl "https://edgettsapi.vercel.app/voices/en-US"

# Rus tili
curl "https://edgettsapi.vercel.app/voices/ru-RU"
```

## 🎛️ Parametrlar

| Parametr | Qiymat | Default | Tavsif |
|----------|--------|---------|--------|
| `text` | string | **majburiy** | Matn |
| `voice` | string | `uz-UZ-MadinaNeural` | Ovoz |
| `rate` | string | `+0%` | Tezlik (-50% / +100%) |
| `volume` | string | `+0%` | Balandlik (-50% / +100%) |
| `pitch` | string | `+0Hz` | Pitch (-50Hz / +50Hz) |

## 🌍 Mashhur ovozlar

### 🇺🇿 O'zbek
- `uz-UZ-MadinaNeural` (Ayol)
- `uz-UZ-SardorNeural` (Erkak)

### 🇺🇸 English
- `en-US-JennyNeural` (Ayol)
- `en-US-GuyNeural` (Erkak)
- `en-US-AriaNeural` (Ayol)
- `en-US-DavisNeural` (Erkak)

### 🇷🇺 Русский
- `ru-RU-SvetlanaNeural` (Женский)
- `ru-RU-DmitryNeural` (Мужской)

### 🇬🇧 British English
- `en-GB-SonaNeural` (Female)
- `en-GB-RyanNeural` (Male)

### 🇩🇪 Deutsch
- `de-DE-KatjaNeural` (Weiblich)
- `de-DE-ConradNeural` (Männlich)

### 🇫🇷 Français
- `fr-FR-DeniseNeural` (Femme)
- `fr-FR-HenriNeural` (Homme)

### 🇪🇸 Español
- `es-ES-ElviraNeural` (Mujer)
- `es-ES-AlvaroNeural` (Hombre)

### 🇹🇷 Türkçe
- `tr-TR-EmelNeural` (Kadın)
- `tr-TR-AhmetNeural` (Erkek)

### 🇸🇦 العربية
- `ar-SA-ZariyahNeural` (أنثى)
- `ar-SA-HamedNeural` (ذكر)

### 🇨🇳 中文
- `zh-CN-XiaoxiaoNeural` (女)
- `zh-CN-YunxiNeural` (男)

### 🇯🇵 日本語
- `ja-JP-NanamiNeural` (女性)
- `ja-JP-KeitaNeural` (男性)

### 🇰🇷 한국어
- `ko-KR-SunHiNeural` (여성)
- `ko-KR-InJoonNeural` (남성)

## 📱 React Native misol

```javascript
import { Audio } from 'expo-av';

async function playTTS(text, voice = 'uz-UZ-MadinaNeural') {
  const url = `https://edgettsapi.vercel.app/tts?text=${encodeURIComponent(text)}&voice=${voice}`;
  
  const { sound } = await Audio.Sound.createAsync({ uri: url });
  await sound.playAsync();
}

// Foydalanish
playTTS('Salom React Native');
```

## 🔥 Node.js misol

```javascript
const axios = require('axios');
const fs = require('fs');

async function tts(text, voice = 'uz-UZ-MadinaNeural') {
  const response = await axios({
    method: 'get',
    url: 'https://edgettsapi.vercel.app/tts',
    params: { text, voice },
    responseType: 'arraybuffer'
  });
  
  fs.writeFileSync('output.mp3', response.data);
  console.log('✅ Tayyor!');
}

tts('Salom Node.js');
```

## ⚡ Telegram Bot misoli

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests

async def tts_handler(update: Update, context):
    text = update.message.text
    
    # TTS yaratish
    response = requests.get(
        'https://edgettsapi.vercel.app/tts',
        params={'text': text, 'voice': 'uz-UZ-MadinaNeural'}
    )
    
    # Audio yuborish
    if response.status_code == 200:
        await update.message.reply_audio(audio=response.content, filename='audio.mp3')
    else:
        await update.message.reply_text('❌ Xatolik yuz berdi')

app = ApplicationBuilder().token('YOUR_TOKEN').build()
app.add_handler(MessageHandler(filters.TEXT, tts_handler))
app.run_polling()
```

## 📊 Response Format

### Muvaffaqiyatli

```
Status: 200 OK
Content-Type: audio/mpeg
Content-Disposition: attachment; filename=tts_uz-UZ-MadinaNeural.mp3

[Binary MP3 Data]
```

### Xatolik

```json
{
  "detail": "TTS xatolik: Invalid voice"
}
```

## 🎯 Rate Limits

- ✅ Limitsiz so'rovlar (hozircha)
- ✅ CORS yoqilgan
- ✅ GET va POST qo'llab-quvvatlanadi

## 📖 Ko'proq ma'lumot

- 📚 **API Docs:** https://edgettsapi.vercel.app/docs
- 📘 **ReDoc:** https://edgettsapi.vercel.app/redoc
- 💡 **Health Check:** https://edgettsapi.vercel.app/health

## 🆘 Muammolar

Muammo bo'lsa issue oching yoki PR yuboring.

---

**API Status:** ✅ Online  
**Vercel:** https://edgettsapi.vercel.app  
**Versiya:** 1.0.0
