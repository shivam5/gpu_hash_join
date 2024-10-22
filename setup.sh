python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip setuptools wheel
python3 -m venv gpu_hash_join
source gpu_hash_join/bin/activate

python3 -m pip install -r requirements.txt