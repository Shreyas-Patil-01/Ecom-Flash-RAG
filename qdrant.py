from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
from time import sleep


qdrant_client = QdrantClient(
    url="YOUR_QDRANT_URL",
    api_key="YOUR_API_KEY",
    timeout=120  
)


with open("embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)


print(f"Total number of points in embeddings.json: {len(data)}")


collection_name = "YOUR_COLLECTION_NAME"
vector_size = len(data[0]["embedding"])  
if qdrant_client.collection_exists(collection_name):
    qdrant_client.delete_collection(collection_name)


qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE  
    )
)


points = []
for idx, item in enumerate(data):
   
    vector = item["embedding"]
    
    
    payload = {
        "Product_name": item["Product_name"],
        "Price": item["Price"],
        "colors": item["colors"],
        "Description": item["Description"],
        
        "text": f"{item['Product_name']} {item['Price']} {item['colors']} {item['Description']}"
    }
    
    
    points.append(
        models.PointStruct(
            id=idx,  
            vector=vector,
            payload=payload
        )
    )


batch_size = 10  
total_points = len(points)
print(f"Total points to upload: {total_points}")

for i in range(0, total_points, batch_size):
    batch = points[i:i + batch_size]
    retries = 3
    for attempt in range(retries):
        try:
            qdrant_client.upsert(
                collection_name=collection_name,
                points=batch
            )
            print(f"Uploaded batch {i // batch_size + 1} ({len(batch)} points)")
            sleep(2) 
            break 
        except Exception as e:
            print(f"Error uploading batch {i // batch_size + 1}: {str(e)}")
            if attempt < retries - 1:
                print(f"Retrying ({attempt + 1}/{retries}) after 10 seconds...")
                sleep(10)  
            else:
                print(f"Failed to upload batch {i // batch_size + 1} after {retries} attempts.")
                raise  

print(f"Successfully uploaded {total_points} points to the '{collection_name}' collection in Qdrant.")