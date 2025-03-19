from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Connect to your Qdrant cluster
qdrant_client = QdrantClient(
    url="YOUR_QDRANT_CLUSTER_URL",
    api_key="YOUR_API_KEY",
    timeout=120
)


collection_name = "YOUR_COLLECTION_NAME"


def get_all_points():
    points = []
    offset = None
    while True:
        response = qdrant_client.scroll(
            collection_name=collection_name,
            limit=100,  
            with_payload=True,
            with_vectors=True,  
            offset=offset
        )
        points.extend(response[0])  
        offset = response[1]  
        if offset is None:  
            break
    return points


points = get_all_points()
print(f"Total points in collection: {len(points)}")


point_ids = [point.id for point in points]
vectors = np.array([point.vector for point in points])


similarity_matrix = cosine_similarity(vectors)


similarity_threshold = 0.999


seen = set()
duplicates = []

for i in range(len(points)):
    if point_ids[i] in seen:
        continue
   
    for j in range(i + 1, len(points)):
        if similarity_matrix[i][j] >= similarity_threshold:
            duplicates.append(point_ids[j])
            seen.add(point_ids[j])

print(f"Found {len(duplicates)} duplicate points based on embeddings.")


if duplicates:
    qdrant_client.delete(
        collection_name=collection_name,
        points_selector=models.PointIdsList(
            points=duplicates
        )
    )
    print(f"Deleted {len(duplicates)} duplicate points from the '{collection_name}' collection.")
else:
    print("No duplicates found based on embeddings.")


points_after = get_all_points()
print(f"Total points after deduplication: {len(points_after)}")