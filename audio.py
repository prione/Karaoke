import sounddevice as sd
import soundfile as sf
import numpy as np
import consts
import librosa

class record():
    def __init__(self, callback_indata):
   
        with sd.InputStream(
                callback=self.callback_closure(callback_indata),
                channels=consts.CHANNEL,
                samplerate=consts.RATE,
                blocksize=consts.CHUNK,
            ):

            sd.sleep(-1)

    def callback_closure(self, callback_indata):
        def callback(indata, frames, time, status):

            if status:
                print(status)
        
            callback_indata(indata)

        return callback


class play():
    def __init__(self, callback_time, inst):
        self.sig, sr = sf.read(inst, always_2d=True)

        self.n_samples, self.n_channels = self.sig.shape
        blocksize = 1024
        self.current_frame = 0

        with sd.OutputStream(
            samplerate=sr, 
            blocksize=blocksize,
            channels=self.sig.shape[1],
            callback=self.callback_closure(callback_time),
        ):
            # 再生終了まで待機
            sd.sleep(-1) 
            

    # コールバック関数
    def callback_closure(self, callback_time):
        def callback(outdata, frames, time, status):

            if status:
                print(status)
            
            chunksize = min(self.n_samples - self.current_frame, frames)
            
            outdata[:] *= 0.0
            # チャンネルごとの信号処理
            for k in range(self.n_channels): 
                outdata[0:chunksize, k] = self.sig[self.current_frame:self.current_frame + chunksize, k]

            if chunksize < frames:
                raise sd.CallbackStop()
                
            self.current_frame += chunksize
            current_time = time.outputBufferDacTime
            callback_time(current_time)

        return callback

class chroma_detection():

    def __init__(self):
        self.specs = np.zeros(consts.CHUNK//2+1)
        self.window = np.hamming(consts.CHUNK)
        self.chroma_pre = np.zeros(consts.n_chroma)        
        self.chroma = np.zeros(consts.n_chroma)
        self.chromafb = (librosa.filters.chroma(sr = consts.RATE, n_fft = consts.CHUNK, tuning=0.0, n_chroma=consts.n_chroma))**2

    def get_chroma(self, indata):
        pw = np.sqrt(np.mean(indata**2))

        if 0.01< pw:
            sig = np.reshape(indata, (consts.CHUNK, consts.CHANNEL)).T
            sig[:] = sig[:] * self.window
            self.specs[:] = np.abs(np.fft.rfft(sig))**2
            self.chroma[:] = np.dot(self.chromafb, self.specs)
            self.chroma[:] = self.chroma / (np.max(self.chroma)+1e-16)
            self.chroma[:] = 0.3*self.chroma+0.7*self.chroma_pre
            self.chroma_pre[:] = self.chroma

            chroma = np.argmax(self.chroma)/(consts.n_chroma//12)

        else:
            chroma = None
        
        # if 0.01< pw:
        #     data=np.frombuffer(indata,dtype="int16")
        #     fd = np.fft.fft(data)
        #     fft_data = np.abs(fd[:consts.CHUNK//2])
        #     freq=np.fft.fftfreq(consts.CHUNK, d=1/consts.RATE)

        #     val=freq[np.argmax(fft_data)]
        #     offset = 0.5 if val >= 440 else -0.5
        #     chroma = (np.log2((val/440.0)**12)+offset) % 12
        #     chroma = chroma - 2 if 2 < chroma else chroma + 10

        #     if chroma == float("inf") or chroma == -float("inf") or chroma == np.nan:
        #         chroma = None
        # else:
        #     chroma = None

        return chroma