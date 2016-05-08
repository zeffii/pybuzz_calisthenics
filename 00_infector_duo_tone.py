# pybuzz is py2.4+ (not 3.x+ i think...)
# edited from supplied python file bassdrum.py

from buzz import *

#            index | name
#            ------+--------------------
#            0     | beatsPerMin
#            1     | ticksPerBeat
#            2     | samplesPerSec
#            3     | samplesPerTick
#            4     | posInTick
#            5     | ticksPerSec

bpm = 0
tpb = 0
sps = 0
spt = 0
pit = 0
tps = 0

trigger = NOTE_NO
tick = 0

def UpdateMasterInfo():
    global bpm,tpb,sps,spt,pit,tps
    bpm,tpb,sps,spt,pit,tps = GetMasterInfo()

def OnStop():
    global trigger,tick
    trigger = NOTE_NO
    tick = 0

def OnTick():
    # on each tick pick from the midicpt pool of integers
    # loop continuously. Play a note on track 0 and play 4 semitones higher on track 1.
    gk = [65,64,74,65,86,73]
    global trigger,tick,tpb
    if (trigger != NOTE_NO):
        gnote = gk[tick % len(gk)]
        SendPeerCtrlChange(0, 0, gnote)
        SendPeerCtrlChange(0, 1, gnote+4)
        tick += 1
    
def OnCommand(text):
    print text

def OnParameter(track,index,value):
    global trigger,tick
    print "[%02i] %i: %i" % (track,index,value)
    if (index == 0):
        if (value == NOTE_OFF):
            trigger = NOTE_NO
        else:
            trigger = value
        tick = 0        

def OnMasterInfoChange():
    UpdateMasterInfo()

def OnSave():
    print "Saving state..."
    return [4,2,8,"ficken"]
    
def OnLoad(data):
    print "Loading state..."
    print "State is " + str(data)

SetEventTarget("OnTick",OnTick)
SetEventTarget("OnCommand",OnCommand)
SetEventTarget("OnParameter",OnParameter)
SetEventTarget("OnMasterInfoChange",OnMasterInfoChange)
SetEventTarget("OnStop",OnStop)
SetEventTarget("OnSave",OnSave)
SetEventTarget("OnLoad",OnLoad)

UpdateMasterInfo()
SetPeerCtrlName(0,"Note Out")
