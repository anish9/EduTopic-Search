import pandas as pd
import numpy as np
import typesense
import json

# Configure the Typesense client
client = typesense.Client({
  'nodes': [{
    'host': 'localhost',  # Replace with your Typesense server address
    'port': '8108',       # Replace with your Typesense port
    'protocol': 'http'    # Use 'https' if you have SSL enabled
  }],
  'api_key': 'Icm3xooVhTLe3WkeIDQGukk5QnUkZI3sVYetYQrotucHBwkv',
  'connection_timeout_seconds': 2
})


df = pd.read_csv("sample.csv")

# globallist = []
# for i,j in df.iterrows():
#     temp = {}
#     for k,v in j.items():
#         temp[k]=v
#     globallist.append(temp)


# schema = {
#   "name": "machinedata",  
#   "fields": [
#     {"name": ".*", "type": "string" }
#   ]
# }

# try:
#     client.collections["machinedata"].delete()
#     client.collections.create(schema)
# except:
#     client.collections.create(schema)


# for item in globallist:
#     client.collections['machinedata'].documents.create(item)


limit = 3

query = "17FU4"
search_parameters = {
        'q': query,
        'query_by': ",".join(list(df.columns)),  # This tells Typesense to search in all fields
        'per_page': limit,
        'prefix': 'true',  # Enable prefix matching
        'num_typos': 0, #Allow up to 2 typos for fuzzy matching
    }

results = client.collections['machinedata'].documents.search(search_parameters)

print(results["hits"])


# limit = 5
# query = "zero tolerance in a array"
# search_parameters = {
#         'q': query,
#         'query_by': "short description,name",  # This tells Typesense to search in all fields
#         'per_page': limit,
#         'prefix': True,  # Enable prefix matching
#         'num_typos': 3, #Allow up to 2 typos for fuzzy matching
#         'exhaustive_search': True,
#         'typo_tolerance_enabled': True,
#         "split_join_tokens": True,
#         "sort_by": "_text_match:desc",
#         "text_match_type":"sum_score"
#     }
