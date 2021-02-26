import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from modules import RK4, draw

#Constantes du système:
M = 1 #masse des disques en kg
R = 0.3 #rayon des disques en m
l = 0.5 #distance du centre du pendule au centre d'un des disques en m
V0 = 1000 #maximum de potentiel du pendule kg*m^2/s^2
alphaM = 0.14 #distance angulaire où la répulsion due à l'aimant se fait sentir en rad
tmax = 10 #instant final en s
h = 0.001 #pas de l'itération (et du temps)

theta0_in  = 2*np.pi/3 #angle de départ du pendule en rad
thetap0_in = 0 #vitesse angulaire de départ du pendule en rad/s
alpha0_in  = np.pi/2 #angle de départ de l'aimant en rad
omega_in   = 10 #pulsation de l'aimant en rad/s


#Listes de paramètres:
var_in = [omega_in, theta0_in, thetap0_in, alpha0_in]
var    = [omega_in, theta0_in, thetap0_in, alpha0_in]
theta_in = [var[1], var[2]]
param_eq = (M, R, l, V0, alphaM)
param    = [M, R, l, V0, alphaM, tmax, h]

#Création de la fonction alpha et du vecteur de temps:
def alpha(t, var):
    return(var[3]*np.cos(var[0]*t))
T = np.arange(0, tmax+h, h) #temps en s

#On définit tout d'abord la fonction de l'équation différentielle:
def f(theta, t, param):
    cste = (-4*param[3]*param[4]**2)/(3*param[0]*(4*param[2]**2+param[1]**2))
    f0 = (-2*(theta - alpha(t, var)))/((param[4]**2+(theta - alpha(t, var))**2)**2)
    f1 = (-2*(theta - alpha(t, var) + 2*np.pi/3))/((param[4]**2+(theta - alpha(t, var) + 2*np.pi/3)**2)**2)
    f2 = (-2*(theta - alpha(t, var) + 4*np.pi/3))/((param[4]**2+(theta - alpha(t, var) + 4*np.pi/3)**2)**2)
    return(cste*(f0+f1+f2))        
#On effectue le calcul de la solution en appellant ensuite le paquet RK4:        
Theta, Thetap = np.array(RK4.ordre_d(f, theta_in, T, h, param))

ani_c = draw.courbes_anim(var, var_in, Theta, Thetap, alpha, T, param)
ani_p = draw.pendule(alpha, Theta, T, param, var)

plt.show()