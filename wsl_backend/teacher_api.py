import time
import requests
import asyncio
import edge_tts
from faster_whisper import WhisperModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

# --- NEW RAG IMPORTS ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"
SYSTEM_PROMPT = """You are Muhammad, an expert Data Science and Python teacher. 
You are conducting a verbal examination with your student. 
You MUST reply strictly in authentic Urdu script (اردو).
Keep your responses conversational, extremely concise, and encouraging. 
Limit your responses to 2 sentences maximum."""

print("Loading Ears (Faster-Whisper - Multi-lingual)...")
whisper_model = WhisperModel("small", device="cuda", compute_type="float16")

print("Loading Memory Bank (ChromaDB RAG)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={'device': 'cuda'})
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

print("API Server Online and Ready!")

chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def ask_brain(student_text):
    global chat_history
    print(f"\n[Brain] Thinking about: '{student_text}'...")
    
    # --- RAG MAGIC HAPPENS HERE ---
    # 1. Search the database for the 3 most relevant paragraphs to the student's speech
    docs = vector_db.similarity_search(student_text, k=3)
    retrieved_context = "\n\n".join([doc.page_content for doc in docs])
    print(retrieved_context)
    print(f"[RAG] Found relevant context from syllabus!")
    
    # 2. Secretly inject the textbook info into the prompt
    augmented_prompt = f"""
    Use the following REFERENCE MATERIAL from the course syllabus to evaluate the student or answer their question. 
    If the answer is not in the material, gently tell them it is outside the scope of the course.
    
    REFERENCE MATERIAL:
    {retrieved_context}
    
    STUDENT SAYS:
    {student_text}
    """
    
    chat_history.append({"role": "user", "content": augmented_prompt})
    
    payload = {
        "model": "llama3.1",
        "messages": chat_history,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        teacher_reply = response.json()['message']['content']
        chat_history.append({"role": "assistant", "content": teacher_reply})
        
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]
            
        return teacher_reply
    else:
        chat_history.pop()
        return "معذرت، مجھے سمجھ نہیں آیا۔"

@app.post("/chat")
async def chat_endpoint(audio: UploadFile = File(...)):
    start_time = time.time()
    
    with open("temp_student.wav", "wb") as f:
        f.write(await audio.read())
        
    segments, _ = whisper_model.transcribe("temp_student.wav", language="ur", vad_filter=True)
    student_text = "".join([segment.text for segment in segments])
    print(f"\n[Student Said]: {student_text}")
    
    teacher_reply = ask_brain(student_text)
    print(f"[Teacher AI]: {teacher_reply}")
    
    filename = "temp_teacher.mp3"
    communicate = edge_tts.Communicate(teacher_reply, "ur-PK-AsadNeural")
    await communicate.save(filename)
    
    print(f"[System] Total API Latency: {time.time() - start_time:.2f} seconds.")
    return FileResponse(filename)
