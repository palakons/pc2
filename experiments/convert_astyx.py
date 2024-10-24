import json
import gzip
import os
from PIL import Image
import numpy as np 
def convert_record(base_dir,key,record):
    # assert key  is tehsame as fiels names (without leading zeros)
    assert int(key) == int(record['calibration'].split('.')[0].split('/')[-1]) == int(record['camera_front'].split('.')[0].split('/')[-1]) , f"key and record fields are not the same {key} {record['calibration'].split('/')[-1] } {record['camera_front'].split('/')[-1]}"
    '''record format

    "0": {
      "calibration": "calibration/000000.json",
      "camera_front": "camera_front/000000.jpg",
      "groundtruth_obj3d": "groundtruth_obj3d/000000.json",
      "lidar_vlp16": "lidar_vlp16/000000.txt",
      "radar_6455": "radar_6455/000000.txt"
    }
    '''

    '''convert to this structure
    #{'sequence_name': '79_8257_17428', 'frame_number': 0, 'frame_timestamp': -1.0, 'image': {'path': 'car/79_8257_17428/images/frame000072.jpg', 'size': [1281, 719]}, 'depth': {'path': 'car/79_8257_17428/depths/frame000072.jpg.geometric.png', 'scale_adjustment': 0.9381256699562073, 'mask_path': 'car/79_8257_17428/depth_masks/frame000072.png'}, 'mask': {'path': 'car/79_8257_17428/masks/frame000072.png', 'mass': 592532.0}, 'viewpoint': {'R': [[0.11167419701814651, 0.3011574447154999, 0.947012722492218], [-0.3123463988304138, -0.8940392136573792, 0.321144163608551], [0.9433814883232117, -0.3316595256328583, -0.005775671452283859]], 'T': [-1.2118680477142334, 0.35525602102279663, 4.3679327964782715], 'focal_length': [3.1938907798374476, 1.7926678147565378], 'principal_point': [0.0, 0.0]}}
    # Convert the record to the new structure'''
    #find the size of record['camera_front']
    #join base patth with record['camera_front']
    full_path = os.path.join(base_dir, record['camera_front'])
    #get the depth path
    def get_depth_path(full_path):
        #from /data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019/camera_front/000479.jpg
        #to /data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019/depth_front/000545_vitl.jpg
        ext = os.path.splitext(full_path)[1]
        return full_path.replace('camera_front','depth_front').replace(f".{ext}",f"_vitl.{ext}")
    def get_mask_path(full_path):
        return ""
        return full_path.replace('camera_front','masks')
    def get_camera_param(calibration_file_path):
        '''
                "calib_data": {
                    "K": [
                        [
                            1817.98103,
                            0.0,
                            1040.27484
                        ],
                        [
                            0.0,
                            1816.83987,
                            319.497539
                        ],
                        [
                            0.0,
                            0.0,
                            1.0
                        ]
                    ],
                    "T_to_ref_COS": [
                        [
                            0.015721251542359097,
                            0.0388038506130491,
                            0.9991231397751291,
                            -0.04286578070231163
                        ],
                        [
                            -0.9983693562813132,
                            -0.054233366081888695,
                            0.0178156951919443,
                            -0.0019011493702534147
                        ],
                        [
                            0.054877145205922295,
                            -0.9977740503554758,
                            0.0378879601312635,
                            0.011313703630010682
                        ],
                        [
                            0.0,
                            0.0,
                            0.0,
                            1.0
                        ]
                    ]
                },
                "sensor_uid": "camera_front"'''
        """
        Reads the focal length from the calibration file for the specified sensor.

        :param calibration_file_path: Path to the calibration file.
        """
        with open(calibration_file_path, 'r') as file:
            calibration_data = json.load(file)
        
        for sensor in calibration_data['sensors']:
            if sensor['sensor_uid'] == "camera_front":
                if 'K' in sensor['calib_data']:
                    K = sensor['calib_data']['K']
                    fx = K[0][0]
                    fy = K[1][1]
                    focal = [fx, fy]
                    #extract R from T

                    R = np.array(sensor['calib_data']['T_to_ref_COS'])[:3,:3]
                    #convert ot list of list
                    R = R.tolist()
                    T = np.array(sensor['calib_data']['T_to_ref_COS'])[:3,3]
                    T = T.tolist()
                    #principal point
                    c = [K[0][2], K[1][2]]
                    return focal, R, T,c
        raise ValueError(f"Could not find focal length for sensor 'camera_front' in calibration file '{calibration_file_path}'.")

    img_size = list(Image.open(os.path.join(base_dir, record['camera_front'])).size)[::-1]
    depth_path = get_depth_path(os.path.join(base_dir,record['camera_front']))
    mask_path = get_mask_path(os.path.join(base_dir,record['camera_front'])) #not used in this case
    camera_focal_length,R,T,c = get_camera_param(os.path.join(base_dir,record['calibration']))
    new_record = {
        'sequence_name': key,
        'frame_number': 0,
        'frame_timestamp': -1.0,
        'image': {
            'path': f"scene/{key}/images/{int(key):06}.jpg",
            'size': img_size
        },
        'depth': {
            'path': f"scene/{key}/depths/{int(key):06}.png",
            'scale_adjustment': 1.0,
            'mask_path': f"scene/{key}/depth_masks/frames{int(key):06}.png",
        },
        'mask': { #not used
            'path': f"scene/{key}/masks/frames{int(key):06}.png",
            'mass': img_size[0]*img_size[1]
        },
        'viewpoint': { #view from origin
            'R': R,
            'T': T,
            'focal_length': camera_focal_length,
            'principal_point': c
        }

    }
    
    return new_record

