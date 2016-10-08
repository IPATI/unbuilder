#coding: utf-8
#
# IPATI - Instrumental Transcommunication Research Institute - Brazil  
#
# IPATI UNBUILDER - system to shuffle voice segments to apply in transcontacts
#
# Segmentation module
#
# Last update: May, 2016
#
# This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
# You are free to share and adapt, but you must give appropriate credit, provide a link to the license, 
# and indicate if changes were made. Please read the license here: https://creativecommons.org/licenses/by-nc/4.0/
#
# Dependences needed to run this code:
#
# Debian-like linux:
# sudo aptitude install python2.7-dev libsndfile-dev python-scipy
# 
# Fedora-like linux:
# sudo dnf -y install python-devel libsndfile-devel freetype-devel scipy
# 
# sudo pip install --upgrade scikits.audiolab
# sudo pip install --upgrade numpy
# sudo pip install --upgrade matplotlib
# sudo pip install --upgrade pywavelets
# 
# ATTENTION: calibrated to Brazilian Portuguese speech

from scikits.audiolab import *
from pylab import *
import numpy as np
import pywt
import sys
import os

print '*************  IPATI UNBUILDER - SEGMENTATION *******************'
try:
	audio_file = sys.argv[1]
except:
	print "Use: python seg-ipaty.py audio.wav"
	quit()
if not(os.path.exists(audio_file)):
	print "File <<%s>> not found - verify if name is correct." % audio_file
	quit()
namefile=audio_file   #('depoimento_marlene1.wav')     # read file
directory=audio_file[0:-4] + '_segs'
os.mkdir(directory)
voice,Fs,bits=wavread(namefile)  
print "freq:",Fs
print "bits:",bits
voice = voice / max(abs(voice))             # normalize voice: range -1 to +1
tam=len(voice)
print "total length:",tam
level=2
filter='db4'  # daubechies 4 coefficiente allow best distribution
cca=voice
for i in range(0,level):
	cca,ccd=pywt.dwt(cca,filter)  # wavelet discreta: ca - low pass and cd - high pass 
length1=len(cca)
length2=len(ccd)
print "vector cca length:",length1

#&&&&&&&&&&&&&&&&&&&&&&  external limits wave definition
superior=max(ccd) # we use details coefficients
inferior=max(abs(ccd))
if superior >= inferior:
    limit_out=inferior
else:
    limit_out=superior
limit_in=limit_out * 0.1   # internal limit is external 10%

#@@@@@@@@@@@@@@@@@@@@@ 
n=[0]*length1 
cuts=[0]*length1
realcutpoint=[0]*tam
cont=0
open = False
start = end = 0
for i in range(2,len(cca)):
    w=cca[i]
    if (w < limit_out and w > -limit_out and (w > limit_in or w < -limit_in)):
        n[i]=w	# new wave, no extremes values
    else:
		if (n[i-2]>0 and n[i-1]==0) or (n[i-2]==0 and n[i-1]==0): 
			cuts[i]=1		# verify wavelet zero points 
		if cuts[i-1] == 1: 
			cont+=1
		else:
			cont == 0
			
		if cont >= 350:	# zero points count  =>TO DO VALIDATE<=
			realcutpoint[i*level*2]=0.5	# shifts cut point to original wave
			cont = 0
			#print "cut point: ",i*level*2
			if not(open):
				start = i*level*2
				open = True
			else:
				end = i*level*2
				if (end-start)>3900:	# number of minimal point to perceive vocalization
					file="%s/seg%d-%d.wav" % (directory,start,end)
					wavwrite(voice[start:end],file,Fs)
				start = i*level*2 + 1
			
#%%%%%%%%%%% show graph
'''
figure
plot(voice,'y')
plot(realcutpoint,'r+')
show()
'''
############################ END OF FILE ############################
