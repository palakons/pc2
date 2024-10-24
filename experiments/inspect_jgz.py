import json
import gzip

# Define the path to the gzipped JSON file
file_path = '/data/palakons/dataset/astyx/scene/frame_annotations.jgz'

# Open and read the gzipped JSON file
with gzip.open(file_path, 'rt', encoding='utf-8') as file:
    data = json.load(file)

print(data[:3]) #{'sequence_name': '79_8257_17428', 'frame_number': 0, 'frame_timestamp': -1.0, 'image': {'path': 'car/79_8257_17428/images/frame000072.jpg', 'size': [1281, 719]}, 'depth': {'path': 'car/79_8257_17428/depths/frame000072.jpg.geometric.png', 'scale_adjustment': 0.9381256699562073, 'mask_path': 'car/79_8257_17428/depth_masks/frame000072.png'}, 'mask': {'path': 'car/79_8257_17428/masks/frame000072.png', 'mass': 592532.0}, 'viewpoint': {'R': [[0.11167419701814651, 0.3011574447154999, 0.947012722492218], [-0.3123463988304138, -0.8940392136573792, 0.321144163608551], [0.9433814883232117, -0.3316595256328583, -0.005775671452283859]], 'T': [-1.2118680477142334, 0.35525602102279663, 4.3679327964782715], 'focal_length': [3.1938907798374476, 1.7926678147565378], 'principal_point': [0.0, 0.0]}}

#print keys of data [0]
print(data[0].keys()) #dict_keys(['sequence_name', 'frame_number', 'frame_timestamp', 'image', 'depth', 'mask', 'viewpoint'])
