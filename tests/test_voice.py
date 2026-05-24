import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import time

print("Loading Parler-TTS Model to RTX 5090 VRAM...")
start_load = time.time()

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model_id = "parler-tts/parler-tts-mini-v1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_id)

print(f"Model loaded in {time.time() - start_load:.2f} seconds.")

# 1. The text the AI will actually speak out loud
prompt = "Excellent job! You correctly identified that setting the nodata value to minus nine thousand nine hundred and ninety nine prevents overlapping class IDs in your exported rasters."

# 2. The description of HOW they should sound
description = "A male speaker with a calm, clear, and educational voice delivers a positive response at a moderate pace."

print("\nGenerating audio (Watch the GPU fly)...")
start_gen = time.time()

# Tokenize inputs
input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

# Generate the audio array
generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()

# Save the file
sf.write("teacher_response.wav", audio_arr, model.config.sampling_rate)

print(f"Audio generated and saved in {time.time() - start_gen:.2f} seconds!")
print("Check your folder for 'teacher_response.wav'.")
