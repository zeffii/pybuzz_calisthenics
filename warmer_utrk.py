# pybuzz is py2.4+ (not 3.x+ i think...)
# edited from supplied python file bassdrum.py

import sys
sys.path.append(r'C:\Python24\Lib')

import random
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

send_pcc = SendPeerCtrlChange

def hex_to_int(hex_val):
    hex_val = str(hex_val) # just in case
    return int("0x" + hex_val, 0)

def seq_sample_from(items, tick):
    num_items = len(items)
    return items[tick % num_items]

def random_choice(items):
    index = random.randint(0, len(items)-1)
    return items[index]


def utrk9p(trk=0, offset=None, note=None, smp=None, vol=None, pan=None, p1=None, p1val=None, p2=None, p2val=None):
    for assignment_idx, param in enumerate([offset, note, smp, vol, pan, p1, p1val, p2, p2val]):
        if not (param is None): 
            send_pcc(assignment_idx, trk, param)


def UpdateMasterInfo():
    global bpm,tpb,sps,spt,pit,tps
    bpm,tpb,sps,spt,pit,tps = GetMasterInfo()

def OnStop():
    global trigger,tick
    trigger = NOTE_NO
    tick = 0

def OnTick():

    global trigger,tick,tpb
    if (trigger != NOTE_NO):

        # Example 1
        trigger_explicits = [0, 2, 4, 6, 8, 10, 12, 14]
        if (tick in trigger_explicits):
            # pick a random sample from these waveslots
            wave_idx = random_choice([5, 6, 7, 8])
            r_vol = random_choice([34,35,37,20])
            r_pan = random_choice([40, 60])
            hexval = hex_to_int(random_choice(["5000", "aa00", "2a00", "8400", "3a20"]))
            p1 = hex_to_int(19)
            # utrk9p(trk=0, offset=None, note=65, smp=wave_idx, vol=r_vol, pan=r_pan, p1=19, p1val=None, p2=None, p2val=None)
            utrk9p(trk=0, note=65, smp=wave_idx, pan=r_pan, vol=r_vol, p1=p1, p1val=hexval)

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
