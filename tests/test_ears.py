from faster_whisper import WhisperModel
import time

print("Loading Whisper Model to RTX 5090 VRAM...")
start_load = time.time()

# We are using the 'small.en' model. It is incredibly fast and highly accurate for English.
# compute_type="float16" forces it to use your GPU's tensor cores.
model = WhisperModel("small.en", device="cuda", compute_type="float16")

print(f"Model loaded in {time.time() - start_load:.2f} seconds.")
print("The 'Ears' are successfully installed and ready to listen!")
