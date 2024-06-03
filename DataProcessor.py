import numpy as np
import scipy.optimize
import Params

#CH3 a táp

def fit_sin(tt, yy, second, j):
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):
        return A * np.sin(w*t + p) + c

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c

    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc(tt)}

def main_activity():
    processed_data = open("ProcessedData.txt", "w")
    processed_data.write("")
    processed_data.close()
    j = 1
    time = []
    ch1 = []
    ch2 = []
    mat_amp = []
    mat_phase = []
    freqs = []

    file_names = open("FileNames.txt")
    for line in file_names:
        current_file = open(line.strip())
        time = []
        ch1 = []
        ch2 = []

        for row in current_file:
            burst = row.split()

            time.append(float(burst[0]))
            ch1.append(float(burst[1]))
            ch2.append(float(burst[2]))

        second = False
        result = fit_sin(time, ch1, second, j)
        second = True
        result_2 = fit_sin(time, ch2, second, j)
        j += 1

        amp_1 = result["amp"]
        phase_1 = result["phase"]
        amp_2 = result_2["amp"]
        phase_2 = result_2["phase"]
        freq = round(result_2["freq"])

        phase = phase_1 - phase_2
        #phase = np.degrees(phase)
        amp = amp_1 / amp_2
        mat_amp.append(amp)
        mat_phase.append(phase)
        freqs.append(freq)
        processed_data = open("ProcessedData.txt", "a")
        processed_data.write(f"{amp} {phase} {freq}\n")
        processed_data.close()
