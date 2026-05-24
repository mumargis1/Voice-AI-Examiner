import time
import requests
import asyncio
import edge_tts
from faster_whisper import WhisperModel

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/chat"

# We now force the AI to write in actual Urdu so the voice engine pronounces it perfectly
SYSTEM_PROMPT = """You are Muhammad, an expert Data Science and Python teacher. 
You are conducting a verbal examination with your student. 
You MUST reply strictly in authentic Urdu script (اردو). Do NOT use Roman Urdu or English letters.
Keep your responses conversational, extremely concise, and encouraging. 
Limit your responses to 2 sentences maximum."""

print("Initializing AI Examiner Core System...")

# --- 1. LOAD THE EARS (Whisper) ---
print("Loading Ears (Faster-Whisper)...")
whisper_model = WhisperModel("small.en", device="cuda", compute_type="float16")

print("\n--- ALL SYSTEMS ONLINE. RTX 5090 IS READY. ---")

def ask_brain(student_text):
    """Sends the student's text to the local Llama 3.1 model."""
    print(f"\n[Brain] Thinking about: '{student_text}'...")
    payload = {
        "model": "llama3.1",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": student_text}
        ],
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        return "معذرت، مجھے سمجھ نہیں آیا۔" # "Sorry, I didn't understand."

def generate_voice(ai_text, filename="latest_response.mp3"):
    """Converts Urdu text to a flawless Pakistani accent using Edge-TTS."""
    print(f"[Voice] Generating Urdu audio for: '{ai_text}'...")
    
    async def _generate():
        # ur-PK-AsadNeural is a native Pakistani male voice
        # ur-PK-UzmaNeural is a native Pakistani female voice
        communicate = edge_tts.Communicate(ai_text, "ur-PK-AsadNeural")
        await communicate.save(filename)
        
    asyncio.run(_generate())
    print(f"[Voice] Saved to {filename}")

# --- MAIN EXAM LOOP ---
while True:
    print("\n" + "="*50)
    user_input = input("Student (Type your answer, or 'quit' to exit): ")
    
    if user_input.lower() in ['quit', 'exit']:
        print("Ending examination...")
        break
        
    start_time = time.time()
    
    # 1. Send to Brain
    teacher_reply = ask_brain(user_input)
    
    # 2. Send to Voice
    generate_voice(teacher_reply)
    
    total_time = time.time() - start_time
    print(f"\n[System] Total Latency: {total_time:.2f} seconds.")
    print(f"Teacher AI Says: {teacher_reply}")
