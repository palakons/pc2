import json
import gzip
import os

# Define the path to the gzipped JSON file
file_path = '/data/palakons/dataset/astyx/scene/sequence_annotations.jgz'

# Open and read the gzipped JSON file
with gzip.open(file_path, 'rt', encoding='utf-8') as file:
    data = json.load(file)

print(data[:3])  #[{'sequence_name': '79_8257_17428', 'category': 'car', 'video': {'path': 'car/79_8257_17428/video.MOV', 'length': -1.0}, 'point_cloud': {'path': 'car/79_8257_17428/pointcloud.ply', 'quality_score': -1.2702143963257189, 'n_points': 117906}, 'viewpoint_quality_score': 0.06755821394157818}, {'sequence_name': '106_12650_23736', 'category': 'car', 'video': {'path': 'car/106_12650_23736/video.MOV', 'length': -1.0}, 'point_cloud': {'path': 'car/106_12650_23736/pointcloud.ply', 'quality_score': 1.9297082316623881, 'n_points': 980001}, 'viewpoint_quality_score': 1.5452153366593602}, {'sequence_name': '106_12651_23171', 'category': 'car', 'video': {'path': 'car/106_12651_23171/video.MOV', 'length': -1.0}, 'point_cloud': {'path': 'car/106_12651_23171/pointcloud.ply', 'quality_score': -0.9697249715535128, 'n_points': 254335}, 'viewpoint_quality_score': 1.4722185165968882}]

#{'sequence_name': '79_8257_17428', 'category': 'car', 'video': {'path': 'car/79_8257_17428/video.MOV', 'length': -1.0}, 'point_cloud': {'path': 'car/79_8257_17428/pointcloud.ply', 'quality_score': -1.2702143963257189, 'n_points': 117906}, 'viewpoint_quality_score': 0.06755821394157818},

#print n points
for d in data:
    print(d['point_cloud']['n_points'], end=", ")

#print keys of data [0]
print(data[0].keys()) #dict_keys(['sequence_name', 'category', 'video', 'point_cloud', 'viewpoint_quality_score'])


#find moveit length != -1
print("video length")
for d in data:
    if d['video']['length'] != -1:
        print(d['video']['length'])

#check if video existed
print("video path")
for d in data:
    if os.path.exists(f"/data/palakons/dataset/co3d/{d['video']['path']}"):
        print("exist",d['video']['path'])