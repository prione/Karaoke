import sounddevice as sd

n_chroma = 12*3
device_info = sd.query_devices(None, 'input')
RATE = int(device_info['default_samplerate'])
CHANNEL = 1
CHUNK = 1024*3

# Notes Detection Sensitivity
Notes_Detection_Sensitivity = 8

# mic sensibility
mic_thread = 0.005