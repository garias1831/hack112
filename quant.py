import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import norm
from math import exp, sqrt, log
from datetime import datetime

def run_quant(K, σ, fulldate):
    # variable definition
    #K = 130 #Call srike price 
    r = 0.0527 #Fixed risk-free interest rate from the US treasury
    #σ = 0.4759#Implied volatility
    fulldate = fulldate
    #print(fulldate)

    # defining time (for second plot)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
            'August', 'September', 'October', 'November', 'December']
    current = datetime.now()
    datelist = fulldate.replace(',', '').split(' ')
    month = int(months.index(datelist[0])) + 1
    day = int(datelist[1])
    year = int(datelist[2])
    maturity = datetime(year, month, day)
    dateDifference = (maturity - current).days
    yearDifference = dateDifference/365.25

    # Black-Scholes formula
    def black_scholes_call(S, K, t, r, σ):
        d1 = (np.log(S / K) + (r + 0.5 * σ ** 2) * t) / (σ * np.sqrt(t))
        d2 = d1 - σ * np.sqrt(t)
        call = (S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2))
        return call

    # create a grid of x and y values
    t = np.linspace(0.001, yearDifference, 350)
    S = np.linspace(10, 350, 350)
    t, S = np.meshgrid(t, S)

    # defining c
    c = black_scholes_call(S, K, t, r, σ)

    # creating Figures and 3D axes
    fig = plt.figure(figsize=(17, 8))

    # plotting the 3d function
    ax1 = fig.add_subplot(121, projection='3d')
    surf1 = ax1.plot_surface(t, S, c, cmap='plasma', alpha = 0.85)
    fig.colorbar(surf1, ax = ax1, shrink = 0.5, aspect = 10, location = 'bottom')
    ax1.set_title('Black-Scholes model for (stock ticker)')

    # plotting the 2d function
    ax2 = fig.add_subplot(122)
    ax2.plot(S, black_scholes_call(S, K, yearDifference, r, σ))
    ax2.set_title(f'Black-Scholes model given {yearDifference} years')
    ax2.set_xlabel('Stock Price (S), in US Dollars')
    ax2.set_ylabel('Call Price (C), in US Dollars')

    # variable box
    variables = f'Strike Price (K) : {K}\nInterest Rate (r) : {r*100}%\nVolatility (σ) : {σ}'
    props = dict(boxstyle = 'round', facecolor = 'lavender', alpha = 0.9)
    ax1.text2D(-0.5 , 0.9, variables, transform = ax1.transAxes, fontsize = 11, 
            horizontalalignment = 'left', verticalalignment = 'top', bbox = props)

    # axes labelling
    ax1.set_xlabel('Time (T), in Years')
    ax1.set_ylabel('Stock Price (S), in US Dollars')
    ax1.set_zlabel('Call Price (C), in US Dollars')

    plt.show()