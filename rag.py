from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os


os.environ["OPENAI_API_KEY"] = "YOUR API KEY"
openai_client = OpenAI()


qdrant_client = QdrantClient(
    url="QDRNAT_URL",
    api_key="QDRANT_API_KEY",
    timeout=30  
)


embedding_model = SentenceTransformer('sentence-transformers/static-retrieval-mrl-en-v1')


collection_name = "YOUR_COLLECTION_NAME"


def generate_query_embedding(query):
    return embedding_model.encode(query, convert_to_numpy=True)


def retrieve_context(query):
    
    query_embedding = generate_query_embedding(query)
    
    
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=1, 
        with_payload=True,
        with_vectors=False  
    )
    
    if not search_result:
        return None
    
    
    top_result = search_result[0]
    payload = top_result.payload
    
    
    context = (
        f"Product: {payload['Product_name']}\n"
        f"Price: {payload['Price']}\n"
        f"Colors: {payload['colors']}\n"
        f"Description: {payload['Description']}"
    )
    return context


def generate_answer(query, context):
    if not context:
        return "Sorry, I couldn’t find any relevant information for your query."
    
   
    prompt = (
        "You are a helpful assistant for an e-commerce platform. Based on the following product information, answer the user's query.\n\n"
        f"Product Information:\n{context}\n\n"
        f"User Query: {query}\n\n"
        "Answer:"
    )
    
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant for an e-commerce platform."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()


print("Welcome to the E-commerce Chatbot! Type 'exit' to quit.")
while True:
    
    query = input("Enter your query: ").strip()
    
    
    if query.lower() == "exit":
        print("Goodbye!")
        break
    
    
    context = retrieve_context(query)
    
    
    answer = generate_answer(query, context)
    
    # Print the answer
    print("\nAnswer:", answer, "\n")