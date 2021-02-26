import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from matplotlib.widgets import Slider, Button
from scipy.integrate import odeint
from modules import RK4


def minmax(list):
        min_l, max_l = 0, 0
        for i in range(len(list)):
            if list[i] == None:
                pass
            elif list[i] <= min_l:
                min_l = list[i]
            elif list[i] >= max_l:
                max_l = list[i]         
        return min_l, max_l


def courbes(var, var_in, Theta, Thetap, alpha, T, param, f, eq):            
    #initialisation de la figure:
    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(top=0.70, bottom=0.1)

    #boites des widgets:
    axom   = plt.axes([0.6, 0.90, 0.25, 0.05])
    axa0   = plt.axes([0.6, 0.80, 0.25, 0.05])
    axh  = plt.axes([0.1, 0.90, 0.25, 0.05])

    #widgets:
    somega   = Slider(axom, r"Pulsation de l'aimant", 0, 20, valinit=var_in[0])
    salpha0  = Slider(axa0, r'$\alpha_0$', 0, 2*np.pi, valinit=var_in[3])
    sh  = Slider(axh, r'$h$', 0, 0.01, valinit=0.01)

    def reinit(var, var_in, Theta, Thetap, alpha, T, param):
        #réinitalisation des axes:
        ax[0].clear()
        ax[1].clear() 
        
        #étiquettes des axes:
        ax[0].set_title(r'Trajectoire du pendule')
        ax[1].set_title(r"Vitesse du pendule")

        #création de la liste des valeurs de alpha:
        Alpha = []
        for i in range(len(T)):
            Alpha.append(alpha(T[i], var))
        
        #On récupère le min et le max de theta et de dtheta/dt pour le dimensionnement des axes:
        alpmin, alpmax = minmax(Alpha)
        thmin, thmax = minmax(Theta)
        thpmin, thpmax = minmax(Thetap)

        #dimensionnement des axes:
        ax[0].set_xlim(0, param[5])
        ax[0].set_ylim(min(thmin, alpmin), max(thmax, alpmax))
        ax[1].set_xlim(0, param[5])
        ax[1].set_ylim(param[0]*(param[2]**2)*thpmin, param[0]*(param[2]**2)*thpmax)

        #Tracé
        ax[0].plot(T, Theta, label=r'$\Delta \theta(t)$')
        ax[1].plot(T, param[0]*(param[2]**2)*Thetap, label=r'$\Delta\frac{d\theta}{dt}(t)$')

        ax[0].legend()
        ax[0].grid()
        ax[1].legend()
        ax[1].grid()

    #action du bouton
    def update(val):
        var[0] = somega.val
        var[3] = salpha0.val
        param[6] = sh.val
        theta_in = [var[1], var[2]]
        param_eq = (param[0], param[1], param[2], param[3], param[4])

        Theta1, Thetap1 = np.array(RK4.ordre_d(f, theta_in, T, param[6], param))
        theta = odeint(eq, theta_in, T, args=param_eq)
        Theta2, Thetap2 = theta[:,0], theta[:,1]
        Theta, Thetap = Theta2-Theta1, Thetap2-Thetap1

        reinit(var, var_in, Theta, Thetap, alpha, T, param)

    somega.on_changed(update)
    salpha0.on_changed(update)
    sh.on_changed(update)
    
    reinit(var, var_in, Theta, Thetap, alpha, T, param)
    plt.show()