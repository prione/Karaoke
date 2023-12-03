import os
from basic_pitch.inference import predict_and_save
import pretty_midi

def get(vocal):
    if not os.path.exists(f"{os.path.dirname(vocal)}/vocals_basic_pitch.mid"):
        predict_and_save(
            audio_path_list=[vocal],
            output_directory=os.path.dirname(vocal),
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=False,
            onset_threshold=1,
            minimum_frequency=130,
            maximum_frequency=2489,        
        )

    return pretty_midi.PrettyMIDI(f"{os.path.dirname(vocal)}/vocals_basic_pitch.mid")