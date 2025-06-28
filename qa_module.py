def show_qa_tab():
    from transformers import pipeline
    import streamlit as st

    #Global var
    model_options = ["deepset/roberta-base-squad2", "distilbert-base-uncased-distilled-squad"]
    model_labels = {
        "deepset/roberta-base-squad2":"Deepset", 
        "distilbert-base-uncased-distilled-squad":"Distilbert"
        
    }
    model_links = {
        "deepset/roberta-base-squad2":"https://huggingface.co/deepset/roberta-base-squad2",
          "distilbert-base-uncased-distilled-squad":"https://huggingface.co/distilbert-base-uncased-distilled-squad"
    }

    # Load QA pipeline with a pretrained model
    def set_pipeline(model_option):
        qa = pipeline("question-answering", model=model_option)
        return qa

    #Select model
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

    
    #select model
    selected_model=select_model()
    link=model_links.get(selected_model, "#")
    st.markdown(f'##### Chosen Model Name:- **{selected_model}**')
    st.markdown(f'''Visit:- 
                <a href="{link}" target="_blank">
                _{selected_model}_ </a>''', unsafe_allow_html=True)

    # Input passage (context)
    #context = st.text_area("Enter a piece of text")

    context=st.session_state.text
    st.text_area(label=f"Your transcribed text is",value=context,height=100)


    # Your question
    question = st.text_input("Enter your question")

    if st.button(f"Answer", key=f"btn2{0}"):
    # Perform extractive QA
        qa = set_pipeline(selected_model)
        result = qa(question=question, context=context)

        # Print answer
        st.text_area(f"Answer:",value=result["answer"],height=68)
        st.text_area("More Details:",value=result,height=68)
        #print(type(result)) od dict type

    else:
        st.info("Please enter question and click Answer button")



