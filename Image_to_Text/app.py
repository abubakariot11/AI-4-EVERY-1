from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())
captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")


def image2text(url):
    image_to_text = pipeline("image-to-text", model = "Salesforce/blip-image-captioning-base")
    text = image_to_text(url)[0]["generated_text"]
    print(text)
    return text


# from transformers import pipeline

# captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
# captioner("https://huggingface.co/datasets/Narsil/image_dummy/resolve/main/parrots.png")
# ## [{'generated_text': 'two birds are standing next to each other '}]

image2text("img.jpg")