from inaSpeechSegmenter import Segmenter
import pickle
import os

def vad(filename):
  if not os.path.exists(os.path.dirname(filename) + "/vocal_section.pkl"):
    
    seg_model = Segmenter(vad_engine="sm", detect_gender=False, ffmpeg = os.path.join(os.path.dirname(__file__), "./ffmpeg.exe"))
    seg_data = seg_model(filename)

    vocal_section = [s[1:] for s in seg_data if s[0] in "speech" or s[0] in "music"]

    with open(os.path.dirname(filename) + "/vocal_section.pkl", "wb") as f:
        pickle.dump(vocal_section, f)

  with open(os.path.dirname(filename) + "/vocal_section.pkl", "rb") as f:
      vocal_section = pickle.load(f)

  return vocal_section


if __name__ == "__main__":

  import tkinter
  from tkinter import filedialog 

  root = tkinter.Tk()
  root.withdraw()
  filename = filedialog.askopenfilename(title = "select audio", initialdir = "./audio/htdemucs")
  root.destroy()

  vocal_section = vad(filename)