import os
import torch
import librosa
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def import_pkg():
    import os
    import torch
    import librosa
    import numpy as np
    from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

# Avoid tokenizer parallel warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load model and processor
def load_stt_model():
    processor = Wav2Vec2Processor.from_pretrained("ai4bharat/indicwav2vec_v1_bengali")
    model = Wav2Vec2ForCTC.from_pretrained("ai4bharat/indicwav2vec_v1_bengali")
    return processor, model

# Preprocess audio and transcribe
def transcribe(audio_path, processor, model):
    # Load audio
    speech_array, sampling_rate = librosa.load(audio_path, sr=16000)
    
    # Convert to tensor
    input_values = processor(speech_array, sampling_rate=16000, return_tensors="pt", padding="longest").input_values

    # Forward pass
    with torch.no_grad():
        logits = model(input_values).logits

    # Decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription

# Example usage
if __name__ == "__main__":
            import_pkg()
    #for i in range(1, 7):
            audio_file = f"{7}.wav"  # Replace with your audio file path

            processor, model = load_stt_model()
            text = transcribe(audio_file, processor, model)
            print("Transcription:", text)
            file_name = f"{audio_file}Ai4bharat.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Transcription saved to {file_name}")
            # Note: Ensure you have the required audio file in the same directory or provide the correct path.
            # Make sure to install the required packages:
            # pip install torch transformers librosa
            # If you encounter issues with torch, you may need to install a specific version compatible with your system.
            # For example, use `pip install torch>=2.6.0` if you have CUDA support.

def run(audio_path):
     import_pkg()
     processor, model = load_stt_model()
     text = transcribe(audio_path, processor, model)
     return text
