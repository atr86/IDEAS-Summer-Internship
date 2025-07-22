from llama_cpp import Llama
#  Load GGUF model from local path
llm = Llama(
        model_path="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6         # Adjust to your CPU cores
    )
# llm = Llama.from_pretrained(
# 	repo_id="asif00/bangla-llama-1B-gguf-16bit",
# 	filename="unsloth.F16.gguf",
#      )


def init_for_out():
    from llama_cpp import Llama
    #  Load GGUF model from local path
    # !pip install llama-cpp-python

    from llama_cpp import Llama

    # llm = Llama.from_pretrained(
	# repo_id="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf",
	# filename="unsloth.F16.gguf",
    #  )

    llm = Llama(
        model_path="llama-3-8b-bangla-GGUF-Q4_K_M-unsloth.Q4_K_M.gguf",
        n_ctx=4096,           # Context size (increase if needed)
        n_threads=6       # Adjust to your CPU cores
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
#     for i in range(1, 2):
#         with open(f"qa{i}.txt", "r", encoding="utf-8") as f:
#             #  Read the question and context from the file
#             lines = f.readlines()
#             question = lines[0].strip()
#             context = "".join(lines[1:]).strip()
#         prompt = "Below is a question and a context in bengali language. Frame in a simple sentence from the context that directly answers the question. Do not generate more than 1 keyword or more than 1 sentence."
#         answer = getResponse(prompt,question,context)

#         #  Print final generated answer
#         print(answer)

#         #  Save the response to a text file
#         with open(f"answer_nous{i}.txt", "w", encoding="utf-8") as f:
#             f.write(answer)

def run1(question,context):
    prompt = "Below is a question and a context in bengali language. Give the most matching keyword from the context that directly answers the question. Do not generate more than 1 keyword or any sentence."
    text=getResponse(prompt,question,context)
    return text

def run2(question,context):
    prompt = "Below is a question and a context in bengali language. Frame in a simple sentence from the context that directly answers the question. Do not generate more than 1 keyword or more than 1 sentence."
    text=getResponse(prompt,question,context)
    return text

def run(question,context):
    init_for_out()
    exact_answer = run1(question,context)
    sentence = run2(question,context)   
    return exact_answer, sentence
