from llama_cpp import Llama
import streamlit as st
import os

try:
    import gdown
except ImportError:
        os.system("pip install gdown")
        import gdown
file_id = "1uYktTEF8EaHdYrGkx8DSWe0aPu49P43x"
url = f"https://drive.google.com/uc?id={file_id}"
local_model_path="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf"

if not os.path.exists(local_model_path):
    with st.spinner("Model llama-3-8b-bangla not found locally. Downloading from Google Drive..."):
            gdown.download(url, local_model_path, quiet=False)
    st.success("Model downloaded successfully!")
else:
    print("Model found locally. Using existing file.")

#  Load GGUF model from local path
llm = Llama(
        model_path="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6         # Adjust to your CPU cores
    )


def init_for_out():
    
    from llama_cpp import Llama
    import streamlit as st
    import os
    #  Load GGUF model from local path
    llm = Llama(
        model_path="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6           # Adjust to your CPU cores
    )

def getResponse(prompt,question,context):
    #  Create a chat-style prompt using create_chat_completion
    response= llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": question + "\n\n" + context + "\n\nanswer:"
                }
            ],
            max_tokens=300,
            temperature=0,
            top_p=0.9
        )
    return response["choices"][0]["message"]["content"]

# if __name__ == "__main__":


def run(question,context):
    init_for_out()
    prompt = "Below is a question and a context in bengali language. Frame in a simple sentence containing the most matching keyword from the context that directly answers the question. Do not generate more than 1 keyword or more than 1 sentence."
    text=getResponse(prompt,question,context)
    return text


