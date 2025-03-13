import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from datetime import datetime as dt 
from datetime import timedelta as td
import traceback
import numpy as np
import csv
import os
import time
import timeit

def dataCollection(fromDateTime: object, toDateTime: object, sensornames: list[str], **kwargs) -> list[list[str,float,...],...]:
    try:
        if kwargs["multicollection"] == True:
            kwargs["multicollection"] = False
            rawdata = dataMultiCollection(fromDateTime, toDateTime, sensornames, **kwargs)
            return rawdata
        now = dt.now()
        defaultSamples = 1_000
        if (fromDateTime-toDateTime).total_seconds() >= 0:
            raise ValueError("Error Occured: Incorrect Time Difference")
            traceback.print_exc()
        defaultStepSize = round((toDateTime-fromDateTime).total_seconds()/defaultSamples)
        defaultSamples = round((toDateTime-fromDateTime).total_seconds()/defaultStepSize)+1
        if defaultSamples > 999999:
            defaultSamples = 999999
        defaultvalues = {"timeStepSize":defaultStepSize, "samples":defaultSamples, "multicollection":False}
        defaultvalues.update(kwargs)
        print("----------Running Data Collection----------\n"+str(fromDateTime)+" --> "+str(toDateTime))
        if defaultvalues['timeStepSize'] == defaultStepSize and defaultvalues['samples'] != defaultSamples:
            defaultvalues['timeStepSize'] = round((toDateTime-fromDateTime).total_seconds()/defaultvalues['samples'])
        elif defaultvalues['timeStepSize'] != defaultStepSize and defaultvalues['samples'] == defaultSamples:
            defaultvalues['samples'] = round((toDateTime-fromDateTime).total_seconds()/defaultvalues['timeStepSize'])+1
        sensorstring = ""
        for sensors in range(len(sensornames)):
            if sensors != 0:
                sensorstring += " "
            sensorstring += sensornames[sensors]
            continue
        #command = "myData -b \""+fromDateTime.strftime("%Y-%m-%d %H:%M:%S")+"\" -e \""+toDateTime.strftime("%Y-%m-%d %H:%M:%S")+"\" -t "+str(defaultvalues["timeStepSize"])+" "+sensorstring+" -i"
        command = "mySampler -b \""+fromDateTime.strftime("%Y-%m-%d %H:%M:%S")+"\" -n"+str(defaultvalues["samples"])+" -s "+str(defaultvalues["timeStepSize"])+" "+sensorstring
        rawdata = os.popen(command).read().split("\n")
        del rawdata[0]
        del rawdata[len(rawdata)-1]
        originaldatapoints = len(rawdata)
        for data in range(0,len(rawdata)):
            rawdata[data] = rawdata[data].split()
            rawdata[data][0] = dt.strptime(rawdata[data][0]+rawdata[data][1], "%Y-%m-%d%H:%M:%S")
            del rawdata[data][1]
            for sensor in range(1,len(rawdata[data])):
                if rawdata[data][sensor] == "<undefined>":
                    continue
                try:
                    rawdata[data][sensor] = float(rawdata[data][sensor])
                except:
                    continue
                continue
            continue
        removeddatapoints = 0
        for data in reversed(range(0,len(rawdata))):
            dataremoval = False
            for sensor in range(1,len(rawdata[data])):
                if type(rawdata[data][sensor]) != type(float()):
                    dataremoval = True
            if dataremoval:
                removeddatapoints += 1
                del rawdata[data]
            continue
        print("Total Number of Datapoints: "+str(originaldatapoints)+"\nRemoved Datapoints: "+str(removeddatapoints))
        deltatime = (dt.now()-now).total_seconds()
        print("Data Collection Took "+str(deltatime)+"s\n----------Ending Data Collection-----------")
        return rawdata
    except:
        print("Error Occured: Within Data Collection\n")
        traceback.print_exc()
        return None
def dataMultiCollection(fromDateTime: object, toDateTime: object, sensornames: list[str], **kwargs) -> list[list[str,float,...],...]:
    try:
        now = dt.now()
        defaultRequestChunkSize = 3600 #Seconds
        defaultRequestChunkResolution = 3600 #Samples Per Chunk
        defaultKwargsValues = {"ChunkSize":defaultRequestChunkSize, "ChunkResolution":defaultRequestChunkResolution}
        defaultKwargsValues.update(kwargs)
        defaultKwargsChunkValues = {"samples": defaultKwargsValues["ChunkResolution"], "multicollection": False}
        print("-------Running Multi Data Collection-------\n"+str(fromDateTime)+" --> "+str(toDateTime))
        chunkTotal = (toDateTime-fromDateTime).total_seconds()/defaultKwargsValues["ChunkSize"]
        for chunk in range(0,round(chunkTotal),1):
            dataCollection(fromDateTime, toDateTime, sensornames, **defaultKwargsChunkValues)
            print("{:4.2f}".format(chunk/chunkTotal*100) + " %")
        deltatime = (dt.now()-now).total_seconds()
        print("Total Data Collection Took "+str(deltatime)+"s\n-------Ending Multi Data Collection--------")
        return None
    except:
        print("Error Occured: Within Multi Data Collection\n")
        traceback.print_exc()
        return None
def dataCSVExport(sensornames: list[str], data: list[list[str,float,...],...]) -> None:
    try:
        print("-------------Running CSV Export------------")
        now = dt.now()
        with open('datacollection.csv', 'w', newline='') as csvfile:
            dataCSV = csv.writer(csvfile, delimiter=',')
            dataCSV.writerow([' ']+list(sensornames))
            flushPeriod = 36255
            flushQuantity = round(len(data)/flushPeriod)
            if flushQuantity > 0:
                for flush in range(0,flushQuantity-1):
                    for dataROW in range(flush*flushPeriod,(flush+1)*flushPeriod):
                        dataCSV.writerow(data[:][dataROW])
                    print(str((flush*flushPeriod)/(len(data))*100.0)+ " %")
                    csvfile.flush()
                for dataROW in range((flushQuantity-1)*flushPeriod,len(data)):
                    dataCSV.writerow(data[:][dataROW])
            else:
                for dataROW in range(0,len(data)):
                    dataCSV.writerow(data[:][dataROW])
            csvfile.flush()
            csvfile.close()
        rows = len(range(0,len(data)))+1
        columns = len(range(0,len(sensornames)))+1
        deltatime = (dt.now()-now).total_seconds()
        print("Rows: "+str(rows)+"\nColumns: "+str(columns)+"\nData Export Took "+str(deltatime)+"s\n-------------Ending CSV Export-------------")
        return None
    except:
        print("Error Occured: Within CSV Export\n")
        traceback.print_exc()
        return None
def main() -> None:
    #CHL2 2024
    fromdate = dt(2023, 7, 1, 0, 0, 0)
    todate = dt(2023, 7, 31, 0, 0, 0)
    sensornames = ("CPI1242", "CTD1242", "CPI1132", "CTD1132", "CSP10T2")
    dataPoints = 100
    #data=
    #dataCollection(fromdate, todate, sensornames, samples=dataPoints)
    dataCollection(fromdate, todate, sensornames, ChunkResolution=dataPoints, multicollection=True)
    #dataCSVExport(sensornames, data)
if __name__ == "__main__":
    print("--------------Starting Program-------------\nContact Info: buhrig@jlab.org")
    try:
        starttime = dt.now()
        main()
        totaltime = (dt.now()-starttime).total_seconds()
        print(f"Total Program Time: {totaltime:.2f}s\n---------------Ending Program--------------")
    except:
        print("Error Occured: On Initial Startup")
        traceback.print_exc()
    quit()