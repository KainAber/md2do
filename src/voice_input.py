import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

def get_voice_input():
    r = sr.Recognizer()
    r.pause_threshold = 5.0
    
    with sr.Microphone() as source:
        logger.info("Listening... (speak now)")
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            text = r.recognize_google(audio)
            logger.info(f"Transcribed: '{text}'")
            return text
        except sr.WaitTimeoutError:
            logger.info("No speech detected")
            return None
        except sr.UnknownValueError:
            logger.info("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            return None 