#coding: utf-8
#
# IPATI - International Instrumental Transcommunication Research Institute - Brazil  
#
# IPATI UNBUILDER - system to shuffle voice segments to apply in transcontacts
#
# Segmentation module
#
# Last update: April, 2016
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

from scikits.audiolab import *
from pylab import *
import numpy as np
import pywt

print '*************  IPATI UNBUILDER - SEGMENTATION *******************'
nomearq=('depoimento_marlene1.wav')     # leitura do arquivo
voz,Fs,bits=wavread(nomearq)  
print "freq:",Fs
print "bits:",bits
voz = voz / max(abs(voz))             # voz normalizada: range -1 to +1
tam=len(voz)
print "tamanho total:",tam
nivel=2
filtro='db4'  # daubechies com 4 coeficientes permite uma melhor distribuicao de coeficientes
cca=voz
for i in range(0,nivel):
	cca,ccd=pywt.dwt(cca,filtro)  # wavelet discreta: ca - passa baixa e cd - passa alta 
tam1=len(cca)
tam2=len(ccd)
print "tamanho vetor cca:",tam1

#&&&&&&&&&&&&&&&&&&&&&&  definição de limites externos na onda
superior=max(ccd) # usamos os coeficientes de detalhe
inferior=max(abs(ccd))
if superior >= inferior:
    limite_fora=inferior
else:
    limite_fora=superior
limite_dentro=limite_fora * 0.1   # limite interno é 10% do externo

#@@@@@@@@@@@@@@@@@@@@@ 
n=[0]*tam1 
cortes=[0]*tam1
pcortereal=[0]*tam
cont=0
abriu = False
inicio = fim = 0
for i in range(2,len(cca)):
    w=cca[i]
    if (w < limite_fora and w > -limite_fora and (w > limite_dentro or w < -limite_dentro)):
        n[i]=w	# nova onda, sem valores extremos
    else:
		if (n[i-2]>0 and n[i-1]==0) or (n[i-2]==0 and n[i-1]==0): 
			cortes[i]=1		# verifica pontos zerados na wavelet
		if cortes[i-1] == 1: 
			cont+=1
		else:
			cont == 0
			
		if cont >= 350:	# contagem de pontos zerados =>VALIDAR<=
			pcortereal[i*nivel*2]=0.5	# desloca o ponto de corte para onda original
			cont = 0
			#print "ponto de corte: ",i*nivel*2
			if not(abriu):
				inicio = i*nivel*2
				abriu = True
			else:
				fim = i*nivel*2
				if (fim-inicio)>3900:	# numero de pontos mínimo que se percebeu a vocalização
					arq="segs/seg%d-%d.wav" % (inicio,fim)
					wavwrite(voz[inicio:fim],arq,Fs)
				inicio = i*nivel*2 + 1
			
#%%%%%%%%%%% mostra gráfico
'''
figure
plot(voz,'y')
plot(pcortereal,'r+')
show()
'''
############################ END OF FILE ############################
