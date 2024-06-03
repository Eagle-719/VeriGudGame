import os
import Params

def main_activity():
    file_names = open("FileNames.txt", "w")

    for file_name in os.listdir(os.path.join("Measurments", Params.subfolder)):
        file_path = os.path.join("Measurments", Params.subfolder, file_name)
        file_names.write(file_path + '\n')
    
    file_names.close()