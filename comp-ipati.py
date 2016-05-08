#coding: utf-8
#
# IPATI - International Instrumental Transcommunication Research Institute - Brazil  
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

#from scikits.audiolab import *
from pydub import AudioSegment
import glob
import random

print '*************  IPATI UNBUILDER - COMPOSITION *******************'
arqs=glob.glob('segs/*.wav')     # leitura do diretório com segmentos
#print arqs
tam = len(arqs)
print "Temos %d arquivos!" % tam
total = AudioSegment.from_wav(arqs[tam/2]) # inicializamos lendo um arquivo do meio
lista=[tam/2]
# como teste, estou gerando um áudio 3 vezes maior que o grupo de arquivos
for i in range(tam*3):
	s = random.randint(0,tam-1)
	lista.append(s)
	voz = AudioSegment.from_wav(arqs[s])
	total=total+voz

nomearq="composicao.wav"
total.export(nomearq,format="wav")
print "Ordem de sorteio dos arquivos: ",lista

############################ END OF FILE ############################