# Define the paths to the input and output files
input_file_path = '/data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019/dataset.json'
base_dir ="/data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019"
output_file_path = '/data/palakons/dataset/astyx/scene/frame_annotations.jgz'

# Read the JSON file
json_data = []
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)["data"]

    for key in data.keys():
        print(key)
        new_record = convert_record(base_dir,key,data[key])
        print(new_record)
        json_data.append(new_record)

if True:
    # Write the JSON data to a GZIP-compressed file
    with gzip.open(output_file_path, 'wt') as output_file:
        json.dump(json_data, output_file, indent=2)

#workign with the sequence file
sequence_output_file_path = '/data/palakons/dataset/astyx/scene/sequence_annotations.jgz'
# {'sequence_name': '79_8257_17428', 'category': 'car', 'video': {'path': 'car/79_8257_17428/video.MOV', 'length': -1.0}, 'point_cloud': {'path': 'car/79_8257_17428/pointcloud.ply', 'quality_score': -1.2702143963257189, 'n_points': 117906}, 'viewpoint_quality_score': 0.06755821394157818},
print("sequence data")
print(json_data[0])
seq_data = []
for record in json_data:
    # n_point = cout lines of txt file
    pc_fname = f"/data/palakons/dataset/astyx/scene/{record['sequence_name']}/{int(record['sequence_name']):06}.txt"
    with open(pc_fname, 'r') as f:
        n_point = len(f.readlines())-3
        seq_data.append({
            'sequence_name': record['sequence_name'],
            'category': 'car',
            'video': {
                'path': f"scene/{record['sequence_name']}/video.MOV",
                'length': -1.0
            },
            'point_cloud': {
                'path': f"scene/{record['sequence_name']}/pointcloud.ply",
                'quality_score': 0.0,
                'n_points': n_point
            },
            'viewpoint_quality_score': 0.0
        })
print(seq_data[0])
if False:
    with gzip.open(sequence_output_file_path, 'wt') as output_file:
        json.dump(seq_data, output_file, indent=2)

#set lists

set_list_output_file_path = '/data/palakons/dataset/astyx/scene/set_lists/set_lists_80-20.json'

# {"train_known": [
#     ["106_12650_23736", 0, "car/106_12650_23736/images/frame000001.jpg"], ["106_12650_23736", 1, "car/106_12650_23736/images/frame000002.jpg"], ["106_12650_23736", 3, "car/106_12650_23736/images/frame000004.jpg"]] "train_unknown": []

train_known_frames = json_data[:int(len(json_data)*0.8)]
train_unknown_frames = json_data[int(len(json_data)*0.8):]
set_list_data={"train_known":[],"train_unknown":[]}
# print(train_known_frames[0]) #{'sequence_name': '0', 'frame_number': 0, 'frame_timestamp': -1.0, 'image': {'path': 'scene/0/images/000000.jpg', 'size': [2048, 618]}, 'depth': {'path': 'scene/0/depths/000000.jpg', 'scale_adjustment': 1.0, 'mask_path': ''}, 'viewpoint': {'R': [[0.015721251542359097, 0.0388038506130491, 0.9991231397751291], [-0.9983693562813132, -0.054233366081888695, 0.0178156951919443], [0.054877145205922295, -0.9977740503554758, 0.0378879601312635]], 'T': [-0.04286578070231163, -0.0019011493702534147, 0.011313703630010682], 'focal_length': [1817.98103, 1816.83987], 'principal_point': [1040.27484, 319.497539]}}
for d in train_known_frames:
    set_list_data['train_known'].append([d['sequence_name'],d['frame_number'],d['image']['path']])
