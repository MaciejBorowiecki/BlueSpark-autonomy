# BlueSpark-autonomy
do odpalenia częsci z pose estimation
python -m pip install -U pip wheel setuptools

# 3) Wyrzuć NumPy 2 i wgraj stabilną 1.26.x
pip uninstall -y numpy
pip install "numpy<2"  # zainstaluje np. 1.26.4

# 4) (opcjonalnie) dopasuj torch/torchvision/torchaudio
pip install -U torch torchvision torchaudio

# 5) Sprawdź wersje
python - <<'PY'
import numpy, torch
print("numpy:", numpy.__version__)
print("torch:", torch.__version__)
PY


pip install ultralytics

I opencv
