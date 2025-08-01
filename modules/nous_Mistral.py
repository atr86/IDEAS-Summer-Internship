import streamlit as st
import os
from llama_cpp import Llama
try:
    import gdown
except ImportError:
        os.system("pip install gdown")
        import gdown
file_id = "1mulUley1DZw7kMVYbEcCTvOOXBb7uGB1"
url = f"https://drive.google.com/uc?id={file_id}"
local_model_path="E:/Python/streamlit/v1/Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf"

if not os.path.exists(local_model_path):
    with st.spinner("Model Nous-Hermes-2-Mistral not found locally. Downloading from Google Drive..."):
            gdown.download(url, local_model_path, quiet=False)
    st.success("Model downloaded successfully!")
else:
    print("Model found locally. Using existing file.")



#  Load GGUF model from local path
llm = Llama(
        model_path="Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6           # Adjust to your CPU cores
    )

def init_for_out():
    from llama_cpp import Llama
    #  Load GGUF model from local path
    llm = Llama(
        model_path="Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6           # Adjust to your CPU cores
    )

def getResponse(question,context):
    #  Create a chat-style prompt using create_chat_completion
    response= llm.create_chat_completion(
            messages=[
                {
                    "role": "system",#framed in 1 sentence
                    "content": "Below is a question and a context in bengali language. Frame a simple sentence containing the most matching keyword from the context that directly answers the question. Do not generate more than 1 keyword or more than 1 sentence."
                },
                {
                    "role": "user",
                    "content": question + "\n\n" + context + "\n\nanswer:"
                }
            ],
            max_tokens=300,
            temperature=0.1,  # Min temperature for more deterministic output
            top_p=0.9
        )
    return response["choices"][0]["message"]["content"]


def run(question,context):   
    init_for_out()
    text=getResponse(question,context)
    return text
