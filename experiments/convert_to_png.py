from PIL import Image
import os

def convert_jpg_to_png(src_file):
    # Open the JPG image
    img = Image.open(src_file)
    
    # Define the destination file path
    base_dir, file_name = os.path.split(src_file)
    file_name_without_ext = os.path.splitext(file_name)[0]
    dest_file = os.path.join(base_dir, f"{file_name_without_ext}.png")
    
    # Save the image as PNG
    img.save(dest_file, 'PNG')
    print(f"Converted {src_file} to {dest_file}")
    #remove the jpg file
    os.remove(src_file)
def convert_png_to_one_channel(src_file):
    # Open the PNG image
    img = Image.open(src_file)
    
    # Convert the image to one channel
    img = img.convert('L')
    
    # Define the destination file path
    base_dir, file_name = os.path.split(src_file)
    file_name_without_ext = os.path.splitext(file_name)[0]
    dest_file = os.path.join(base_dir, f"{file_name_without_ext}.png")
    
    # Save the image as PNG
    img.save(dest_file, 'PNG')
    print(f"Converted {src_file} to {dest_file}")
    #remove the jpg file
def convert_all_png_to_one_channel(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png') and subdir.split("/")[-1] == "depths":
                src_file = os.path.join(subdir, file)
                # print(f"Converting {src_file} in {subdir}...")
                convert_png_to_one_channel(src_file)
def convert_all_jpgs_in_directory(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.jpg') and subdir.split("/")[-1] == "depths":
                src_file = os.path.join(subdir, file)
                # print(f"Converting {src_file} in {subdir}...")
                convert_jpg_to_png(src_file)

# Example usage
root_dir = '/data/palakons/dataset/astyx/scene/'
# convert_all_jpgs_in_directory(root_dir)
convert_all_png_to_one_channel(root_dir)