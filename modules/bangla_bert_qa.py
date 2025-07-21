from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load model & tokenizer
tokenizer = AutoTokenizer.from_pretrained("doerig/banglabert")
model = AutoModelForQuestionAnswering.from_pretrained("doerig/banglabert")

# # Inputs
# question = "চার্লসটন হারবার থেকে অ্যাশলে নদীর সাথে কোন নদী মিশে গেছে?  "
# context = "চার্লসটন আমেরিকা যুক্তরাষ্ট্রের দক্ষিণ ক্যারোলাইনা রাজ্যের প্রাচীনতম এবং দ্বিতীয় বৃহত্তম শহর, চার্লসটন কাউন্টির কাউন্টি আসন এবং চার্লসটন – নর্থ চার্লসটন – সামারভিলে মেট্রোপলিটন স্ট্যাটিস্টিকাল এরিয়ার প্রধান শহর  শহরটি দক্ষিণ ক্যারোলিনার উপকূলরেখার ভৌগলিক মিডপয়েন্টের ঠিক দক্ষিণে অবস্থিত এবং অ্যাশলে এবং কুপার নদীর নদীর সংগম দ্বারা গঠিত আটলান্টিক মহাসাগরের একটি খাঁটি চার্লস্টন হারবারে অবস্থিত, অথবা স্থানীয়ভাবে প্রকাশিত হয়েছে, যেখানে কুপার এবং অ্যাশলে রয়েছে। নদীগুলি একত্র হয়ে আটলান্টিক মহাসাগর গঠনে আসে। "

def init_for_out():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("doerig/banglabert")
    model = AutoModelForQuestionAnswering.from_pretrained("doerig/banglabert")


def run(question, context):

    init_for_out()
   
    # Tokenize
    inputs = tokenizer(question, context, return_tensors="pt")

    # Get start & end logits
    with torch.no_grad():
        outputs = model(**inputs)

    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Find the tokens with the highest score
    start_idx = torch.argmax(start_logits)
    end_idx = torch.argmax(end_logits) + 1

    # Decode the tokens to string
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_idx:end_idx])
    )

    print("Answer:", answer)

    return answer
