from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

#MODEL_NAME = "Falconsai/text_summarization"
#MODEL_NAME = "facebook/bart-large-cnn"
#MODEL_NAME = "google/pegasus-large"
#MODEL_NAME = "t5-large"
MODEL_NAME_1 = "google/pegasus-xsum"
MODEL_NAME = "./nha-finetuned-on-transcripts"
#MODEL_NAME = "t5-large"

# Load tokenizer and model

# Load tokenizer and model
tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME_1)
model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME_1)

#tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def summarize_transcript(text: str, max_input_length=512, max_output_length=64) -> str:
    inputs = tokenizer.encode(
        text,
        return_tensors="pt",
        max_length=max_input_length,
        truncation=True
    ).to(device)

    summary_ids = model.generate(
        inputs,
        max_length=max_output_length,
        min_length=10,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()

def summarize_batch_transcripts(texts: list, max_input_length=512, max_output_length=64) -> list:
    def clean_and_pad_short(text, min_words=5):
        text = text.strip()
        return text

    cleaned_texts = [clean_and_pad_short(t) for t in texts]

    inputs = tokenizer(
        cleaned_texts,
        return_tensors="pt",
        max_length=max_input_length,
        truncation=True,
        padding=True
    ).to(device)

    summary_ids = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=max_output_length,
        min_length=5,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True,
        no_repeat_ngram_size=3
    )

    summaries = [tokenizer.decode(g, skip_special_tokens=True).strip() for g in summary_ids]
    return summaries
