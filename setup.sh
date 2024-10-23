# python3 -m ensurepip --default-pip
# python3 -m pip install --upgrade pip setuptools wheel
# python3 -m venv gpu_hash_join
# source gpu_hash_join/bin/activate

wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
bash Anaconda3-2024.02-1-Linux-x86_64.sh -b -p $HOME/anaconda3
$HOME/anaconda3/bin/conda init bash
bash
conda create --prefix ./env python=3.9
conda activate ./env

pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
pip install --no-cache-dir triton

# python3 -m pip install -r requirements.txt

# pip install llnl-hatchet
# pip install -U --index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/Triton-Nightly/pypi/simple/ triton-nightly --use-deprecated legacy-resolver
