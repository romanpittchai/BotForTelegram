sudo apt update && sudo apt upgrade

sudo apt install python-gi-dev python3-venv

python3 -m venv venv

. venv/bin/activate

python3 -m pip install --upgrade pip

pip install -r requirements.txt
