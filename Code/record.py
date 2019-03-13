#Retrieved and modified from https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
import aubio
import pyaudio
import wave

###########################################################################
######################### Recording a WAV file ############################
###########################################################################

def record(data):
    CHUNK = 1024 #measured in bytes
    FORMAT = pyaudio.paInt16
    CHANNELS = 2 #stereo
    RATE = 44100 #common sampling frequency
    
    #Modification: modfied to take in a specified recording length and filepath
    if data.recordLength == "":
        RECORD_SECONDS = 5
    else:
        RECORD_SECONDS = int(data.recordLength)
    
    if data.songName == "":
        name = "File"
    else:
        name = data.songName
        
    y = 11*data.height // 12
    x = data.width // 2

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    data.isRecording = True

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        songData = stream.read(CHUNK)
        frames.append(songData)


    stream.stop_stream()
    stream.close()
    p.terminate()
    
    data.isRecording = False
    
    
    wf = wave.open("Songs/" + name + ".wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    data.recordLength = ""
    data.songName = ""
    