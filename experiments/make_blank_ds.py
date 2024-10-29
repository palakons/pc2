import os
from PIL import Image
root_dir="/data/palakons/dataset/astyx/scene_blank_cam"

#go though subdirs in root_dir, except set_lists and eval_batches
for dir in sorted(os.listdir(root_dir)):
    if dir == "set_lists" or dir == "eval_batches":
        continue
    print(f"Processing {root_dir}/{dir}")
    #/data/palakons/dataset/astyx/scene_blank_cam/148/depths/000148.png
    depth_fname = f"{root_dir}/{dir}/depths/{int(dir):06d}.png"
    #make the file all white, mayusing PIL
    img = Image.open(depth_fname)
    img = img.convert('L')
    img = img.point(lambda p: 255)
    img.save(depth_fname)


    #/data/palakons/dataset/astyx/scene_blank_cam/148/images/000148.jpg
    image_fname = f"{root_dir}/{dir}/images/{int(dir):06d}.jpg"
    #make the file all white
    img = Image.open(image_fname)
    #reatin the channels
    img = img.convert('RGB')
    img = img.point(lambda p: 255)

    img.save(image_fname)
