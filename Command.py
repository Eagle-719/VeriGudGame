import DataClipper
import FileLister
import DataProcessor
import Params
import FittingScriptAMP
import FittingScripPHASE

FileLister.main_activity()

DataProcessor.main_activity()

if Params.clipData:
    DataClipper.main_activity()

FittingScriptAMP.main_activity()

FittingScripPHASE.main_activity()