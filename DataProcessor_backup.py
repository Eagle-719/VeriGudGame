import numpy as np
import scipy.optimize
import Params
import matplotlib.pyplot as plt

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

    '''if Params.plotSine:
        plot(tt, yy, fitfunc, second, j)'''

    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc(tt)}

def main_activity():
    processed_data = open("ProcessedData.txt", "w")
    processed_data.write("")
    processed_data.close()
    freqs = []
    amps = []
    phases = []
    file_names = open("FileNames.txt")
    for line in file_names:
        current_file = open(line.strip())

        freq_temp = line.split("\\", 2)[2]
        freq = freq_temp.split(".", 1)[0]
        lineCounter = 0
        time = []
        ch2 = []
        ch3 = []
        for row in current_file:
            if lineCounter < 3:
                print(lineCounter)
            if lineCounter == 3:
                amp_string_ch2 = row.split(",", 2)[1]
                amp_string_ch3 = row.split(",", 2)[2]
                amp_string_ch2 = amp_string_ch2.replace("mV", "")
                amp_ch2 = float(amp_string_ch2)/1000
                amp_string_ch3 = amp_string_ch3.replace("V", "")
                amp_ch3 = float(amp_string_ch3)
                amp = amp_ch2/amp_ch3
                print(amp_ch2)
                print(amp_ch3)
                freqs.append(freq)
                amps.append(amp)
            if lineCounter > 3:
                burst = row.split(",")
                IndTime = float(burst[0])
                secTime = IndTime*(1/Params.SampleRate)
                time.append(secTime)
                ch2.append(float(burst[1]))
                ch3.append(float(burst[2]))
            lineCounter += 1

        result = fit_sin(time, ch2)
        result_2 = fit_sin(time, ch3)

        phase_m = result["phase"]
        phase_r = result_2["phase"]
        phase = phase_m - phase_r
        phase = np.rad2deg(float(phase))
        while phase > 90:
            phase = phase - 180
        while phase < -90:
            phase = phase +180
        print(phase)
        phases.append(phase)


        processed_data = open("ProcessedData.txt", "a")
        processed_data.write(f"{freq} {amp} {phase_m} {phase_r} {phase}\n")
        processed_data.close()

    plt.scatter(freqs, amps, color='blue', label='Measured V')
    plt.xticks(freqs)
    plt.scatter(freqs, phases, color='red', label='Phase')
    #plt.scatter({freq}, amps, color='red', label='Fitted V')
    plt.legend()
    plt.xlabel('Freqvency')
    plt.ylabel('y')
    plt.title('Amp and Phase')
    plt.show()

#main_activity()