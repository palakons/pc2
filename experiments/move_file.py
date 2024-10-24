
import os


src  = "/data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019"
dst = "/data/palakons/dataset/astyx/scene"

# self.dataset_root --dst
#         ├── <category_0> --scene
#         │   ├── <sequence_name_0> --id
#         │   │   ├── depth_masks --na
#         │   │   ├── depths --depth_front
#         │   │   ├── images --camera_front
#         │   │   ├── masks --na
#         │   │   └── pointcloud.ply  --radar_6455
#         │   ├── set_lists
#         │       ├── set_lists_<subset_name_0>.json
#         │       ├── set_lists_<subset_name_1>.json
#         │       ├── ...
#         │       ├── set_lists_<subset_name_M>.json
#         │   ├── eval_batches
#         │   │   ├── eval_batches_<subset_name_0>.json
#         │   │   ├── eval_batches_<subset_name_1>.json
#         │   │   ├── ...
#         │   │   ├── eval_batches_<subset_name_M>.json
#         │   ├── frame_annotations.jgz
#         │   ├── sequence_annotations.jgz

# "list files in src/camera_front"
files = os.listdir(f"{src}/camera_front")
#mkdir set_lists
os.system(f"mkdir -p {dst}/set_lists")
#mkdir eval_batches
os.system(f"mkdir -p {dst}/eval_batches")

#cp to dst/camera_front
if False:
    for file in files:
        #file /data/palakons/dataset/radar_dataset_astyx/dataset_astyx_hires2019/camera_front/000479.jpg
        # extract frame number
        frame_number = int(file.split('.')[0])
        #mkdir -p 
        os.system(f"mkdir -p {dst}/{frame_number}/images")
        #cp
        os.system(f"cp {src}/camera_front/{file} {dst}/{frame_number}/images")

if True:
    import cv2
    files = os.listdir(f"{src}/depth_front")
    for file in files:
        #if ends with vitl
        if  not file.endswith('vitl.png') and not file.endswith('vitb.png') and not file.endswith('vitl.jpg'):
            continue
        #000476_vitb.jpg
        frame_number = int(file.split('_')[0])
        # if frame_number >20:
        #     continue
        #depth
        #convert to grayscale
        img = cv2.imread(f"{src}/depth_front/{file}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #save to dst/depths
        
        cv2.imwrite(f"{src}/depth_front/{file}", img)
        
        # print("img", img.shape)
        os.system(f"mkdir -p {dst}/{frame_number}/depths")
        os.system(f"cp {src}/depth_front/{file} {dst}/{frame_number}/depths/{frame_number:06d}.png")

if False:
    files = os.listdir(f"{src}/radar_6455")
    for file in files:
        frame_number = int(file.split('.')[0])
        #radar
        os.system(f"cp {src}/radar_6455/{file} {dst}/{frame_number}")