from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional, List
import edge_tts
import io
import asyncio
from pydantic import BaseModel

app = FastAPI(
    title="Edge-TTS API",
    description="Professional Text-to-Speech API using Microsoft Edge TTS",
    version="1.0.0"
)

# Models
class VoiceInfo(BaseModel):
    name: str
    short_name: str
    gender: str
    locale: str
    suggested_codec: str
    friendly_name: str
    status: str

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "uz-UZ-MadinaNeural"
    rate: Optional[str] = "+0%"
    volume: Optional[str] = "+0%"
    pitch: Optional[str] = "+0Hz"

# Cache for voices
voices_cache = None

async def get_all_voices():
    """Get all available voices from Edge-TTS"""
    global voices_cache
    if voices_cache is None:
        voices = await edge_tts.list_voices()
        voices_cache = voices
    return voices_cache

@app.get("/", tags=["Info"])
async def root():
    """API ma'lumotlari"""
    return {
        "message": "Edge-TTS API",
        "version": "1.0.0",
        "endpoints": {
            "tts": "/tts?text=...&voice=...&rate=...&volume=...&pitch=...",
            "voices": "/voices",
            "voices_by_language": "/voices/{language}",
            "voice_info": "/voice/{voice_name}",
            "languages": "/languages",
            "health": "/health"
        },
        "example": "/tts?text=Salom dunyo&voice=uz-UZ-MadinaNeural&rate=+20%&volume=+10%"
    }

@app.get("/health", tags=["Info"])
async def health_check():
    """API health check"""
    return {"status": "healthy", "service": "Edge-TTS API"}

@app.get("/tts", tags=["TTS"])
async def text_to_speech(
    text: str = Query(..., description="Matn (TTS uchun)", min_length=1),
    voice: str = Query("uz-UZ-MadinaNeural", description="Ovoz nomi"),
    rate: str = Query("+0%", description="Tezlik (-50% dan +100% gacha)"),
    volume: str = Query("+0%", description="Ovoz balandligi (-50% dan +100% gacha)"),
    pitch: str = Query("+0Hz", description="Pitch (-50Hz dan +50Hz gacha)")
):
    """
    Text-to-Speech konvertatsiya
    
    Parametrlar:
    - text: Konvertatsiya qilinadigan matn
    - voice: Ovoz nomi (default: uz-UZ-MadinaNeural)
    - rate: Tezlik (default: +0%, masalan: +20%, -10%)
    - volume: Ovoz balandligi (default: +0%, masalan: +50%, -25%)
    - pitch: Balandlik (default: +0Hz, masalan: +10Hz, -5Hz)
    
    Misol: /tts?text=Salom&voice=uz-UZ-MadinaNeural&rate=+20%&volume=+10%
    """
    try:
        # TTS yaratish
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )
        
        # Audio ma'lumotlarini yig'ish
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        # Boshiga qaytarish
        audio_data.seek(0)
        
        # Audio faylni qaytarish
        return StreamingResponse(
            audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=tts_{voice}.mp3"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS xatolik: {str(e)}")

@app.post("/tts", tags=["TTS"])
async def text_to_speech_post(request: TTSRequest):
    """
    POST metodi bilan TTS (JSON body)
    
    Body:
    {
        "text": "Salom dunyo",
        "voice": "uz-UZ-MadinaNeural",
        "rate": "+0%",
        "volume": "+0%",
        "pitch": "+0Hz"
    }
    """
    try:
        communicate = edge_tts.Communicate(
            text=request.text,
            voice=request.voice,
            rate=request.rate,
            volume=request.volume,
            pitch=request.pitch
        )
        
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        audio_data.seek(0)
        
        return StreamingResponse(
            audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=tts_{request.voice}.mp3"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS xatolik: {str(e)}")

@app.get("/voices", tags=["Voices"])
async def get_voices(
    language: Optional[str] = Query(None, description="Til bo'yicha filter (uz-UZ, en-US, ru-RU, ...)")
):
    """
    Barcha mavjud ovozlar ro'yxati
    
    Parametr:
    - language: Til kodi (optional) - masalan: uz-UZ, en-US, ru-RU
    
    Misol: /voices?language=uz-UZ
    """
    try:
        voices = await get_all_voices()
        
        if language:
            voices = [v for v in voices if v["Locale"].lower().startswith(language.lower())]
        
        result = []
        for voice in voices:
            result.append({
                "name": voice["Name"],
                "short_name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"],
                "suggested_codec": voice["SuggestedCodec"],
                "friendly_name": voice["FriendlyName"],
                "status": voice["Status"]
            })
        
        return {
            "total": len(result),
            "voices": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

@app.get("/voices/{language}", tags=["Voices"])
async def get_voices_by_language(language: str):
    """
    Til bo'yicha ovozlar ro'yxati
    
    Misol: /voices/uz-UZ, /voices/en-US, /voices/ru-RU
    """
    try:
        voices = await get_all_voices()
        filtered = [v for v in voices if v["Locale"].lower().startswith(language.lower())]
        
        if not filtered:
            raise HTTPException(status_code=404, detail=f"'{language}' tili uchun ovoz topilmadi")
        
        result = []
        for voice in filtered:
            result.append({
                "name": voice["Name"],
                "short_name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"],
                "friendly_name": voice["FriendlyName"]
            })
        
        return {
            "language": language,
            "total": len(result),
            "voices": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

@app.get("/voice/{voice_name}", tags=["Voices"])
async def get_voice_info(voice_name: str):
    """
    Bitta ovoz haqida to'liq ma'lumot
    
    Misol: /voice/uz-UZ-MadinaNeural
    """
    try:
        voices = await get_all_voices()
        voice = next((v for v in voices if v["ShortName"] == voice_name or v["Name"] == voice_name), None)
        
        if not voice:
            raise HTTPException(status_code=404, detail=f"'{voice_name}' ovozi topilmadi")
        
        return {
            "name": voice["Name"],
            "short_name": voice["ShortName"],
            "gender": voice["Gender"],
            "locale": voice["Locale"],
            "suggested_codec": voice["SuggestedCodec"],
            "friendly_name": voice["FriendlyName"],
            "status": voice["Status"],
            "voice_tag": voice.get("VoiceTag", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

@app.get("/languages", tags=["Voices"])
async def get_languages():
    """Barcha mavjud tillar ro'yxati"""
    try:
        voices = await get_all_voices()
        locales = sorted(set(v["Locale"] for v in voices))
        
        languages = {}
        for locale in locales:
            count = len([v for v in voices if v["Locale"] == locale])
            languages[locale] = {
                "locale": locale,
                "voice_count": count
            }
        
        return {
            "total_languages": len(languages),
            "languages": languages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

@app.get("/uzbek-voices", tags=["Voices"])
async def get_uzbek_voices():
    """O'zbek tilida mavjud ovozlar"""
    try:
        voices = await get_all_voices()
        uzbek_voices = [v for v in voices if v["Locale"].startswith("uz")]
        
        result = []
        for voice in uzbek_voices:
            result.append({
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "friendly_name": voice["FriendlyName"]
            })
        
        return {
            "language": "Uzbek",
            "total": len(result),
            "voices": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """API ishga tushganda ovozlarni yuklash"""
    await get_all_voices()
    print("✅ Edge-TTS API tayyor!")
    print("📝 Dokumentatsiya: http://localhost:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)