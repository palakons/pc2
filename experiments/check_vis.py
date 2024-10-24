import os

base_dir = '/home2/palakons/singularity/outputs/debug/'

for dir_name in sorted(os.listdir(base_dir), reverse=True):
    #print last update time

    dir_path = os.path.join(base_dir, dir_name)
    if os.path.isdir(dir_path):
        vis_dir = os.path.join(dir_path, 'vis')
        if os.path.exists(vis_dir) and os.path.isdir(vis_dir):
            images_dir = os.path.join(vis_dir, 'images')
            if os.path.exists(images_dir) and os.path.isdir(images_dir):
                if os.listdir(images_dir):
                    print(f"Files exist in {images_dir}")
                # else:
                #     print(f"No files in {images_dir}")
            # else:
            #     print(f"{images_dir} does not exist")
        # else:
        #     print(f"{vis_dir} does not exist")