for d in train_unknown_frames:
    set_list_data['train_unknown'].append([d['sequence_name'],d['frame_number'],d['image']['path']])
if False:
    #mkdir -p /data/palakons/dataset/astyx/scene/set_lists
    os.system(f"mkdir -p {os.path.dirname(set_list_output_file_path)}")
    with open(set_list_output_file_path, 'w') as output_file:
        json.dump(set_list_data, output_file, indent=2)

#eval batches
print("eval batches")
eval_batch_output_file_path = '/data/palakons/dataset/astyx/scene/eval_batches/eval_batches_80-20.json'

#output []
eval_batch_data = []
if False:
    #mkdir -p /data/palakons/dataset/astyx/scene/eval_batches
    os.system(f"mkdir -p {os.path.dirname(eval_batch_output_file_path)}")
    with open(eval_batch_output_file_path, 'w') as output_file:
        json.dump(eval_batch_data, output_file, indent=2)

#use open3d to convert astyx point cloud to ply

#/data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019/radar_6455/000151.txt
astyx_point_cloud_output_dir = "/data/palakons/dataset/astyx/scene"
#/data/palakons/dataset/astyx/scene/xxx/pointcloud.ply
import open3d as o3d
import numpy as np
import os
if False:
    for record in json_data:
        # n_point = cout lines of txt file
        pc_fname = f"/data/palakons/dataset/astyx/scene/{record['sequence_name']}/{int(record['sequence_name']):06}.txt"
        with open(pc_fname, 'r') as f:
            numnum = len(f.readlines())-3
            print(f"processing {pc_fname} numpoints {numnum}")
        with open(pc_fname, 'r') as f:
            points = []
            for line in f.readlines()[3:]:
                if line.strip() == "":
                    continue
                values = list(map(float,line.split()))
                #if the the first 3 are not numbers, skip
                if not all(map(lambda x: isinstance(x,float),values[:3])):
                    continue
                points.append(values[:3])

            assert len(points)== numnum, f"point count mismatch {len(points)} {numnum}"
            #save to ply
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.io.write_point_cloud(f"{astyx_point_cloud_output_dir}/{record['sequence_name']}/pointcloud.ply", pcd)
            print(f"saved {astyx_point_cloud_output_dir}/{record['sequence_name']}/pointcloud.ply")

#make an all-white grayscale mask for each image, same size as image
new_base_dir = "/data/palakons/dataset/astyx"
if True:
    for record in json_data:
        # print("key",record.keys()) #ey dict_keys(['sequence_name', 'frame_number', 'frame_timestamp', 'image', 'depth', 'viewpoint'])
        # print(record) #{'sequence_name': '0', 'frame_number': 0, 'frame_timestamp': -1.0, 'image': {'path': 'scene/0/images/000000.jpg', 'size': [618, 2048]}, 'depth': {'path': 'scene/0/depths/000000.png', 'scale_adjustment': 1.0, 'mask_path': ''}, 'viewpoint': {'R': [[0.015721251542359097, 0.0388038506130491, 0.9991231397751291], [-0.9983693562813132, -0.054233366081888695, 0.0178156951919443], [0.054877145205922295, -0.9977740503554758, 0.0378879601312635]], 'T': [-0.04286578070231163, -0.0019011493702534147, 0.011313703630010682], 'focal_length': [1817.98103, 1816.83987], 'principal_point': [1040.27484, 319.497539]}}
        output_mask_fname = f"{new_base_dir}/scene/{record['sequence_name']}/masks/frames{int(record['sequence_name']):06}.png"
        #/data/palakons/dataset/co3d/car/429_60446_117578/masks/frame000001.png
        #mkdir
        os.system(f"mkdir -p {os.path.dirname(output_mask_fname)}")
        img = Image.open(os.path.join(new_base_dir,record['image']['path']))
        mask = Image.new('L', img.size, 255)
        mask.save(output_mask_fname)
        print(f"saved {output_mask_fname}")


        output_depth_mask_fname = f"{new_base_dir}/scene/{record['sequence_name']}/depth_masks/frames{int(record['sequence_name']):06}.png"
        os.system(f"mkdir -p {os.path.dirname(output_depth_mask_fname)}")
        mask.save(output_depth_mask_fname)
        print(f"saved {output_depth_mask_fname}")

