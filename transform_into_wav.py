from pydub import AudioSegment
import os

file_path = os.path.join(os.getcwd(), "apps", "interface", "static", "sounds", "organ.mp3")
out_path  = os.path.join(os.getcwd(), "apps", "interface", "static", "sounds", "organ.wav")

AudioSegment.from_mp3(file_path).export(out_path, format="wav")
