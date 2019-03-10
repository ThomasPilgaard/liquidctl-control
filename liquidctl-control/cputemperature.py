import subprocess
import re

def getMaxCpuTemperature():
    return max(getAllCpuTemperatures())

def getAllCpuTemperatures():
    cpuTemperatures = []
    for temperatureFile in _getCpuSensorFiles():
        rawTemperature = _getCpuTemperatureFromFile(temperatureFile)
        temperatureInt = _convertTemperatureToInt(rawTemperature)
        trimmedTemperature = _temperatureRemoveTrailingZeroes(temperatureInt)
        cpuTemperatures.append(trimmedTemperature)
    return cpuTemperatures

def _getCpuTemperatureFromFile(cpuSensorFile):
    with open(cpuSensorFile, 'r') as fileHandle:
        temperature = fileHandle.readline().strip()
        return temperature

def _convertTemperatureToInt(temperatureString):
    return int(temperatureString)

def _temperatureRemoveTrailingZeroes(temperature):
    return temperature//1000

def _getCpuSensorFiles():
    cpuSensorFiles = []
    allHwmonFiles = subprocess.check_output(["find", "/sys/class/hwmon/hwmon1/"]).decode("utf-8")
    for hwmonFile in allHwmonFiles.split('\n'):
        if _fileIsSensorFile(hwmonFile):
            cpuSensorFiles.append(hwmonFile)
    return cpuSensorFiles

def _fileIsSensorFile(fileName):
    inputFileRegex = "temp\d\d*?_input"
    fileMatch = re.search(inputFileRegex, fileName)
    return fileMatch is not None

