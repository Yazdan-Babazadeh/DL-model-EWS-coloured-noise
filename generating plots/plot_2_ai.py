# -*- coding: utf-8 -*-
"""plot 2 AI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13s8f0gO3Uduu4El8R4oveheAiyF-zg83
"""

!pip install tensorflow==2.12.1

from google.colab import files
uploaded = files.upload()

from tensorflow.keras.models import load_model
model = load_model('Normal_form_CNN_LSTM_r=0.h5')

import numpy as np
import matplotlib.pyplot as plt
import random


steps = 10000
dt = 10**-2
X = np.zeros(steps)
Y = np.zeros(steps)
X[0] = 0
Y[0] = 0

def x_dot(x,y,mu):
    return y
def y_dot(x,y,mu):
    return mu*(1-x**2)*y-x

mu = -5.0
d_mu = (1-mu)/steps
sigma = 0.1

for i in range(0,steps-1):
    X[i+1] = X[i] + x_dot(X[i],Y[i],mu)*dt + (sigma*np.sqrt(dt)*random.gauss(0,1))
    Y[i+1] = Y[i] + y_dot(X[i],Y[i],mu)*dt + (sigma*np.sqrt(dt)*random.gauss(0,1))
    mu = mu + d_mu

X1 = X
t11 = np.linspace(0,1,steps)
plt.plot(t11,X1)
plt.title("Van der Pol Oscillator - Hopf Bifrucation")
plt.xlabel("Time")
plt.ylabel("X")
plt.axvline(x=0.85,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')
plt.show()

import statsmodels.api as sm
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.tsa.seasonal import seasonal_decompose
steps2 = len(X1)
steps = 1000
intervals = 400
sigmaa = 100
padding = 100
size = int(((steps2/steps)-1)*intervals)+1
Y = np.zeros((size,steps))
Y2 = np.zeros(steps+(2*padding))
t = np.zeros(size)
for i in range(0,size):
  j1=int(i*steps/intervals)
  j2 = j1+steps
  #j=i
  Y[i,:] = X[j1:j2]
  #Y2[padding:steps+padding] = Y[i,:]
  #frac = 0.75
  Y[i,:] = Y[i,:]-(gaussian_filter1d(Y[i,:], sigmaa,mode = 'nearest'))
  #Y2[i,:] = Y[i,100:1100]
  #Y[i,:] = Y2[padding:steps+padding]
  Y[i,:] = (Y[i,:]-np.average(Y[i,:]))/(np.std(Y[i,:]))
  #Y2[i,:] = (Y2[i,:]-np.average(Y2[i,:]))/(np.std(Y2[i,:]))
  #smoothed = sm.nonparametric.lowess(Y[i,:], np.arange(len(Y[i,:])), frac=frac)
  #Y[i,:] = (Y[i,:]-smoothed[:,1])/(np.std(Y[i,:]-smoothed[:,1]))

np.shape(Y)
predict_x=model.predict(Y)
output=np.argmax(predict_x,axis=1)

fold1_prob = predict_x[:,0]
#fold2_prob = predict_x[:,1]
Trans1_prob = predict_x[:,1]
#Trans2_prob = predict_x[:,3]
Hopf_prob = predict_x[:,2]
Null_prob = predict_x[:,3]
t= np.linspace(steps,steps2,size)
#t= t*50/size
plt.plot(t,fold1_prob,"r",label="fold")
#plt.plot(t,fold2_prob,"r",label="fold")
plt.plot(t,Trans1_prob,'g',label="trans1")
#plt.plot(t,Trans2_prob,'g',label="trans")
plt.plot(t,Hopf_prob,'y',label="Hopf")
plt.plot(t,Null_prob,'b',label="null")
#plt.plot(t,null_fold_prob,'y',label="Null_Fold")

plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Time")
plt.axvline(x=0.7,color='black',ls='--', ymin=0,ymax=1,label='Alpha=0.55')

window_size = 50

Fold1 = np.convolve(fold1_prob, np.ones(window_size)/window_size, mode='valid')

Trans1 = np.convolve(Trans1_prob, np.ones(window_size)/window_size, mode='valid')
#Trans2_prob = np.convolve(Trans2_prob, np.ones(window_size)/window_size, mode='valid')
Hopf1 = np.convolve(Hopf_prob, np.ones(window_size)/window_size, mode='valid')
Null1 = np.convolve(Null_prob, np.ones(window_size)/window_size, mode='valid')

t12= np.linspace(0,1,np.size(Hopf1))
plt.plot(t12,Hopf1,"y",label="Hopf")
plt.plot(t12,Trans1,"g",label="Trans")
#plt.plot(t,Trans2_prob,"brown",label="Trans2")
plt.plot(t12,Fold1,'r',label="fold")
plt.plot(t12,Null1,'b',label="null")
#plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Scaled Time")
plt.title("Van der Pol Oscillator - Hopf Bifurcation")
#plt.axvline(x=0.6,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')
plt.axvline(x=0.85,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')

import numpy as np
import random
import matplotlib.pyplot as plt


steps = 10000
I = np.zeros(steps)
gamma = 5
beta = 0
d_beta = (5-beta)/steps

I[0] = 0
dt = 10**-2
def I_dot(i,beta):
  a = beta*i*(1-i)
  b = gamma*i
  return a-b
sigma = 0.01
for i in range(0,steps-1):
  I[i+1] = I[i] + I_dot(I[i],beta)*dt + sigma*np.sqrt(dt)*np.random.normal(0,1)
  beta = beta + d_beta

t = np.linspace(0,1,steps)

plt.plot(t,I)
plt.title("SIS model - Transcritical")
plt.xlabel("Time")
plt.ylabel("I")
plt.show()
X2 = I
t21 = t

import statsmodels.api as sm
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.tsa.seasonal import seasonal_decompose
steps2 = len(X2)
steps = 1000
intervals = 400
sigmaa = 100
padding = 100
size = int(((steps2/steps)-1)*intervals)+1
Y = np.zeros((size,steps))
Y2 = np.zeros(steps+(2*padding))
t = np.zeros(size)
for i in range(0,size):
  j1=int(i*steps/intervals)
  j2 = j1+steps
  #j=i
  Y[i,:] = I[j1:j2]
  #Y2[padding:steps+padding] = Y[i,:]
  #frac = 0.75
  Y[i,:] = Y[i,:]-(gaussian_filter1d(Y[i,:], sigmaa,mode = 'nearest'))
  #Y2[i,:] = Y[i,100:1100]
  #Y[i,:] = Y2[padding:steps+padding]
  Y[i,:] = (Y[i,:]-np.average(Y[i,:]))/(np.std(Y[i,:]))
  #Y2[i,:] = (Y2[i,:]-np.average(Y2[i,:]))/(np.std(Y2[i,:]))
  #smoothed = sm.nonparametric.lowess(Y[i,:], np.arange(len(Y[i,:])), frac=frac)
  #Y[i,:] = (Y[i,:]-smoothed[:,1])/(np.std(Y[i,:]-smoothed[:,1]))

np.shape(Y)
predict_x=model.predict(Y)
output=np.argmax(predict_x,axis=1)

fold1_prob = predict_x[:,0]
#fold2_prob = predict_x[:,1]
Trans1_prob = predict_x[:,1]
#Trans2_prob = predict_x[:,3]
Hopf_prob = predict_x[:,2]
Null_prob = predict_x[:,3]
t= np.linspace(steps,steps2,size)
#t= t*50/size
plt.plot(t,fold1_prob,"r",label="fold")
#plt.plot(t,fold2_prob,"r",label="fold")
plt.plot(t,Trans1_prob,'g',label="trans1")
#plt.plot(t,Trans2_prob,'g',label="trans")
plt.plot(t,Hopf_prob,'y',label="Hopf")
plt.plot(t,Null_prob,'b',label="null")
#plt.plot(t,null_fold_prob,'y',label="Null_Fold")

plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Time")
plt.axvline(x=0.7,color='black',ls='--', ymin=0,ymax=1,label='Alpha=0.55')

window_size = 100

Fold2 = np.convolve(fold1_prob, np.ones(window_size)/window_size, mode='valid')

Trans2 = np.convolve(Trans1_prob, np.ones(window_size)/window_size, mode='valid')
#Trans2_prob = np.convolve(Trans2_prob, np.ones(window_size)/window_size, mode='valid')
Hopf2 = np.convolve(Hopf_prob, np.ones(window_size)/window_size, mode='valid')
Null2 = np.convolve(Null_prob, np.ones(window_size)/window_size, mode='valid')

t22= np.linspace(0,1,np.size(Hopf2))
plt.plot(t22,Hopf2,"y",label="Hopf")
plt.plot(t22,Trans2,"g",label="Trans")
#plt.plot(t,Trans2_prob,"brown",label="Trans2")
plt.plot(t22,Fold2,'r',label="fold")
plt.plot(t22,Null2,'b',label="null")
#plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Scaled Time")
plt.title("Transcritical")
#plt.axvline(x=0.6,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')
plt.axvline(x=0.8,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import random

def u_dot(u,r):
  a = -u
  b = r/(1+np.exp(-5*(u-1)))
  return a+b

steps = 10000
u = np.zeros(steps)
u[0] = 4
r = 4
dr = (0-r)/steps
dt = 0.01
sigma = 0.03
for i in range(steps-1):
  u[i+1] = u[i] + u_dot(u[i],r)*dt + sigma*random.gauss(0,1)*np.sqrt(dt)
  r = r + dr

t = np.linspace(0,1,steps)

X3 = u
t31 = t

plt.plot(t,u)
plt.title("Neural Activation Model - Fold Bifurcation")
plt.xlabel("Time")
plt.ylabel("u")
plt.axvline(x=0.93,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')
plt.show()

import statsmodels.api as sm
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.tsa.seasonal import seasonal_decompose
steps2 = len(X3)
steps = 1000
intervals = 400
sigmaa = 100
padding = 100
size = int(((steps2/steps)-1)*intervals)+1
Y = np.zeros((size,steps))
Y2 = np.zeros(steps+(2*padding))
t = np.zeros(size)
for i in range(0,size):
  j1=int(i*steps/intervals)
  j2 = j1+steps
  #j=i
  Y[i,:] = u[j1:j2]
  #Y2[padding:steps+padding] = Y[i,:]
  #frac = 0.75
  Y[i,:] = Y[i,:]-(gaussian_filter1d(Y[i,:], sigmaa,mode = 'nearest'))
  #Y2[i,:] = Y[i,100:1100]
  #Y[i,:] = Y2[padding:steps+padding]
  Y[i,:] = (Y[i,:]-np.average(Y[i,:]))/(np.std(Y[i,:]))
  #Y2[i,:] = (Y2[i,:]-np.average(Y2[i,:]))/(np.std(Y2[i,:]))
  #smoothed = sm.nonparametric.lowess(Y[i,:], np.arange(len(Y[i,:])), frac=frac)
  #Y[i,:] = (Y[i,:]-smoothed[:,1])/(np.std(Y[i,:]-smoothed[:,1]))

np.shape(Y)
predict_x=model.predict(Y)
output=np.argmax(predict_x,axis=1)

fold1_prob = predict_x[:,0]
#fold2_prob = predict_x[:,1]
Trans1_prob = predict_x[:,1]
#Trans2_prob = predict_x[:,3]
Hopf_prob = predict_x[:,2]
Null_prob = predict_x[:,3]
t= np.linspace(steps,steps2,size)
#t= t*50/size
plt.plot(t,fold1_prob,"r",label="fold")
#plt.plot(t,fold2_prob,"r",label="fold")
plt.plot(t,Trans1_prob,'g',label="trans1")
#plt.plot(t,Trans2_prob,'g',label="trans")
plt.plot(t,Hopf_prob,'y',label="Hopf")
plt.plot(t,Null_prob,'b',label="null")
#plt.plot(t,null_fold_prob,'y',label="Null_Fold")

plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Time")
plt.axvline(x=0.7,color='black',ls='--', ymin=0,ymax=1,label='Alpha=0.55')

window_size = 50

Fold3 = np.convolve(fold1_prob, np.ones(window_size)/window_size, mode='valid')

Trans3 = np.convolve(Trans1_prob, np.ones(window_size)/window_size, mode='valid')
#Trans2_prob = np.convolve(Trans2_prob, np.ones(window_size)/window_size, mode='valid')
Hopf3 = np.convolve(Hopf_prob, np.ones(window_size)/window_size, mode='valid')
Null3 = np.convolve(Null_prob, np.ones(window_size)/window_size, mode='valid')

t32= np.linspace(0,1,np.size(Hopf3))
plt.plot(t32,Hopf3,"y",label="Hopf")
plt.plot(t32,Trans3,"g",label="Trans")
#plt.plot(t,Trans2_prob,"brown",label="Trans2")
plt.plot(t32,Fold3,'r',label="fold")
plt.plot(t32,Null3,'b',label="null")
#plt.legend(loc="lower left")
plt.ylabel("DL Probability")
plt.xlabel("Scaled Time")
plt.title("Transcritical")
#plt.axvline(x=0.6,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')
plt.axvline(x=12355/20000,color='black',ls='--', ymin=0,ymax=1,label='Alpha=15.69')

from google.colab import files
import matplotlib.pyplot as plt

# Set global font size
plt.rcParams.update({'font.size': 14})

# Create a figure with 6 subplots in a vertical layout (time series on top, DL analysis below)
fig, axs = plt.subplots(2, 3, figsize=(20, 12), sharex=True, gridspec_kw={'width_ratios': [1, 1, 1]})

# Define labels for each subplot
subplot_labels = ['A', 'B', 'C', 'D', 'E', 'F']

# Top row: Time series
axs[0, 0].plot(t11, X1, label="Time Series 1")
axs[0, 0].set_title("Van der Pol - Hopf")
axs[0, 0].set_ylabel("State")
axs[0, 0].axvline(x=0.82, color='black', linestyle='--', linewidth=1)
axs[0, 0].text(0, 1.05, subplot_labels[0], transform=axs[0, 0].transAxes, fontsize=16, fontweight='bold')

axs[0, 1].plot(t21, X2, label="Time Series 2")
axs[0, 1].set_title("SIS - Transcritical")
axs[0, 1].set_ylabel("State")
axs[0, 1].axvline(x=0.7, color='black', linestyle='--', linewidth=1)
axs[0, 1].text(0, 1.05, subplot_labels[1], transform=axs[0, 1].transAxes, fontsize=16, fontweight='bold')

axs[0, 2].plot(t31, X3, label="Time Series 3")
axs[0, 2].set_title("Neural Activation - Fold")
axs[0, 2].set_ylabel("State")
axs[0, 2].axvline(x=0.65, color='black', linestyle='--', linewidth=1)
axs[0, 2].text(0, 1.05, subplot_labels[2], transform=axs[0, 2].transAxes, fontsize=16, fontweight='bold')

# Bottom row: DL analysis results
axs[1, 0].plot(t12, Hopf1, color='darkgoldenrod', label="Hopf")
axs[1, 0].plot(t12, Trans1, color='green', label="Trans")
axs[1, 0].plot(t12, Fold1, color='red', label="Fold")
axs[1, 0].plot(t12, Null1, color='blue', label="Null")
axs[1, 0].set_title("DL Analysis - Hopf")
axs[1, 0].set_ylabel("DL Probability")
axs[1, 0].axvline(x=0.82, color='black', linestyle='--', linewidth=1)
axs[1, 0].legend(loc='upper left')
axs[1, 0].text(0, 1.05, subplot_labels[3], transform=axs[1, 0].transAxes, fontsize=16, fontweight='bold')

axs[1, 1].plot(t22, Hopf2, color='darkgoldenrod', label="Hopf")
axs[1, 1].plot(t22, Trans2, color='green', label="Trans")
axs[1, 1].plot(t22, Fold2, color='red', label="Fold")
axs[1, 1].plot(t22, Null2, color='blue', label="Null")
axs[1, 1].set_title("DL Analysis - Transcritical")
axs[1, 1].set_ylabel("DL Probability")
axs[1, 1].axvline(x=0.7, color='black', linestyle='--', linewidth=1)
axs[1, 1].legend(loc='upper left')
axs[1, 1].text(0, 1.05, subplot_labels[4], transform=axs[1, 1].transAxes, fontsize=16, fontweight='bold')

axs[1, 2].plot(t32, Hopf3, color='darkgoldenrod', label="Hopf")
axs[1, 2].plot(t32, Trans3, color='green', label="Trans")
axs[1, 2].plot(t32, Fold3, color='red', label="Fold")
axs[1, 2].plot(t32, Null3, color='blue', label="Null")
axs[1, 2].set_title("DL Analysis - Fold")
axs[1, 2].set_ylabel("DL Probability")
axs[1, 2].axvline(x=0.65, color='black', linestyle='--', linewidth=1)
axs[1, 2].legend(loc='upper left')
axs[1, 2].text(0, 1.05, subplot_labels[5], transform=axs[1, 2].transAxes, fontsize=16, fontweight='bold')

# Link x-axis across all plots
for ax in axs.flat:
    ax.set_xlabel("Scaled Time")

# Adjust layout
plt.tight_layout()
filename = "plot_with_labels.png"
fig.savefig(filename, dpi=300, bbox_inches="tight")

# Download the plot file
files.download(filename)
plt.show()