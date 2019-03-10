import subprocess
import glob

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
    return glob.glob("/sys/class/hwmon/hwmon1/*_input")

