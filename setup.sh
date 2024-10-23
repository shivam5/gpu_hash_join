# Setup conda if not already setup
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
bash Anaconda3-2024.02-1-Linux-x86_64.sh -b -p $HOME/anaconda3
$HOME/anaconda3/bin/conda init bash
bash

# Create a new conda environment
conda create --prefix ./hash_join_env python=3.9
conda activate ./hash_join_env

# Install dependencies in conda environment
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
pip install llnl-hatchet
pip install -U --index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/Triton-Nightly/pypi/simple/ triton-nightly --use-deprecated legacy-resolver
