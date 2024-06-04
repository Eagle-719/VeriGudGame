import numpy as np
import scipy.optimize
import Params

#CH3 a táp

def fit_sin(tt, yy):
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
    lineCounter = 1
    file_names = open("FileNames.txt")
    for line in file_names:
        current_file = open(line.strip())
        
        freq = float(line.strip("\MeasurementsAluminiumCopperIronEmptySolidSmallBigTest_.csv.txt\n"))
        time = []
        ch2 = []
        ch3 = []
        for row in current_file:
            if lineCounter < 4:
                pass
            elif lineCounter == 4:
                pass
            else:
                burst = row.split(",")

                secTime = float(burst[0])*(1/Params.SampleRate)
                time.append(secTime)
                ch2.append(float(burst[1]))
                ch3.append(float(burst[2]))

        result = fit_sin(time, ch2, freq)
        result_2 = fit_sin(time, ch3, freq)

        amp_m = result["amp"]
        phase_m = result["phase"]
        amp_r = result_2["amp"]
        phase_r = result_2["phase"]

        phase = phase_m - phase_r
        #phase = np.degrees(phase)
        amp = amp_m / amp_r
        processed_data = open("ProcessedData.txt", "a")
        processed_data.write(f"{amp} {phase} {freq}\n")
        processed_data.close()

def stripFile():
    pass