#Playing SOng during game
import pyaudio
import wave
import sys


def getSong(folder, data):
    #once song chosen, get the song and intialize song data
    data.wf = wave.open(folder + "/" + data.course, 'rb')
    data.chunk = 1024
    data.songData = data.wf.readframes(data.chunk)
    

def initializeSong(data):
    #initialize a song object to play the song
    data.audio = pyaudio.PyAudio()
    
#when time starts -> start song
def startSong(data):
    #start the song of current course
    data.stream = data.audio.open(format=\
    data.audio.get_format_from_width(data.wf.getsampwidth()),
                    channels=data.wf.getnchannels(),
                    rate=data.wf.getframerate(),
                    output=True)
      

def playSong(data):
    #play the song of current course
    data.stream.write(data.songData, 1024)
    data.songData = data.wf.readframes(data.chunk)
    
    
def endSong(data):
    #once game ends, stop the stream
    
    data.stream.stop_stream()
    data.stream.close()
    data.audio.terminate()