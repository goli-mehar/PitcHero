#### retrieved from: https://stackoverflow.com/questions/42934617/how-to-find-the-tempo-of-a-wav-with-aubio


from aubio import source, tempo
from numpy import median, diff
from random import randint


def get_file_bpm(path, params = None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except KeyError:
        """
        # super fast
        samplerate, win_s, hop_s = 4000, 128, 64 
        # fast
        samplerate, win_s, hop_s = 8000, 512, 128
        """
        # default:
        samplerate, win_s, hop_s = 44100, 1024, 512

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    beatsCourse = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            beatsCourse += [(this_beat)]
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm 
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        b = median(bpms)
    else:
        b = 0
        print("not enough beats found in {:s}".format(path))
    return b, beatsCourse

##### Build Obstacle
        
def buildCourseUnscaled(file):
    #taking song, build the unscaled version of its course
    bpm, beats = get_file_bpm(file)
    course = []
    for i in range(0, len(beats), 1):
        timeStamp = beats[i] * 10
        timeStamp = int(timeStamp)
        level = randint(0, 20)
        course += [(timeStamp, level)]
    return course
    
import os
def buildCourses(folder):
    #taking all possible songs, build the unscaled versions of the courses
    courses = dict()
    for song in os.listdir(folder):
        if ".DS_Store" in song:
            continue
        courses[song] = buildCourseUnscaled(folder + "/" + song)
    return courses