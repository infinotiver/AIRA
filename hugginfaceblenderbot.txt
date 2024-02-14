import torch
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
def blenderbot_chat(inputs):
    inputs = tokenizer(inputs, return_tensors="pt")
    inputs
    res = model.generate(**inputs)
    res
    tokenizer.decode(res[0])
    return tokenizer.decode(inputs['input_ids'][0])