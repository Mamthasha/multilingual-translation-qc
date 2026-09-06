from transformers import MarianMTModel, MarianTokenizer
import time

MODEL_NAME = "Helsinki-NLP/opus-mt-en-hi"  # English -> Hindi

print("Loading model... (much smaller, ~300MB)")
start = time.time()

tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME, use_safetensors=True)

print(f"Model loaded in {time.time() - start:.1f} seconds")

def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs, max_length=100)
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

text = "Hello, my name is Mamthasha and I study at SASTRA University."
result = translate(text)

print(f"\nEnglish: {text}")
print(f"Hindi:   {result}")