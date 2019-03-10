#!/usr/bin/env python3

import subprocess
import traceback
import time
import sys
import signal
import collections as col
import statistics as stat
import cputemperature as cputemp
import liquidctl as liq
import exceptions as ex
import gracefulkiller

circularBufSize = 3
frontFans = ["fan1", "fan2", "fan3"]
backFans = ["fan4"]
topFans = []

evenTemps = col.deque(maxlen=circularBufSize)


def main():
    killer = gracefulkiller.GraceFulKiller()
    try:
        currentFanSpeed = "-1"
        fansToControl = getFansToControl()

        liq.initializeLiquidctl()
        liq.checkIfFansAreConnectedToPort(fansToControl)

        initializeCircularTempBuffer()

        while True:
            maxTemp = cputemp.getMaxCpuTemperature()
            evenTemps.appendleft(maxTemp)
            tempMedian = stat.median(evenTemps)

            fanSpeed = calculateFanSpeedFromCpuTemperature(tempMedian)

            if currentFanSpeed != fanSpeed:
                liq.setSpeedOfFans(fansToControl, fanSpeed)

                print("--------------------------------------")
                print(evenTemps)
                print("Median: " + str(tempMedian))
                print("setting speed to " + fanSpeed)
                sys.stdout.flush()

                currentFanSpeed = fanSpeed

            if killer.kill_now:
                break

            time.sleep(2)

    finally:
        errorHandling(traceback.format_exc())

def initializeCircularTempBuffer():
    for i in range(circularBufSize):
        evenTemps.append(40)

def calculateFanSpeedFromCpuTemperature(temp):
    if temp > 75:
        return "100"
    if temp > 70:
        return "90"
    if temp > 65:
        return "80"
    if temp > 60:
        return "60"
    if temp > 55:
        return "50"
    if temp > 50:
        return "40"
    if temp > 0:
        return "0"

def getFansToControl():
    return frontFans + backFans + topFans

def errorHandling(errorMsg):
    allFans = getFansToControl()
    liq.setSpeedOfFans(allFans, "100")
    print("Gracefully terminating")


if __name__ == "__main__":
    main()

