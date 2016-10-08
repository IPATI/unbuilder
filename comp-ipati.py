#coding: utf-8
#
# IPATI - Instrumental Transcommunication Research Institute - Brazil  
#
# IPATI UNBUILDER - system to shuffle voice segments to apply in transcontacts
#
# Composition module
#
# Last update: May, 2016
#
# This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
# You are free to share and adapt, but you must give appropriate credit, provide a link to the license, 
# and indicate if changes were made. Please read the license here: https://creativecommons.org/licenses/by-nc/4.0/
#
# Dependences needed to run this code:
#
# sudo pip install pydub
#

from pydub import AudioSegment
import glob
import random
import sys
import os.path

print '*************  IPATI UNBUILDER - COMPOSITION *******************'
try:
	dir_audio=sys.argv[1]
except:
	print "Use: python comp-ipaty.py folder"
	quit()
if not(os.path.exists(dir_audio)):
	print "Folder <<%s>> not found - verify if name is correct." % dir_audio
	quit()
files_dir_audio = dir_audio + '/*.wav'
files=glob.glob(files_dir_audio)     # read folder with segments files
#print files
length = len(files)
print "We have %d files!" % length
total = AudioSegment.from_wav(files[length/2]) # we start a mid file in folder
list=[length/2]
# to test, we generate 2 times larger than original file group
for i in range(length*3):
	s = random.randint(0,length-1)
	list.append(s)
	voice = AudioSegment.from_wav(files[s])
	total=total+voice

nomearq = dir_audio + "_composition.wav"
total.export(nomearq,format="wav")
print "Files sort order: ",list

############################ END OF FILE ############################
