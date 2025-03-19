from sentence_transformers import SentenceTransformer
import json


model = SentenceTransformer('sentence-transformers/static-retrieval-mrl-en-v1')


with open("cleaned_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)


texts = [
    f"{item['Product_name']} {item['Price']} {item['colors']} {item['Description']}" 
    for item in data
]


embeddings = model.encode(texts, convert_to_numpy=True)


for i, item in enumerate(data):
    item['embedding'] = embeddings[i].tolist()  


with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Embeddings generated and saved to 'embeddings.json'")