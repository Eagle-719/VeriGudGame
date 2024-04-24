import os
import Params


def main_activity():
    file_names = open("FileNames.txt", "w")

    for file_name in os.listdir(os.path.join("Alfredmeres", Params.subfolder)):
        file_path = os.path.join("Alfredmeres", Params.subfolder, file_name)
        file_names.write(file_path + '\n')
        Params.dataQuant += 1

    file_names.close()
