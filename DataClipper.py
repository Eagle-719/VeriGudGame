import Params

def main_activity():
    clipped_data = open("ClippedData.txt", "w")
    clipped_data.write("")
    clipped_data.close()
    i = 0
    clipped_data = open("ClippedData.txt", "a")
    processed_data = open("ProcessedData.txt")
    for row in processed_data:
        burst = row.split()

        amp = float(burst[0])
        phase = float(burst[1])
        freq = float(burst[2])

        if float(burst[2]) <= Params.clipAtFreqMax and float(burst[2]) >= Params.clipAtFreqMin:
            clipped_data.write(f"{amp} {phase} {freq}\n")

    clipped_data.close()
    processed_data.close()