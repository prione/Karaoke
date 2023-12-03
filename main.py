from audio import record, play
from display import app
import threading

# Disp
display_app = app()

# AudioStream
record_theread = threading.Thread(target=record, args=(display_app.callback_indata,), daemon=True)
play_theread = threading.Thread(target=play, args=(display_app.callback_time, display_app.audiodic["inst"]), daemon=True)
record_theread.start()
play_theread.start()

# Start
display_app.run()