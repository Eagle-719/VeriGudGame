import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import Params

def ampfunction(f, L, C, dR):
    f = f * np.array(2) * np.pi
    f = np.asarray(f)
    L = float(L)
    R = float(Params.realOhmRes)
    C = float(C)
    dR = float(dR)
    return ((R) / (np.sqrt(np.square(R + dR) + np.square((L * f) - (1 / (C * f))))))

def main_activity():
    processed_data = open(Params.ResultsPath, "r")

    amp_values = []
    freq_values = []

    for row in processed_data:
        burst = row.split()
        amp_values.append(float(burst[1]))
        freq_values.append(float(burst[0]))

    popt, pcov = scipy.optimize.curve_fit(ampfunction, freq_values, amp_values, p0=(0.04, Params.Capacitor, 700))
    freq_smooth = np.linspace(min(freq_values), max(freq_values), 1000)
    amp_smooth = ampfunction(freq_smooth, *popt)

    Inductivity, Capacity, deltaR = popt
    Ind = float(Inductivity)
    Cap = float(Capacity)
    deltaR = float(deltaR)

    # Calculate R-squared
    residuals = np.array(amp_values) - ampfunction(np.array(freq_values), *popt)
    SSE = np.sum(residuals ** 2)
    SST = np.sum((np.array(amp_values) - np.mean(np.array(amp_values))) ** 2)
    R_squared = 1 - (SSE / SST)

    plt.plot(freq_smooth, amp_smooth, label=f'Fitted Curve (R²={R_squared:.4f})', color='red')
    plt.scatter(freq_values, amp_values, label='Data (UR/UT)')
    plt.title(f"{Params.subfolder} Fitted Curve")
    plt.legend()
    plt.show()

main_activity()