import os
import tkinter
from tkinter import filedialog
from vad import vad
import audio_splitter
import vocal_to_midi
import numpy as np
import consts

def get():
    if not os.path.exists("./audio"):
        os.mkdir("audio")

    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title = "select audio", filetypes = [("audio files", "*.mp3; *.wav")], initialdir = "./audio")
    root.destroy()

    vocal, inst = audio_splitter.run(filepath)
    vocal_section = vad(vocal)

    audiodic = {
        "name": os.path.splitext(os.path.basename(filepath))[0],
        "base": filepath,
        "vocal": vocal,
        "inst": inst
    }

    midi_data = vocal_to_midi.get(vocal)
    midi_data.remove_invalid_notes()
    # sr: Notes Detection Sensitivity
    sr = consts.Notes_Detection_Sensitivity
    piano = midi_data.get_piano_roll(fs=sr, pedal_threshold=None)
    p_times = np.arange(0, midi_data.get_end_time(), 1./sr)
    p_notes = piano.argmax(axis=0)
    p_volumes = piano.max(axis=0)
    vol_thread= np.percentile(p_volumes[p_volumes > 1], 10)

    times = []
    notes = []
    for start, end in vocal_section:
        _times = []
        _notes = []

        for t, note, volume in zip(p_times, p_notes, p_volumes):
            if t < start:
                pass

            if (start <= t <= end and note!=0) and (28 <= note <= 79) and (vol_thread < volume):
                _times.append(t)
                _notes.append(note)

            if end < t:
                break

        # ノード整理
        _times, _notes = arrangement(_times, _notes)
        times += _times
        notes += _notes

    return audiodic, np.array(times), np.array(notes)

# ノードの整地
def arrangement(times, notes):

    # 単発ノードを消す
    while True: 
        _notes = []
        count = 0
        for n in range(len(notes)):
            if n == 0 or n == len(notes) - 1:
                _notes.append(notes[n])

            else:
                if notes[n] == notes[n-1] and notes[n] == notes[n+1]:
                    _notes.append(notes[n])

                elif notes[n] == notes[n-1]:
                    _notes.append(notes[n-1])

                elif notes[n] == notes[n+1]:
                    _notes.append(notes[n+1])

                else:
                    _notes.append(None)
                    count += 1

        times = [t for t, c in zip(times, _notes) if c != None]
        notes = [c for c in _notes if c != None]

        if count == 0:
            break

    return times, notes

if __name__=="__main__":
    get()