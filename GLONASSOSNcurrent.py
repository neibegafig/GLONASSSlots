import requests
import time
import os, psutil
import numpy as np
import sys
import datetime
sys.path.insert(0, 'D:\RANDOMFILES\AFIT\Thesis\Python Code\prototypeauto')

url = 'https://www.glonass-iac.ru/en/GLONASS/'

# In theory this script should continuously be checking the TLE master from
# Celestrack every 15 minutes, for 24 hours, and every 15 minutes will download 
# a new copy of updated TLEs for GNSS satellites, if there are any. There might
# not always be updates, but at least it checks. After 24 hours, it stops the 
# program entirely. This should be run in its own IPython console because of the
# time sleep command. If theres a way around this that might be more useful,
# then awesome!
starttime = datetime.datetime.now()
while(True):
    timecheck = datetime.datetime.now()
    time.sleep(1)
    try:
        r = requests.get(url, allow_redirects=True)
        
        GOSNsave = str('GLONASS_OSN_Current_' + str(datetime.datetime.now())[0:19] + ".txt")
        GOSNsave = GOSNsave.replace('-', '_')
        GOSNsave = GOSNsave.replace(':', '-')
        open(GOSNsave, 'wb').write(r.content)
        print("saved ", GOSNsave, ".")
        print()

        break
    except:
        print("Connection error, trying again.")
        pass

    if timecheck.day == (starttime.day + 1):
        break
    
    
glonasslines = open(GOSNsave, 'r').readlines()
GlonassSlots = []

class GlonassOrbitSlot(object):
    def __init__(self):
        self.orbitslot = 0
        self.orbitplane = 0
        self.RFchannel = 0
        self.GlonassNumber = 0
        self.launchdate = ''
        self.opstartdate = ''
        self.openddate = ''
        self.lifetime = 0
        self.healthinalmanac = ''
        self.inephemeris = ''
        self.comment = ''
        
    def printrow(self):
        print("Orbit slot:         ", self.orbitslot)
        print("Orbit plane:        ", self.orbitplane)
        print("RF Channel:         ", self.RFchannel)
        print("GlonassNumber:      ", self.GlonassNumber)
        print("Launch Date:        ", self.launchdate)
        print("Ops Start date:     ", self.opstartdate)
        print("Ops end date:       ", self.openddate)
        print("Lifetime (months):  ", self.lifetime)
        print("In Almanac?:        ", self.healthinalmanac)
        print("In Ephemeris (UTC): ", self.inephemeris)
        print("Comment:            ", self.comment)
        print()

def ProcessGLONASS(filename):
    glonasslines = open(filename, 'r').readlines()
    GlonassSlots = []
    for line in range(len(glonasslines)):
    
        if glonasslines[line].startswith('<caption>GLONASS Constellation Status at'):
            status = glonasslines[line]
            status = status.replace('<caption>', '')
            status = status.replace('</caption>', '.')
            print(status)
    
        if "<tr bgcolor=" in glonasslines[line]:
            tablerow = glonasslines[line+1:line+12]
            GOrb = GlonassOrbitSlot()
            # 11 lines
            # Line 1
            tablerow[0] = tablerow[0].replace('<td width="6%">', '')
            tablerow[0] = tablerow[0].replace('</td>\n', '')
            GOrb.orbitslot = int(tablerow[0])
            # Line 2
            tablerow[1] = tablerow[1].replace('<td width="4%">', '')
            tablerow[1] = tablerow[1].replace('</td>\n', '')
            GOrb.orbitplane = int(tablerow[1])        
            # Line 3
            tablerow[2] = tablerow[2].replace('<td width="6%">', '')
            tablerow[2] = tablerow[2].replace('</td>\n', '')
            if '&nbsp' in tablerow[2]:
                GOrb.RFchannel = str(tablerow[2])
            elif not ('&nbsp' in tablerow[2]):
                GOrb.RFchannel = int(tablerow[2])        
            # Line 4
            tablerow[3] = tablerow[3].replace('<td width="6%">', '')
            tablerow[3] = tablerow[3].replace('</td>\n', '')
            GOrb.GlonassNumber = int(tablerow[3])        
            # Line 5
            tablerow[4] = tablerow[4].replace('<td width="8%">', '')
            tablerow[4] = tablerow[4].replace('</td>\n', '')
            GOrb.launchdate = tablerow[4]        
            # Line 6
            tablerow[5] = tablerow[5].replace('<td width="8%">', '')
            tablerow[5] = tablerow[5].replace('</td>\n', '')
            GOrb.opstartdate = tablerow[5]        
            # Line 7
            tablerow[6] = tablerow[6].replace('<td width="8%">', '')
            tablerow[6] = tablerow[6].replace('</td>\n', '')
            GOrb.openddate = tablerow[6]        
            # Line 8
            tablerow[7] = tablerow[7].replace('<td width="8%">', '')
            tablerow[7] = tablerow[7].replace('</td>\n', '')
            GOrb.lifetime = float(tablerow[7])        
            # Line 9
            tablerow[8] = tablerow[8].replace('<td width="8%">', '')
            tablerow[8] = tablerow[8].replace('</td>\n', '')
            GOrb.healthinalmanac = tablerow[8]        
            # Line 10
            tablerow[9] = tablerow[9].replace('<td width="14%">', '')
            tablerow[9] = tablerow[9].replace('</td>\n', '')
            GOrb.inephemeris = tablerow[9]       
            # Line 11
            tablerow[10] = tablerow[10].replace('<td width="18%">', '')
            tablerow[10] = tablerow[10].replace('</td>\n', '')
            GOrb.comment = tablerow[10]
            
            GlonassSlots.append(GOrb)

    myGLONASSslots = {}
    for slot in GlonassSlots:
        myGLONASSslots[slot.orbitslot] = slot.GlonassNumber
    return GlonassSlots, myGLONASSslots

GlonassSlots, SlotToGC = ProcessGLONASS(GOSNsave)
