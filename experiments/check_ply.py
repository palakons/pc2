import os

dst = "/data/palakons/dataset/astyx/scene"

files = os.listdir(dst)
for file in files:
    #check if pointcloud.ply exists, the file si dir
    if  not os.path.exists(os.path.join(dst, file, "pointcloud.ply")) and os.path.isdir(os.path.join(dst, file)):
        print(f"Pointcloud not found in {file}")
# /data/palakons/dataset/astyx/scene/10/pointcloud.ply