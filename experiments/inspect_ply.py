import open3d as o3d
import numpy as np

file_path = '/data/palakons/dataset/co3d/car/429_60444_117576/pointcloud.ply'

# Read the PLY file
pcd = o3d.io.read_point_cloud(file_path)

# Print basic information about the point cloud
print(pcd)

# Print the first 10 points
print("First 10 points:")
print(np.asarray(pcd.points)[:10])

# Visualize the point cloud
# o3d.visualization.draw_geometries([pcd])