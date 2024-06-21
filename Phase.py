import numpy as np
import scipy.optimize
import Params

def phasefunction(f, L, C, R, dR):
    f = f  * np.array(2) * np.pi
    f = np.asarray(f)
    L = float(L)
    R = float(R)
    C = float(C)
    dR = float(dR)
    return np.arctan((L*f-(1/(C*f)))/(R + dR))

def main_activity():
    if Params.clipData:
        processed_data = open("ClippedData.txt")
    else:
        processed_data = open("ProcessedData.txt")
    measured_values = open("MeasuredValues_FS_PHASE.txt", "w")

    phase2_values = []
    phase1_values = []
    freq_values = []
    phase_values = []

    for i, row in enumerate(processed_data):
        burst = row.split()
        freq_values.append(float(burst[0]))
        phase_values.append(float((burst[1])) - float(burst[2]))

    popt, pcov = scipy.optimize.curve_fit(phasefunction, freq_values, phase_values, p0=(0.02, 0.0000022, 0, 300))
    freq_smooth = np.linspace(min(freq_values), max(freq_values), 1000)
    amp_smooth = phasefunction(freq_smooth, *popt)

    Inductivity, Capacity, deltaR, Resistance = popt
    Ind = float(Inductivity)
    Cap = float(Capacity)
    deltaR = float(deltaR)
    Res = float(Resistance)

    # Calculate R-squared
    residuals = phase_values - phasefunction(freq_values, *popt)
    SSE = np.sum(residuals ** 2)
    SST = np.sum((phase_values - np.mean(phase_values)) ** 2)
    R_squared = 1 - (SSE / SST)

    measured_values.write(f"{Params.matName}: L = {Ind}; C = {Cap}; dR = {deltaR}; R = {Res}; R^2 = {R_squared}\n")
    measured_values.close()
