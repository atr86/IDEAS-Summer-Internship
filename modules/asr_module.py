import io


def show_asr_tab():
    import streamlit as st
    import tempfile
    import os
    #from transformers import pipeline
    import time as time
    #import torch
    #from whisper_cpp_python import Whisper
    
    #print(os.environ['PATH'])
    
    
    def AI4Bharat(audio_path,gguf=False):
        from modules.ai4bharat import run
        text=run(audio_path)
        return text
    
    try:
        import gdown
    except ImportError:
        os.system("pip install gdown")
        import gdown
    file_id = "1IaH_PPk8e02Imf_Wf6m4WrVsUSGQNu5A"
    url = f"https://drive.google.com/uc?id={file_id}"
    local_model_path = "whisper-large-v3-q8_0.gguf"
    
    
    if not os.path.exists(local_model_path):
        with st.spinner("whisper-large-v3-q8_0.gguf model not found locally. Downloading from Google Drive..."):
            gdown.download(url, local_model_path, quiet=False)
        st.success("Model downloaded successfully!")
    else:
        print("Model already exists locally.")
    
    
    def Whisper_Large_v3(audio_path, gguf=True):

        # whisper_model = Whisper("whisper-large-v3-q8_0.gguf")
        # result = whisper_model.transcribe(audio_path)
        # return result["text"]
        # return "Dummy" ---this is method 1--- using whisper_cpp_python

        output_prefix = audio_path
        output_file = f"{output_prefix}.txt"
        env = set_path()  # Your function to set PATH


        import subprocess
        # Method 2: Using whisper-cli
        # Check if whisper-cli binary exists, if not download it
        binary_path="whisper-cli.exe"
        if not os.path.exists(binary_path):
            file_id1 = "1qS9facmYvpnzI5J_6N5rJ-v3HNtOAhJq"
            url = f"https://drive.google.com/uc?id={file_id1}"
            with st.spinner("whisper-cli not found locally. Downloading from Google Drive..."):
                gdown.download(url, binary_path, quiet=False)
                os.chmod("whisper-cli.exe", 0o755)
            st.success("whisper-cli downloaded successfully!")
        else:
            print("Model already exists locally.")

        cmd = [
            "whisper-cli.exe",#for windows
            "-m", "whisper-large-v3-q8_0.gguf",
            "-f", audio_path,
            "--language", "bn",
            "-otxt",
            "-of", output_prefix
        ]

        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file was not created: {output_file}")

        with open(output_file, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    

    #Global var
    hf_options = ["ai4bharat/indicwav2vec_v1_bengali"]
    hf_labels = {"ai4bharat/indicwav2vec_v1_bengali": "IndicWav2Vec - AI4Bharat Bengali"}
    hf_fn = {
        "ai4bharat/indicwav2vec_v1_bengali": AI4Bharat
    }


    gguf_options=["whisper-large-v3-q8_0"]
    gguf_labels = {
    "whisper-large-v3-q8_0": "Whisper-large-V3-Q8_0"
    }
    gguf_fn = {
        "whisper-large-v3-q8_0": Whisper_Large_v3
    }   
    

    def set_path():
        # Copy existing env
        env = os.environ.copy()

        # Replace PATH with the working Command Prompt PATH
        env["PATH"] = (
            r"C:\mingw64-new\bin;"
            r"C:\Program Files\Common Files\Oracle\Java\javapath;"
            r"C:\Program Files (x86)\Common Files\Oracle\Java\java8path;"
            r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath;"
            r"C:\Windows\system32;"
            r"C:\Windows;"
            r"C:\Windows\System32\Wbem;"
            r"C:\Windows\System32\WindowsPowerShell\v1.0\;"
            r"C:\Windows\System32\OpenSSH\;"
            r"C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;"
            r"C:\MinGW\bin;"
            r"C:\Program Files\Git\cmd;"
            r"C:\Program Files\BlueJ\jdk\bin;"
            r"E:\Python\bin;"
            r"C:\Program Files\CMake\bin;"
            r"C:\Users\abc\AppData\Local\Programs\Python\Python313\Scripts\;"
            r"C:\Users\abc\AppData\Local\Programs\Python\Python313\;"
            r"C:\Users\abc\AppData\Local\Microsoft\WindowsApps;"
            r"C:\Users\abc\AppData\Local\Programs\Microsoft VS Code\bin;"
            r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.3.3\bin;"
            r"C:\Users\abc\AppData\Local\Programs\Ollama;"
                      )
        return env
        return env


    def transcription(audio_path, category, model_option):
        if category == "Original HF models":
            text=hf_fn[model_option](audio_path)
            return text
            # p = pipeline("automatic-speech-recognition", model=model_option)
            # return p(audio_path, return_timestamps=True)["text"]

        elif category == "Local GGUF models":
            text=gguf_fn[model_option](audio_path,gguf=True)
            return text


    def select_model(selected_type="Original HF models"):
        """
        Display a selectbox for model selection and return the selected model name as a string.
        """
        #Choose models based on category
        if selected_type == "Original HF models":
            selected_model = st.selectbox(
            "Select Hugging Face model:",
            hf_options,
            format_func=lambda x: hf_labels[x],
            key=1,
            )
        else:
            selected_model = st.selectbox(
                "Select local GGUF model:",
            gguf_options,
            format_func=lambda x: gguf_labels[x],
            key=2,
        )
        
        return selected_model
    
    

    # Initialize session state for uploaded files
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    # Initialize session state for text
    if 'text' not in st.session_state:
        st.session_state.text = ''

    if 'no_of_rec' not in st.session_state:
        st.session_state.no_of_rec= 0

    # File uploader for audio files
    uploaded_files = st.file_uploader(
        "Upload Audio File(s)", 
        type=["wav", "mp3", "flac"], 
        accept_multiple_files=True
    )

    # Add newly uploaded files to session state (avoid duplicates)
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f.name for f in st.session_state.uploaded_files]:
                st.session_state.uploaded_files.append(file)
        #Manually Cancel after uploading audio
        st.info("Please remove your recorded voice using inbuilt ✖ button")

    st.markdown('##### Or')
    #Record voice and upload

    audio_value = st.audio_input("Record a voice message")
    if audio_value:
        st.audio(audio_value)
        # Give a custom name (e.g., use a timestamp or counter for uniqueness)
        custom_name = f"mic_recording_{st.session_state.no_of_rec}.wav"
        st.session_state.no_of_rec += 1

        # Wrap the audio bytes in a BytesIO object and set a name attribute
        audio_file = io.BytesIO(audio_value.getvalue())
        audio_file.name = custom_name

        # Only add if not already in uploaded_files
        if audio_file.name not in [f.name for f in st.session_state.uploaded_files]:
            st.session_state.uploaded_files.append(audio_file)
        
        #Manually Cancel after uploading audio
        st.info("Please remove your recorded voice using inbuilt 🗑 button")
    
    
    
    
    
    categories = ["Original HF models", "Local GGUF models"]
    # Select category first
    selected_category = st.selectbox("Choose model category:", categories,key="asr_cat")

    model_option=select_model(selected_category)

    st.markdown(f'Model name:- **{model_option}**')

    if st.session_state.uploaded_files:
        st.markdown("### 🗂️ Audio Files")
        for i, file in enumerate(st.session_state.uploaded_files):
            st.markdown(f"**{i+1}. {file.name}**")
            st.audio(file, format="audio/wav")
            # Delete button for each file
            if st.button(f"Delete", key=f"del{i}"):
                st.session_state.uploaded_files.pop(i)
                st.rerun()  

            # Button to transcribe each file
            if st.button(f"Transcribe", key=f"btn{i}"):
                # Save the file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(file.read())
                    temp_path = temp_file.name

                # Simulate transcription process
                with st.spinner("Transcribing..."):
                
                    st.session_state.text = transcription(temp_path,selected_category,model_option)
                    st.text_area(
                        f"Transcription for {file.name}", 
                        value=st.session_state.text, 
                        height=150
                                 )
                

                # Clean up the temporary file
                os.remove(temp_path)
    else:
        st.info("Record or Upload Audio files to begin transcription.")


