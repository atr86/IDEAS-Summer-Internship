
def show_qa_tab():
    #from transformers import pipeline
    import streamlit as st    

    def Nous_Hermes_Mistral_7B(question, context):
        from modules.nous_Mistral import run
        return run(question, context)
    
    def Bangla_BERT_QA(question, context):
        from modules.bangla_bert_qa import run
        return run(question, context)
    
    def Bangla_Llama_3_8B(question, context):
        from modules.bangla_llama import run
        return run(question, context)
    

    #Global var
    hf_options = ["doerig/banglabert"]
    hf_labels = {"doerig/banglabert": "Bangla-BERT-QA"}
    
    hf_fn = {"doerig/banglabert": Bangla_BERT_QA}

    gguf_options=["Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf","llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf"]
    gguf_labels = {"Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf":"Nous-Hermes-Mistral Q4",
        "llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf":"Bangla-Llama-Q4"
    }
    gguf_fn = {
        "Nous-Hermes-2-Mistral-7B-DPO.i1-Q4_K_M.gguf":Nous_Hermes_Mistral_7B,
       "llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf": Bangla_Llama_3_8B
    }   
    

    
    def qa(category,model_option,context, qs):
        if category == "Original HF models":
            text=hf_fn[model_option](context, qs)
            return text

        elif category == "Local GGUF models":
            text=gguf_fn[model_option](context, qs)
            return text

    #Select model
    def select_model(selected_type="Original HF models"):
        """
        Display a selectbox for model selection and return the selected model name as a string.
        """
        # Choose models based on category
        if selected_type == "Original HF models":
            selected_model = st.selectbox(
            "Select model from Hugging Face :",
            hf_options,
            format_func=lambda x: hf_labels.get(x, x),
            key=3,
            )
        else:
            selected_model = st.selectbox(
                "Select model from GGUF files:",
            gguf_options,
            format_func=lambda x: gguf_labels.get(x, x),
            key=4,
        )
        return selected_model

    
    categories = ["Original HF models", "Local GGUF models"]
    # Select category first
    selected_category = st.selectbox("Choose model category:", categories,key="qa_category")

    selected_model=select_model(selected_category)

    st.markdown(f'Model name:- **{selected_model}**')


    context=st.session_state.text
    st.text_area(label=f"Your transcribed text is",value=context,height=100)
    #st.code(context, language="text", height=150)


    # Your question
    question = st.text_input("Enter your question")
    #st.code(question,language="text",height=65)

    if st.button(f"Answer", key=f"btn2{0}"):
    # Perform extractive QA
        
        result = qa(selected_category, selected_model, question,context)

        # Print answer
        st.text_area(f"Answer:",value=result,height=68)
        #st.code(result, language="text",height=100)
        #st.text_area("More Details:",value=result,height=68)
        #print(type(result)) of  dict type

    else:
        st.info("Please enter question and click Answer button")







