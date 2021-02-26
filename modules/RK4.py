def ordre_d(f, v_init, T, h, param):
        
    '''Calcul des listes de valeurs de x et de dx/dt 
    et les renvoie sous forme d'un tuple (x, dx/dt)'''
       
    X  = [v_init[0]]
    Xp = [v_init[1]]
    for i in range(len(T)-1): 
        #initialisation des paramètres de chaque étape
        xn  = X[-1]
        xpn = Xp[-1]
        t   = T[i]
        #calcul des coefficients
        k1 = f(xn, t, param)
        k2 = f(xn + xpn*h / 2, t + h / 2, param)
        k3 = f(xn + xpn*h / 2 + k1*(h / 2)**2, t + h / 2, param)
        k4 = f(xn + xpn*h + k2*((h)**2) / 2, t + h, param)
        #calcul de theta_n+1 et de dtheta/dt_n+1
        xnpun = xn + xpn*h + ((h**2)/6)*(k1 + k2 + k3)
        xpnpun = xpn + (h / 6)*(k1 + 2*k2 + 2*k3 + k4)
        X.append(xnpun)
        Xp.append(xpnpun)
    return(X, Xp)
