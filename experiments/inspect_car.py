import json
from collections import Counter

# Define the path to the JSON file
file_path = '/data/palakons/dataset/co3d/car/set_lists/set_lists_set_lists.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Print all keys in the JSON file
print("Keys in the JSON file:")
keys = list(data.keys())
for key in keys:
    print(f"- {key}")

all_file_path = [d[2]  for key in keys for d in data[key]] 

# Count the number of files in each set
file_count = Counter(all_file_path)
check = [k for k, v in file_count.items() if v > 1]
print(check)

#inspec eval batch: /data/palakons/dataset/co3d/car/eval_batches/eval_batches_80-20.json
file_eval_batch_path = '/data/palakons/dataset/co3d/car/eval_batches/eval_batches_set_lists.json'
print("Inspect eval batch")
with open(file_eval_batch_path, 'r') as file:
    data = json.load(file)
print(len(data))
for d in data:
    print(len(d))   