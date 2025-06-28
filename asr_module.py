import io


def show_asr_tab():
    import streamlit as st
    import tempfile
    import os
    from transformers import pipeline
    import time as time



    
    #Global var
    model_options = ["openai/whisper-small", "facebook/wav2vec2-base-960h"]
    model_labels = {
        "openai/whisper-small": "Whisper Small",
        "facebook/wav2vec2-base-960h": "Wav2Vec2"
    }
    model_links = {
        "openai/whisper-small": "https://huggingface.co/openai/whisper-small",
        "facebook/wav2vec2-base-960h": "https://huggingface.co/facebook/wav2vec2-base-960h"
    }

    # App Title
    #st.title("🎙️ Speech to Text Project")

    # transcription function for demonstration
    def transcription(audio_path,model_option="openai/whisper-small",):
        p=pipeline("automatic-speech-recognition",model=model_option) #for all models
        return p(audio_path, return_timestamps=True)["text"]

    def select_model():
        """
        Display a selectbox for model selection and return the selected model name as a string.
        """
    
        selected = st.selectbox(
            "Select a speech recognition model:",
        model_options,
            format_func=lambda x: model_labels[x]
        )
        return selected

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
    
    

    model_option=select_model()
    link=model_links.get(model_option, "#")
    st.markdown(f'Model name:- **{model_option}**')
    st.markdown(f'''Visit:- 
                <a href="{link}" target="_blank">
                _{model_option}_ </a>''', unsafe_allow_html=True)

    # Display the list of uploaded audio files
    if st.session_state.uploaded_files:
        st.markdown("### 🗂️ Audio Files")
        for i, file in enumerate(st.session_state.uploaded_files):
            st.markdown(f"**{i+1}. {file.name}**")
            st.audio(file, format="audio/wav")
            # Delete button for each file
            if st.button(f"Delete {file.name}", key=f"del{i}"):
                st.session_state.uploaded_files.pop(i)
                st.rerun()  

            # Button to transcribe each file
            if st.button(f"Transcribe {file.name}", key=f"btn{i}"):
                # Save the file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(file.read())
                    temp_path = temp_file.name

                # Simulate transcription process
                with st.spinner("Transcribing..."):
                
                    st.session_state.text = transcription(temp_path,model_option)
                    st.text_area(
                        f"Transcription for {file.name}", 
                        value=st.session_state.text, 
                        height=150
                                 )
                

                # Clean up the temporary file
                os.remove(temp_path)
    else:
        st.info("Record or Upload Audio files to begin transcription.")


