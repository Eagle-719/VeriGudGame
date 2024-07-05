import Params
import matplotlib.pyplot as plt

#CH3 a táp

def main_activity():
    processed_data = open(Params.ResultsPath, "w")
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
                pass
            if lineCounter == 3:
                amp_string_ch2 = row.split(",", 2)[1]
                amp_string_ch3 = row.split(",", 2)[2]
                if '?' in amp_string_ch2:
                    amp_string_ch2 = amp_string_ch2.replace(" ?", "")
                if 'm' in amp_string_ch2:
                    amp_string_ch2 = amp_string_ch2.replace("mV", "")
                    amp_ch2 = float(amp_string_ch2) / 1000
                else:
                    amp_string_ch2 = amp_string_ch2.replace("V", "")
                    amp_ch2 = float(amp_string_ch2)
                if '?' in amp_string_ch2:
                    amp_string_ch2 = amp_string_ch2.replace(" ?", "")
                print(amp_string_ch2)
                amp_string_ch3 = amp_string_ch3.replace("V", "")
                amp_ch3 = float(amp_string_ch3)
                amp = amp_ch2/amp_ch3
                print(amp_ch2)
                freqs.append(freq)
                amps.append(amp)
            if lineCounter > 3:
                burst = row.split(",")
                ch2.append(float(burst[1]))
                ch3.append(float(burst[2]))
            lineCounter += 1

        processed_data = open(Params.ResultsPath, "a")
        processed_data.write(f"{freq} {amp}\n")
        processed_data.close()

    plt.scatter(freqs, amps, color='blue', label='Measured V')
    plt.xticks(freqs)
    plt.legend()
    plt.xlabel('Freqvency')
    plt.ylabel('Um/Ur')
    plt.title('Amp')
    plt.show()
