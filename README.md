
# Smart Speech-to-Text Application

An **end-to-end pipeline** for Bengali language that performs **Automatic Speech Recognition (ASR)** followed by a **Question Answering (QA)** on the transcribed text. The goal is to take a spoken passage in Bengali, convert it to text, and answer questions asked by the user using context from that passage.

---

## Project Structure

```
IDEAS-Summer-Internship/
│
├── _pycache_
├── modules/                     # ASR,QA Modules, and Models runner
|   ├── _pycache_
│   ├── ai4bharat.py
|   ├── nous_Mistral.py
|   ├── bangla_llama,py
|   ├── bangla_bert_qa.py
|   ├── asr_module.py                  
│   └── qa_module.py           
│
├── packages.txt                 # reqd packages import                                                
│
├── evaluation/                  # evaluation notebooks
│
├── requirements.txt             # All dependencies
├── start.py                     # Entry point 
├── README.md                    # You're here
└── .env                         # (to add) HF Secrets or config
```

---

## Features

* ASR (Speech-to-Text) using Whisper / Indic-ASR (AI4Bharat)
* QA Module with support for extractive (BanglaBERT) and generative models (Mistral)
* Evaluation metrics like WER, CER, EM, F1 for both ASR and QA
* Modular and extensible: easy to plug and swap models
* Optional Streamlit-based interface for demo

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/atr86/IDEAS-Summer-Internship.git
cd IDEAS-Summer-Internship
```

### 2. Create and activate virtual environment

```bash
python -m venv ideas
source ideas/bin/activate   # Linux/Mac
ideas\Scripts\activate      # Windows
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```


```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make
```
Keep whisper-cli.exe at top of directory

```
mv build/bin/whisper-cli.exe .. #For Linux
move build/bin/whisper-cli.exe .. #For Windows CMD
```

---

## How to Run the Pipeline

```bash
streamlit run start.py
```

This will:

0. Start an Web Application at localhost:8501 
    Local URL: http://localhost:8501
    Network URL: http://192.168.0.161:8501
1. Take an audio file as input (record live or browse from local)
2. Transcribe it using the ASR module
3. Extract answer from context using QA module
4. Get the output answer

---

## Evaluation

Metrics implemented:

* Word Error Rate (WER) for ASR
* Character Error Rate (CER) for ASR
* Exact Match (EM) for QA
* F1 Score for QA

Results can be found in project report and all datasets [here](https://drive.google.com/drive/folders/1cAU_NOPho_W28c-9QUu2cZU0c0AI8qLv?usp=sharing).

You can evaluate model performance using provided evaluation notebooks in Evaluation folder or in Google drive.

---
.
## Models Used

| Task | Model                                  | Source                                                                            |
| ---- | -------------------------------------- | --------------------------------------------------------------------------------- |
| ASR  | Whisper-large-v3-gguf                  | [OpenAI](https://huggingface.co/vonjack/whisper-large-v3-gguf) |                        |
| ASR  | IndicWhisper (ai4bharat/indic-whisper) | [AI4Bharat](https://huggingface.co/ai4bharat/indicwav2vec_v1_bengali) |                      |
| QA   | BanglaBERT                             | [BanglaBERT](https://huggingface.co/doerig/banglabert)           |
| QA   | Mistral - GGUF                         | [Nous-Hermes-2-Mistral-7B](https://huggingface.co/mradermacher/Nous-Hermes-2-Mistral-7B-DPO-i1-GGUF) |
| QA   | Bangla Llama -GGUF                     | [Bangla-Llama-8B](https://huggingface.co/KillerShoaib/llama-3-8b-bangla-GGUF-Q4_K_M)|
---

---

## This project is done as part of Summer Internship at IDEAS, ISI TIH, Kolkata, by Sayan Dutta([GitHub profile](https://github.com/Sayan-Dutta-2003)) and Myself([GitHub profile](https://github.com/atr86))