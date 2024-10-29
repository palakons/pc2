import wandb

# Example sweep configuration
sweep_configuration = {
    "description": "Sweep over batch size and learning rate",
    "method": "grid",
    "name": "bkank-fit",
    "parameters": {
        "dataloader.batch_size": {"values": [12,8,4,2]},
        "run.max_steps": {"values": [4000]},
        "optimizer.lr": {"values": [.01,.001,.0001,.00001]},
    },
    "program": "projection-conditioned-point-cloud-diffusion/experiments/main.py",
    "command": ["${env}","${interpreter}","${program}","${args_no_hyphens}"]
}

sweep_id = wandb.sweep(sweep=sweep_configuration, project="pc2-astyx")
print("sweep_id:", sweep_id)