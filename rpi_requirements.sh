sudo apt update && sudo apt install python3-opencv python3-picamera2

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt