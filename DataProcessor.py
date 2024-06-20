import numpy as np
import scipy.optimize
import Params

#CH3 a táp

def fit_sin(tt, yy, amp, freq):
    tt = np.array(tt)
    yy = np.array(yy)
    A = amp
    w = float(freq) * 2. * np.pi
    f = float(freq)

    def sinfunc(t, p):
        A = amp
        w = float(freq)*2.*np.pi
        print(amp, w)
        return A * np.sin(w*t + p)

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy)
    p = popt
    #f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p)

    return {"amp": A, "omega": w, "phase": p, "offset": 0., "freq": f, "period": 1./f, "fitfunc": fitfunc(tt)}

def main_activity():
    processed_data = open("ProcessedData.txt", "w")
    processed_data.write("")
    processed_data.close()
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
            if lineCounter > 3:
                burst = row.split(",")
                IndTime = float(burst[0])
                secTime = IndTime*(1/Params.SampleRate)
                time.append(secTime)
                ch2.append(float(burst[1]))
                ch3.append(float(burst[2]))
            lineCounter += 1

        result = fit_sin(time, ch2, amp_ch2, freq)
        result_2 = fit_sin(time, ch3, amp_ch3, freq)
        print(result)
        print(result_2)

        phase_m = result["phase"]
        phase_r = result_2["phase"]
        '''while phase_m < -np.pi/2:
            phase_m = phase_m+np.pi
        while phase_m > np.pi/2:
            phase_m = phase_m-np.pi
        while phase_r < -np.pi/2:
            phase_r = phase_r+np.pi
        while phase_r > np.pi/2:
            phase_r = phase_r-np.pi'''
        phase = phase_m - phase_r
        phase = np.rad2deg(float(phase))
        while phase > 90:
            phase = phase - 180
        while phase < -90:
            phase = phase +180
        print(phase)

        processed_data = open("ProcessedData.txt", "a")
        processed_data.write(f"{freq} {amp} {phase_m} {phase_r}\n")
        processed_data.close()