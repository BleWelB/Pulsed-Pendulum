import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from modules import draw_comp, draw, RK4

#constantes du système
M = 1 #masse des disques en kg
R = 0.3 #rayon des disques en m
l = 0.5 #distance du centre du pendule au centre d'un des disques en m
V0 = 1000 #maximum de potentiel du pendule kg*m^2/s^2
alphaM = 0.14 #distance angulaire où la répulsion due à l'aimant se fait sentir en rad
tmax = 2 #instant final en s
h = 0.005 #pas de l'itération (et du temps)

T = np.arange(0, tmax+h, h) #temps en s

theta0_in  = 0 #angle de départ du pendule en rad
thetap0_in = 0 #vitesse angulaire de départ du pendule en rad/s²
alpha0_in  = np.pi/2 #angle de départ de l'aimant en rad
omega_in   = 10 #pulsation de l'aimant en rad/s

#listes de paramètres
var_in = [omega_in, theta0_in, thetap0_in, alpha0_in]
var    = [omega_in, theta0_in, thetap0_in, alpha0_in]
theta_in = [var[1], var[2]]
param_eq = (M, R, l, V0, alphaM)
param    = [M, R, l, V0, alphaM, tmax, h]

#création de la fonction alpha:
def alpha(t, var):
    return(var[3]*np.cos(var[0]*t))

#On définit tout d'abord la fonction de l'équation différentielle
def f(theta, t, param):
    cste = (-2*param[3]*param[4]**2)/(3*param[0]*(2*param[2]**2+param[1]**2))
    f0 = (-2*(theta - alpha(t, var)))/((param[4]**2+(theta - alpha(t, var))**2)**2)
    f1 = (-2*(theta - alpha(t, var) + 2*np.pi/3))/((param[4]**2+(theta - alpha(t, var) + 2*np.pi/3)**2)**2)
    f2 = (-2*(theta - alpha(t, var) + 4*np.pi/3))/((param[4]**2+(theta - alpha(t, var) + 4*np.pi/3)**2)**2)
    return(cste*(f0+f1+f2))        
#on appelle ensuite le paquet RK4:        
Theta1, Thetap1 = np.array(RK4.ordre_d(f, theta_in, T, h, param))

def eq(theta, t, M, R, l, V0, alphaM):
    g0 = theta[1]
    cste = (-2*param[3]*param[4]**2)/(3*param[0]*(2*param[2]**2+param[1]**2))
    f0 = (-2*(theta[0] - alpha(t, var)))/((param[4]**2+(theta[0] - alpha(t, var))**2)**2)
    f1 = (-2*(theta[0] - alpha(t, var) + 2*np.pi/3))/((param[4]**2+(theta[0] - alpha(t, var) + 2*np.pi/3)**2)**2)
    f2 = (-2*(theta[0] - alpha(t, var) + 4*np.pi/3))/((param[4]**2+(theta[0] - alpha(t, var) + 4*np.pi/3)**2)**2)
    g1 = cste*(f0+f1+f2)
    return g0,g1
#calcul de theta avec scipy:
theta = odeint(eq, theta_in, T, args=param_eq)
Theta2, Thetap2 = theta[:,0], theta[:,1]
Theta, Thetap = (Theta2-Theta1)/Theta2, (Thetap2-Thetap1)/Thetap2

draw_comp.courbes(var, var_in, Theta, Thetap, alpha, T, param, f, eq)
plt.show()