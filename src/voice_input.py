import speech_recognition as sr
import whisper
import tempfile
import os
import logging

logger = logging.getLogger(__name__)


def get_voice_input():
    r = sr.Recognizer()

    r.energy_threshold = 300
    r.dynamic_energy_threshold = False
    r.pause_threshold = 2.0

    with sr.Microphone() as source:
        logger.info("Listening... (speak now)")
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=None)
            logger.debug("Audio recorded, transcribing with Whisper...")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name

            with open(temp_path, "wb") as f:
                f.write(audio.get_wav_data())

            model = whisper.load_model("base")
            result = model.transcribe(temp_path, fp16=False, language="en")
            text = result["text"].strip()

            os.remove(temp_path)

            if text:
                logger.debug(f"Transcribed: '{text}'")
                return text
            else:
                logger.debug("No speech detected")
                return None

        except sr.WaitTimeoutError:
            logger.debug("No speech detected")
            return None
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            return None
