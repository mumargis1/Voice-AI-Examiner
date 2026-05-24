# 🎙️ Local Voice-to-Voice AI Examiner (Zero-Latency, Cross-OS)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Ollama](https://img.shields.io/badge/Ollama-Llama_3.1-white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Local_RAG-orange)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An autonomous, edge-deployed Voice-to-Voice (V2V) AI Teaching Assistant designed for real-time virtual classroom examinations. Built to escape the latency, rate limits, and privacy concerns of cloud APIs, this pipeline orchestrates local Large Language Models, Vector Databases, and Speech-to-Text models across a cross-OS bridge (Windows + WSL2).

Currently configured to conduct Data Science and Python examinations in fluent, native Urdu using Microsoft Edge-TTS, but easily adaptable to any syllabus or language.

📖 **Read the full architectural deep-dive on Medium:** [Insert Medium Link Here]

## 🏗️ System Architecture

![Architecture Flow](assets/architecture.gif)

The system isolates heavy tensor computations in a Linux (WSL) container while handling complex audio routing via a lightweight Windows-native client. 

1. **The Ears (WSL):** `Faster-Whisper` with strict Voice Activity Detection (VAD) to prevent silence hallucinations.
2. **The Memory (WSL):** A local RAG pipeline utilizing `ChromaDB` and `HuggingFace Embeddings` to restrict the AI's knowledge to a specific syllabus (e.g., *Fluent Python*).
3. **The Brain (WSL):** `Llama 3.1` (via Ollama) processing the RAG-augmented prompt.
4. **The Voice (WSL):** `Edge-TTS` synthesizing the native response (`ur-PK-AsadNeural`).
5. **The Bridge (Windows):** A lightweight `sounddevice` and `pygame` client that intercepts audio from Google Meet via **VB-Audio Virtual Cable**, posts it to the WSL FastAPI backend, and broadcasts the response back to the virtual classroom with zero echo.

## 💻 Hardware Requirements
* **GPU:** Tested on an NVIDIA RTX 5090 (24GB VRAM). A minimum of 12GB VRAM is recommended to run Llama 3.1, Faster-Whisper, and the embedding models simultaneously without offloading to CPU.
* **OS:** Windows 10/11 with WSL2 (Ubuntu) installed.
* **Audio:** [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) installed on the Windows host.

## 🚀 Installation & Setup

### Part 1: The WSL Backend (Linux Environment)
Open your Ubuntu WSL terminal:

1. Clone the repository:
   ```bash
   git clone [https://github.com/mumargis1/Voice-AI-Examiner.git](https://github.com/mumargis1/Voice-AI-Examiner.git)
   cd Voice-AI-Examiner/wsl_backend