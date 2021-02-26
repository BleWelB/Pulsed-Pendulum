import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from matplotlib.widgets import Slider, Button
from scipy.integrate import odeint
import matplotlib as mpl

font = {'family': 'sans-serif',
        'weight': 'regular',
        'size': 16}
mpl.rc('font', **font)


def minmax(list):
        min_l = min(list)
        max_l = max(list)
        return min_l, max_l


def pendule(alpha, Theta, T, param, var):
    #Initialisation de la figure:
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))

    #Création de la liste des valeurs de alpha:
    Alpha = []
    for i in range(len(T)):
        Alpha.append(alpha(T[i], var))

    #Coordonnées des centres des cercles:
    x0, y0 = param[2] * np.cos(Theta), param[2] * np.sin(Theta)
    x1, y1 = param[2] * np.cos(Theta + 2 * np.pi / 3), param[2] * np.sin(Theta + 2 * np.pi / 3)
    x2, y2 = param[2] * np.cos(Theta + 4 * np.pi / 3), param[2] * np.sin(Theta + 4 * np.pi / 3)

    #Tracé des cercles:
    cercle0 = plt.Circle((0,0), param[1], facecolor= 'blue')
    cercle1 = plt.Circle((0,0), param[1], facecolor= 'blue')
    cercle2 = plt.Circle((0,0), param[1], facecolor= 'blue')
    
    #Barres:
    barre0, = ax.plot([],[],color='black')
    barre1, = ax.plot([],[],color='black')
    barre2, = ax.plot([],[],color='black')

    #Aimant:
    xa, ya = (param[2] + 3 * param[1]) * np.cos(Alpha), (param[2] + 3 * param[1]) * np.sin(Alpha)
    aimant = plt.Circle((0,0), 0.1, facecolor= 'red', label=r'Aimant sous excitation périodique de pulsation $\omega$')

    #Initialisation des objets:
    def init():
        cercle0.center = (0,0)
        cercle1.center = (0,0)
        cercle2.center = (0,0)
        ax.add_patch(cercle0)
        ax.add_patch(cercle1)
        ax.add_patch(cercle2)

        barre0.set_data([],[])
        barre1.set_data([],[])
        barre2.set_data([],[])

        aimant.center = (0,0)
        ax.add_patch(aimant)
        return cercle0, cercle1, cercle2, barre0, barre1, barre2, aimant,

    #Animation:
    def animate(i):
        if i == len(T):
            ani.frame_seq = ani.new_frame_seq()
            return cercle0, cercle1, cercle2, barre0, barre1, barre2, aimant,
        else:
            cercle0.center = (y0[i],x0[i])
            cercle1.center = (y1[i],x1[i])
            cercle2.center = (y2[i],x2[i])

            barre0.set_data([0,y0[i]],[0,x0[i]])
            barre1.set_data([0,y1[i]],[0,x1[i]])
            barre2.set_data([0,y2[i]],[0,x2[i]])

            aimant.center = (ya[i],xa[i])

            return cercle0, cercle1, cercle2, barre0, barre1, barre2, aimant,

    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    ani = animation.FuncAnimation(fig, animate, blit=True, init_func=init, interval=1, cache_frame_data=False)
    return ani


def courbes_anim(var, var_in, Theta, Thetap, alpha, T, param):
    #Initialisation de la figure et des axes:
    fig, ax = plt.subplots(1, 2)

    #Etiquettes des axes:
    ax[0].set_title(r'Trajectoire du pendule')
    ax[1].set_title(r"Trajectoire du pendule dans l'espace des phases")
    
    #Création de la liste des valeurs de alpha:
    Alpha = []
    for i in range(len(T)):
        Alpha.append(alpha(T[i], var))
        
    #On récupère le min et le max de theta et de dtheta/dt pour le dimensionnement des axes:
    alpmin, alpmax = minmax(Alpha)
    thmin, thmax = minmax(Theta)
    thpmin, thpmax = minmax(Thetap)

    #Dimensionnement des axes:
    ax[0].set_xlim(0, param[5])
    ax[0].set_ylim(min(thmin, alpmin), max(thmax, alpmax))
    ax[1].set_xlim(thmin, thmax)
    ax[1].set_ylim(param[0]*(param[2]**2)*thpmin, param[0]*(param[2]**2)*thpmax)
        
    #Initialisation des courbes:
    tth, = ax[0].plot([], [], label=r'$\theta(t)$')
    tal, = ax[0].plot([], [], label=r'$\alpha(t)$')
    thpth, = ax[1].plot([], [], label=r'$\frac{d\theta}{dt}(\theta)$')

    list_ani = [[], [], [], []]
    
    def init():
        tth.set_data(list_ani[3], list_ani[0])
        tal.set_data(list_ani[3], list_ani[1])
        thpth.set_data(list_ani[0], list_ani[2])
        return tth, tal, thpth     

    #Animation:
    def animate(i):
        if i >= len(T):
            return tth, tal, thpth
        else:
            list_ani[0].append(Theta[i])
            list_ani[1].append(Alpha[i])
            list_ani[2].append(param[0]*(param[2]**2)*Thetap[i])
            list_ani[3].append(T[i])
            
            tth.set_data(list_ani[3], list_ani[0])
            tal.set_data(list_ani[3], list_ani[1])
            thpth.set_data(list_ani[0], list_ani[2])
        return tth, tal, thpth
    
        ax[0].legend()
        ax[0].grid()
        ax[0].set_xlabel(r'Temps (s)')
        ax[0].set_ylabel(r'$\theta$ et $\alpha$')
        ax[1].legend()
        ax[1].grid()
        ax[1].set_xlabel(r'$\theta$')
        ax[1].set_ylabel(r'$\dot{\theta}$')

    ani = animation.FuncAnimation(fig, animate, blit=True, init_func=init, interval=1, cache_frame_data=False)
    return ani


