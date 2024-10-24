import torch
from pytorch3d import renderer

# from pytorch3d.renderer import PointsRasterizer
# from pytorch3d.renderer import PointsRasterizer, PointsRasterizationSettings, FoVPerspectiveCameras
import imageio

# Define the camera
cameras = renderer.FoVPerspectiveCameras(device='cuda')

# Define rasterization settings
raster_settings = renderer.PointsRasterizationSettings(
	image_size=512,  # Output image size
	radius=0.01,     # Radius of the points
	points_per_pixel=10  # Number of points to consider per pixel
)

# Create the PointsRasterizer
rasterizer = renderer.PointsRasterizer(
	cameras=cameras,
	raster_settings=raster_settings
)

# Example 3D points
points = torch.rand((1, 1000, 3), device='cuda')  # Batch of 1, 1000 points

# Rasterize the points
rasterized_points = rasterizer(points)

# Save the point cloud to a file
torch.save(points.cpu(), 'point_cloud.pt')

# Convert rasterized points to an image and save
# We take the first channel and the first batch element for simplicity
rasterized_image = rasterized_points[0, ..., 0].cpu().numpy()
imageio.imwrite('rasterized_image.png', rasterized_image)

print("Point cloud and rasterized image saved.")