import re
import subprocess
import time
import exceptions as ex

def setSpeedOfFans(fans, speed):
    for fan in fans:
        _setSpeed(fan, speed)

def _setSpeed(fan, speed):
    subprocess.run(["liquidctl", "set", fan, "speed", speed])
    time.sleep(1)


def initializeLiquidctl():
    subprocess.run(["liquidctl", "initialize"])
    time.sleep(10)

def checkIfFansAreConnectedToPort(fans):
    for fan in fans:
        _fanIsConnectedToPort(fan)

def _fanIsConnectedToPort(fan):
    liquidctlStatusFanName = _convertFanNameToLiquidctlStatusName(fan)
    connectedFans = _getAllConnectedFans()
    for i in range(len(connectedFans)):
        if liquidctlStatusFanName in connectedFans[i]:
            return True
    raise ex.FanNotConnectedException(fan + " is not connected to the fan controller")

def _getAllConnectedFans():
    fanRegex = "(Fan\s\d\d?)\s+?DC|PWM"
    liquidctlStatus = _getLiquidctlOutput()
    connectedFans = re.findall(fanRegex, liquidctlStatus)
    return connectedFans

def _getLiquidctlOutput():
    return subprocess.check_output(["liquidctl", "status"]).decode("utf-8").strip()

def _convertFanNameToLiquidctlStatusName(fanName):
    if _getFanNumberFromFanName(fanName) is not None:
        fanStatusName = "Fan " + _getFanNumberFromFanName(fanName)
        return fanStatusName

def _getFanNumberFromFanName(fanName):
    return re.search('\d\d?', fanName)[0]

