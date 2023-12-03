import sounddevice as sd

n_chroma = 12*3
device_info = sd.query_devices(None, 'input')
RATE = int(device_info['default_samplerate'])
CHANNEL = 1
CHUNK = 1024*5