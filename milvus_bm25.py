from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def delete_collection(collection_name):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
        print(f"Collection '{collection_name}' has been deleted.")
    else:
        print(f"Collection '{collection_name}' does not exist.")


connections.connect("default", host="localhost", port="19530")

delete_collection("text_documents")

documents = [
    "The quick brown fox jumps over the lazy dog",
    "A journey of a thousand miles begins with a single step",
    "To be or not to be, that is the question",
    "All that glitters is not gold",
    "Where there's a will, there's a way",
    "x89_78_ux_uix code: signa converter are passed at operation parameters",
    "x89_74_ux_uix code: signa converter are passed at operation parameters"
]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)


# Create a collection for our documents
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR,dim=tfidf_matrix.toarray().shape[-1])
]
schema = CollectionSchema(fields, "A collection for text documents")
collection = Collection("text_documents", schema)

# Create an IVF_FLAT index on the embedding field
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}
collection.create_index("embedding", index_params)


# Function to convert TF-IDF vector to dense numpy array
def tfidf_to_dense(tfidf_vector):
    return tfidf_vector.toarray().flatten()

# Insert documents into Milvus
for i, doc in enumerate(documents):
    embedding = tfidf_to_dense(tfidf_matrix[i])
    collection.insert([[i], [doc], [embedding]])


# Flush the inserted data to make it visible for search
collection.flush()

# Load the collection
collection.load()


# BM25 search function
def bm25_search(query, top_k=1):
    # Convert query to TF-IDF vector
    query_vector = tfidf_to_dense(vectorizer.transform([query]))
    
    # Search in Milvus
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text"]
    )
    
    return [(hit.entity.get('text'), hit.distance) for hit in results[0]]



# Example search
query = "X89_74_UX_uix"
results = bm25_search(query,top_k=2)

print(f"Query: {query}")
print("Results:")
for text, score in results:
    print(f"Text: {text}")
    print(f"Score: {score}")
    print()

# # Disconnect from Milvus
# connections.disconnect("default")


