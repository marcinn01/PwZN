import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

N = 10000
I0 = 5  
R0 = 1    
S0 = N - I0 - R0  
beta, gamma = 0.3, 0.1
tmax = 100
Nt = 100
t = np.linspace(0, tmax, Nt+1)

def SIR(X, t):
    S, I, R = X
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return np.array([dSdt, dIdt, dRdt])

y0 = S0, I0, R0 
result = odeint(SIR, y0, t)
S, I, R = result.T

plt.figure()
plt.title("Model SIR")
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered or Removed')
plt.xlabel(' t [dni]')
plt.ylabel('Populacja')
plt.ylim([0,N])
plt.legend()

plt.show()
