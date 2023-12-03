import subprocess
import os

def run(filename):
  if not os.path.exists("./audio/htdemucs/" + os.path.splitext(os.path.basename(filename))[0]):
    input_audio_path = filename
    output_audio_path = "./audio"
    cmd = ["python", "-m", "demucs", "--two-stems=vocals", "-o", f"{output_audio_path}", f"{input_audio_path}"]

    subprocess.run(cmd)

  vocal_data = f"./audio/htdemucs/{os.path.splitext(os.path.basename(filename))[0]}/vocals.wav"
  inst_data = f"./audio/htdemucs/{os.path.splitext(os.path.basename(filename))[0]}/no_vocals.wav"
  
  return vocal_data, inst_data