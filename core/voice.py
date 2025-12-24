import threading, time
import speech_recognition as sr
import pyttsx3

class VoiceAssistant:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self._listener_thread = None
        self._stop_evt = threading.Event()
        self.engine = pyttsx3.init()
        if cfg.get("VOICE_TTS") and cfg.get("VOICE_TTS") != "auto":
            for v in self.engine.getProperty('voices'):
                if cfg["VOICE_TTS"].lower() in (v.id.lower(), v.name.lower()):
                    self.engine.setProperty('voice', v.id)
                    break

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def _listen_loop(self, gpt, memory):
        r = sr.Recognizer()
        mic = sr.Microphone()
        wake = self.cfg.get("WAKE_WORD", "jarvis").lower()
        with mic as source:
            r.adjust_for_ambient_noise(source)
        while not self._stop_evt.is_set():
            try:
                with mic as source:
                    audio = r.listen(source, phrase_time_limit=6)
                text = r.recognize_google(audio).lower()
                if wake in text:
                    self.speak("Yes?")
                    with mic as source:
                        audio2 = r.listen(source, phrase_time_limit=6)
                    try:
                        prompt = r.recognize_google(audio2)
                        reply = gpt.chat(prompt, memory=memory)
                        print(f"\n[Voice] You: {prompt}\n[Jarvis]: {reply}")
                        self.speak(reply)
                    except Exception as e:
                        print("[Voice] error:", e)
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print("[Voice] error:", e)
            time.sleep(0.1)

    def start_background_listener(self, gpt, memory):
        if self._listener_thread and self._listener_thread.is_alive():
            return
        self._stop_evt.clear()
        self._listener_thread = threading.Thread(target=self._listen_loop, args=(gpt, memory), daemon=True)
        self._listener_thread.start()

    def stop_background_listener(self):
        self._stop_evt.set()