def courbes(var, var_in, Theta, Thetap, alpha, T, param, eq):            
    #Initialisation de la figure:
    fig, ax = plt.subplots(1, 3)
    plt.subplots_adjust(top=0.70, bottom=0.1)

    #Boîtes des widgets:
    axom   = plt.axes([0.6, 0.90, 0.25, 0.05])
    axa0   = plt.axes([0.6, 0.80, 0.25, 0.05])
    axth0  = plt.axes([0.1, 0.90, 0.25, 0.05])
    axthp0 = plt.axes([0.1, 0.80, 0.25, 0.05])

    #Création des sliders:
    somega   = Slider(axom, r"Pulsation de l'aimant", 0, 40, valinit=var_in[0])
    salpha0  = Slider(axa0, r'$\alpha_0$', 0, 2*np.pi, valinit=var_in[3])
    stheta0  = Slider(axth0, r'$\theta_0$', 0, 2*np.pi/3, valinit=var_in[1])
    sthetap0 = Slider(axthp0, r'$\frac{d\theta}{dt}$', 0, 50, valinit=var_in[2])

    def reinit(var, var_in, Theta, Thetap, alpha, T, param):
        #Réinitalisation des axes:
        ax[0].clear()
        ax[1].clear() 
        ax[2].clear()
        
        #Etiquettes des axes:
        ax[0].set_title(r'Trajectoire du pendule')
        ax[1].set_title(r"Portrait de phase")
        ax[2].set_title(r"Spectre de Fourier")

        #Création de la liste des valeurs de alpha:
        Alpha = []
        for i in range(len(T)):
            Alpha.append(alpha(T[i], var))

        #On récupère le min et le max de theta et de dtheta/dt pour le dimensionnement des axes:
        alpmin, alpmax = minmax(Alpha)
        thmin, thmax = minmax(Theta)
        thpmin, thpmax = minmax(Thetap)

        #Calcul du spectre de Fourier:
        fs = 10000
        Ntfd = 3*len(Theta)
        fft = np.fft.fft(Theta, Ntfd)
        freq = np.arange(Ntfd)*fs/Ntfd

        #Dimensionnement des axes:
        ax[0].set_xlim(0, param[5])
        ax[0].set_ylim(min(thmin, alpmin), max(thmax, alpmax))
        ax[1].set_xlim(thmin, thmax)
        ax[1].set_ylim(param[0]*(param[2]**2)*thpmin, param[0]*(param[2]**2)*thpmax)
        ax[2].set_xlim(0, fs/3)

        #Tracé des courbes:
        ax[0].plot(T, Theta, label=r'$\theta(t)$')
        ax[0].plot(T, Alpha, label=r'$\alpha(t)$')
        ax[1].plot(Theta, param[0]*(param[2]**2)*Thetap, label=r'$\frac{d\theta}{dt}(\theta)$')
        ax[2].semilogy(freq, abs(fft))

        ax[0].legend()
        ax[0].grid()
        ax[0].set_xlabel(r'Temps (s)')
        ax[0].set_ylabel(r'$\theta$ et $\alpha$')
        ax[1].legend()
        ax[1].grid()
        ax[1].set_xlabel(r'$\theta$')
        ax[1].set_ylabel(r'$\dot{\theta}$')
        ax[2].grid()
        ax[2].set_xlabel(r'Fréquence (Hz)')

    #Action des sliders:
    def update(val):
        var[0] = somega.val
        var[1] = stheta0.val
        var[2] = sthetap0.val
        var[3] = salpha0.val
        theta_in = [var[1], var[2]]
        param_eq = (param[0], param[1], param[2], param[3], param[4])

        theta = odeint(eq, theta_in, T, args=param_eq)
        Theta, Thetap = theta[:,0], theta[:,1]
        reinit(var, var_in, Theta, Thetap, alpha, T, param)

    somega.on_changed(update)
    salpha0.on_changed(update)
    stheta0.on_changed(update)
    sthetap0.on_changed(update)
    
    reinit(var, var_in, Theta, Thetap, alpha, T, param)
    plt.show()