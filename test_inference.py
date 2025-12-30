from pathlib import Path
from models.CNN10_v1.config.overseer import Overseer

# 1. Setup paths
project_root = Path(__file__).parent
model_folder = project_root / "models" / "CNN10_v1"

# 2. Initialize Overseer
# This will load config/parameters.yaml and weight/best.pth
overseer = Overseer(model_folder)

# 3. Define path to your test audio
audio_path = project_root / "electric_guitar.wav" # Make sure this file exists!

# 4. Run prediction
if audio_path.exists():
    instruments = overseer.predict(str(audio_path))
    print(f"Detected instruments: {instruments}")
else:
    print("Please place a 'instr.wav' file in the project root.")
