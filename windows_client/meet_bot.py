import sounddevice as sd
import soundfile as sf
import requests
import pygame
import time
import os

# This points to your WSL Linux API Server!
API_URL = "http://127.0.0.1:8000/chat"
RECORD_SECONDS = 8  # How long to record the student's answer
FS = 16000

print("\nInitializing Windows Audio Engine...")
pygame.mixer.init()

print("="*50)
print("AI EXAMINER: WINDOWS CLIENT ONLINE")
print("="*50)

while True:
    input("\nPress ENTER to capture the student's voice (8-second recording)...")
    print("\n[Listening...] Speak now!")
    
    # 1. Record the microphone
    # 1. Record the microphone
    myrecording = sd.rec(int(RECORD_SECONDS * FS), samplerate=FS, channels=1, device=1)
    sd.wait()
    
    # 2. Save the recording temporarily
    sf.write('temp_student_windows.wav', myrecording, FS)
    print("[Transmitting to RTX 5090 WSL Brain...]")
    
    # 3. Send over the local network to WSL
    try:
        with open('temp_student_windows.wav', 'rb') as f:
            files = {'audio': ('student_windows.wav', f, 'audio/wav')}
            response = requests.post(API_URL, files=files)
            
        if response.status_code == 200:
            print("[Success!] AI generated a response. Playing audio...")
            
            # Save the AI's MP3 response
            with open('temp_teacher_windows.mp3', 'wb') as out_f:
                out_f.write(response.content)
            
            # 4. Play the audio 
            pygame.mixer.music.load('temp_teacher_windows.mp3')
            pygame.mixer.music.play()
            
            # Wait for the AI to finish speaking
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.music.unload()
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Connection failed! Is the WSL Uvicorn server running? Error: {e}")