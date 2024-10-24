import open3d as o3d
import numpy as np
import os,time

sample_path = '/home2/palakons/singularity/outputs/debug/2024-10-22--05-32-26/sample/pred/car/'
ds_path = "/data/palakons/dataset/radar_dataset_astyx_genai/dataset_astyx_hires2019/radar_6455/"

# for each sample in sample_path
for sameple_fname in sorted(os.listdir(sample_path)):
    sample = o3d.io.read_point_cloud(sample_path + sameple_fname)
    print(sample)
    print(np.asarray(sample.points)[:10])

    idx = int(sameple_fname.split('.')[0])
    radar_pd_fname = f"{idx:06d}.txt"
    #
    # X Y Z V_r Mag
    # 0.156961712104167567 2.30565393293341492 -0.254848718643188477 0 47.5
    # 1.1886736381409535 2.25347094076469778 -0.106887154281139374 0 48.5
    # 1.91251998170473048 2.21058479439606614 0.105867467820644379 0 50
    # 1.96062454348353121 2.26726630794580108 0.124318979680538177 0 59
    # 1.95957798864980748 2.26726630794580108 0.13984854519367218 -0.0812000036239624023 53
    # 1.95860896709576271 2.269140701388217 0.121867001056671143 0.0812000036239624023 53.5

    #move radar_pd_fname to radar_pd_fname.old_{timestamps}
    os.rename(ds_path + radar_pd_fname, ds_path + radar_pd_fname + f".old_{time.time()}")   

    #create new file 
    with open(ds_path + radar_pd_fname, 'w') as f:
        f.write(f"\nX Y Z V_r Mag\n")
        for point in np.asarray(sample.points):
            f.write(f"{point[0]} {point[1]} {point[2]} 0 0\n")


