import wandb

# Example sweep configuration
sweep_configuration = {
    "description": " na",
    "method": "grid",
    "name": "q1 data sizes",
    "parameters": {
        "dataloader.batch_size": {"values": [8]},#[10,8,4]},
        "run.max_steps": {"values": [4000]},
        "optimizer.lr": {"values": [.01]},#[.1,.01,.001]},
        "dataset.subset_name": {"values": ["21-6","43-11","80-20"]},
        # "model.point_cloud_model_embed_dim": {"values": [64]},
    },
    "program": "projection-conditioned-point-cloud-diffusion/experiments/main.py",
    "command": ["${env}","${interpreter}","${program}","${args_no_hyphens}"]
}

sweep_id = wandb.sweep(sweep=sweep_configuration, project="pc2-astyx")
print("sweep_id:", sweep_id)