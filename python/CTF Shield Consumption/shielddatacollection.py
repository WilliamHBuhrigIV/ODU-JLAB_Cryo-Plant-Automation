import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from datetime import datetime as dt
#from errno import EEXIST
import traceback
import numpy as np
import csv
import os
from HEPAKforPython.HEPAK import HeCalc as HeCalc
import time
import timeit
#import shutil
#import matplotlib as mpl
def HECalc(temperature: float, pressure: float) -> float:
    density = 0
    with open('HeCalcTPRange.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rawdata = []
        for row in reader:
            rawdata.append(row)
    temperaturevalues = list(rawdata[0].keys())
    del temperaturevalues[0]
    pressurevalues,densityvalues = [[],[]]
    for rows in range(len(rawdata)):
        pressurevalues.append(int(rawdata[rows]["kg/m3"]))
        for items in rawdata[rows].items():
            values = list(rawdata[rows].values())
        del values[0]
        densityvalues.append(values)
        continue
    closestTemperatureValues = []
    for i in range(0,len(temperaturevalues)):
        closestTemperatureValues.append(np.abs(float(temperaturevalues[i])-temperature))
    closestTemperatureValuesbackup = list(closestTemperatureValues)
    minClosestTempValue = [min(closestTemperatureValues),None]
    for i in range(0,len(closestTemperatureValues)):
        if closestTemperatureValues[i] == minClosestTempValue[0]:
            minClosestTempValue[0] = i
            del closestTemperatureValues[i]
            break
        continue
    minClosestTempValue[1] = min(closestTemperatureValues)
    closestTemperatureValues = list(closestTemperatureValuesbackup)
    del closestTemperatureValuesbackup
    for i in range(0,len(closestTemperatureValues)):
        if closestTemperatureValues[i] == minClosestTempValue[1]:
            minClosestTempValue[1] = i
            break
        continue
    closestPressureValues = []
    for i in range(0,len(pressurevalues)):
        closestPressureValues.append(np.abs(float(pressurevalues[i])-pressure))
    closestPressureValuesbackup = list(closestPressureValues)
    minClosestPressureValue = [min(closestPressureValues),None]
    for i in range(0,len(closestPressureValues)):
        if closestPressureValues[i] == minClosestPressureValue[0]:
            minClosestPressureValue[0] = i
            del closestPressureValues[i]
            break
        continue
    minClosestPressureValue[1] = min(closestPressureValues)
    closestPressureValues = list(closestPressureValuesbackup)
    del closestPressureValuesbackup
    for i in range(0,len(closestPressureValues)):
        if closestPressureValues[i] == minClosestPressureValue[1]:
            minClosestPressureValue[1] = i
            break
        continue
    for i in range(len(densityvalues)):
        for j in range(len(densityvalues[i])):
            densityvalues[i][j] = float(densityvalues[i][j])
    if minClosestPressureValue[0] == minClosestPressureValue[1]:
        minClosestPressureValue[1] += 1
    if minClosestTempValue[0] == minClosestTempValue[1]:
        minClosestTempValue[1] += 1
    intermediatepressurevalue1 = densityvalues[minClosestPressureValue[0]][minClosestTempValue[0]]-((pressurevalues[minClosestPressureValue[0]]-pressure)*(densityvalues[minClosestPressureValue[0]][minClosestTempValue[0]]-densityvalues[minClosestPressureValue[1]][minClosestTempValue[0]])/(pressurevalues[minClosestPressureValue[0]]-pressurevalues[minClosestPressureValue[1]]))
    intermediatepressurevalue2 = densityvalues[minClosestPressureValue[0]][minClosestTempValue[1]]-((pressurevalues[minClosestPressureValue[0]]-pressure)*(densityvalues[minClosestPressureValue[0]][minClosestTempValue[1]]-densityvalues[minClosestPressureValue[1]][minClosestTempValue[1]])/(pressurevalues[minClosestPressureValue[0]]-pressurevalues[minClosestPressureValue[1]]))
    intermediatevalue = intermediatepressurevalue1-((float(temperaturevalues[minClosestTempValue[0]])-temperature)*(intermediatepressurevalue1-intermediatepressurevalue2)/(float(temperaturevalues[minClosestTempValue[0]])-float(temperaturevalues[minClosestTempValue[1]])))
    return intermediatevalue
def temperatureFunction(x):
    return (x-2500)/15
def massflowFunction(x):
    return (x-7000)/200
def linePlot(xy: list[list[float,...],list[float,...]], *args: list[list[float,...],list[float,...]], **kwargs) -> None:
    defaultvalues = {
        "label": None,
        "xlabel": None,
        "ylabel": None,
        "title": None,
        "figuresize": (4,3),
        "xlim": "auto",
        "ylim": "auto",
        "layout": "constrained",
        "yscale": "linear",
        "xscale": "linear",
        "color": None,
        "figax": None,
        "secondaryaxis": None,
        "y2label": None,
        "secondaryaxisfunction": None,
        "secondaryaxislocation": None,
        "secondaryaxisminorticklocator": None
    }
    defaultvalues.update(kwargs)
    if defaultvalues["figax"] == None:
        fig, ax = plt.subplots(figsize=defaultvalues["figuresize"],layout=defaultvalues["layout"])
    else:
        fig, ax = [defaultvalues["figax"][0],defaultvalues["figax"][1]]
    if defaultvalues["secondaryaxis"] != None:
        if defaultvalues["secondaryaxis"] == True:
            if defaultvalues["secondaryaxislocation"] != None:
                secax = ax.secondary_yaxis(defaultvalues["secondaryaxislocation"],functions=(defaultvalues["secondaryaxisfunction"],defaultvalues["secondaryaxisfunction"]))
            else:
                secax = ax.secondary_yaxis('right',functions=(defaultvalues["secondaryaxisfunction"],defaultvalues["secondaryaxisfunction"]))
            if defaultvalues["secondaryaxisminorticklocator"] != None:
                secax.yaxis.set_minor_locator(MultipleLocator(defaultvalues["secondaryaxisminorticklocator"]))
                secax.grid(visible=True,which="minor",linestyle='--',color="green")
                secax.set_axisbelow(True)
        else:
            secax = defaultvalues["secondaryaxis"]
        if defaultvalues["y2label"] != None:
            secax.set_ylabel(defaultvalues["y2label"])
    ax.set_xscale(defaultvalues["xscale"])
    ax.set_yscale(defaultvalues["yscale"])
    if defaultvalues["color"] == None:
        if defaultvalues["label"] != None:
            ax.plot(xy[0],xy[1], label=defaultvalues["label"])
        else:
            ax.plot(xy[0],xy[1])
        for line in range(0,len(args)):
            ax.plot(args[line][0],args[line][1])
            continue
    else:
        if defaultvalues["label"] != None:
            ax.plot(xy[0],xy[1],color=defaultvalues["color"],label=defaultvalues["label"])
            for line in range(0,len(args)):
                ax.plot(args[line][0],args[line][1],color=defaultvalues["color"][line+1])
                continue
        else:
            ax.plot(xy[0],xy[1],color=defaultvalues["color"])
    if defaultvalues["xlim"] == "auto":
        ax.set_xlim(auto=True)
    else:
        ax.set_xlim(defaultvalues["xlim"])
    if defaultvalues["ylim"] == "auto":
        ax.set_ylim(auto=True)
    else:
        ax.set_ylim(defaultvalues["ylim"])
    if defaultvalues["xlabel"] != None:
        ax.set_xlabel(defaultvalues["xlabel"])
    if defaultvalues["ylabel"] != None:
        ax.set_ylabel(defaultvalues["ylabel"])
    if defaultvalues["title"] != None:
        ax.set_title(defaultvalues["title"])
    ax.yaxis.set_major_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(250))
    ax.grid(visible=True,axis='both',which="major",linestyle='-.',color="dimgrey")
    ax.grid(visible=True,axis='y',which="minor",linestyle='--',color="dimgrey")
    return fig, ax
def rateEnergyCalculation(data: list[list[str,float,...],...], *args) -> float:
    #deltas = deltaDataCalculation(data[0], data[1])
    #rates p[],[]]
    print('--------Starting Energy Calculation--------')
    if args != ():
        massflowdata = args[0]
    q, deltatime = [[],[]]
    for datapoint in range(0,len(data)-1):
        deltatime.append((data[datapoint+1][0]-data[datapoint][0]).total_seconds())
        continue
    for datapoints in range(0,len(data)):
        Cp = 5200
        if args != ():
            q.append(Cp*float(massflowdata[datapoints])/1000*(data[datapoints][2]-data[datapoints][1]))
        else:
            q.append(Cp*data[datapoints][3]/1000*(data[datapoints][2]-data[datapoints][1]))
        continue
    q_full = list(q)
    for datapoint in range(0,len(data)-1):
        q[datapoint] = (q[datapoint+1]+q[datapoint])/2
        continue
    del q[len(data)-1]
    q_total=0
    for datapoint in range(0,len(data)-1):
        q_total += q[datapoint]*deltatime[datapoint]
        continue
    print(f'Energy Consumed: {q_total/1e6:.5f} Mega-Joule\n---------Ending Energy Calculation---------')
    return q, q_total, q_full
def massflowCalculation(data: list[list[str,float,...],...]) -> list[float]:
    print('-------Starting Massflow Calculation-------')
    ptcalc = HeCalc(3, 1, 2)
    bore = 3*0.0254
    stroke = 2*0.0254
    volume = np.pi*np.power(bore,2)/4*stroke
    rpmvalues, temperature_input, pressure_input = [[],[],[]]
    for datapoints in range(0,len(data)):
        rpmvalues.append(float(data[datapoints][8]))
        temperature_input.append(float(data[datapoints][4]))
        pressure_input.append(float(data[datapoints][6]))
        continue
    massflow = []
    for i in range(len(rpmvalues)):
        #massflow.append(HECalc(temperature_input[i], pressure_input[i]*100000)*2*volume*rpmvalues[i]/60)
        massflow.append(ptcalc.run(pressure_input[i]*100000, temperature_input[i])*2*volume*rpmvalues[i]/60)
    print(f'Mean Gasflow: {np.mean(massflow)*1000:.5f} g/m3')
    print('--------Ending Massflow Calculation-------')
    return massflow
def dataCollection(fromDateTime: object, toDateTime: object, sensornames: list[str], **kwargs) -> list[list[str,float,...],...]:
    print("----------Running Data Collection----------\n"+str(fromDateTime)+" --> "+str(toDateTime))
    now = dt.now()
    defaultvalues = {"timeStepSize":1}
    defaultvalues.update(kwargs)
    sensorstring = ""
    for sensors in range(len(sensornames)):
        if sensors != 0:
            sensorstring += ", "
        sensorstring += sensornames[sensors]
        continue
    command = "myData -b \""+fromDateTime.strftime("%Y-%m-%d %H:%M:%S")+"\" -e \""+toDateTime.strftime("%Y-%m-%d %H:%M:%S")+"\" -t "+str(defaultvalues["timeStepSize"])+" "+sensorstring+" -i"
    #print(command)
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
def main() -> None:
    fromdate = dt(2023, 1, 20, 16, 15, 0)
    todate = dt(2023, 1, 24, 0, 0, 0)
    sensornames = ["CTP2420","CTP2421","CFI2400","CTD2413R","CTD2414R","CPI2415R","CPI2416R","CSP241R_M"]
    try:
        
        data=dataCollection(fromdate, todate, sensornames, timeStepSize=60*10)
        q, q_total, q_full = rateEnergyCalculation(data)
        mass_flow_rpm = massflowCalculation(data)
        for i in range(len(mass_flow_rpm)):
            mass_flow_rpm[i]=mass_flow_rpm[i]*1000
        q_rpm, q_total_rpm, q_full_rpm = rateEnergyCalculation(data,mass_flow_rpm)
        for i in range(len(mass_flow_rpm)):
            mass_flow_rpm[i]=mass_flow_rpm[i]*200+7000
        times, heat_flux_meter,temp_in, temp_out, mass_flow_meter  = [[],[],[],[],[]]
        heat_flux_meter = q_full
        heat_flux_rpm = q_full_rpm
        for item in data:
            temp_in.append(item[2]*15+2500)
            temp_out.append(item[1]*15+2500)
            mass_flow_meter.append(item[3]*200+7000)
            times.append((item[0]-fromdate).total_seconds())
            continue
        print('-------------Starting Plotting-------------\nPlotting Heat Flux, Temperature, and Massf-\nlow on seperate axes.')
        fig, ax = linePlot((times,heat_flux_meter),label="Heat Flux Meter [Calculated]",color="mediumorchid", xlabel="Time (Second)", ylabel="Shield Heat Generation (Watt)", title="Energy Consumption Rate", figuresize=(12,8))
        linePlot((times,heat_flux_rpm),figax=(fig,ax),label="Heat Flux RPM [Calculated]",color="orangered")
        linePlot((times,temp_in),figax=(fig,ax),label="Inlet Temperature [CTP2420]",color="mediumslateblue",y2label="Temperature (Kelvin)",secondaryaxis=True,secondaryaxisfunction=temperatureFunction, secondaryaxisminorticklocator=20)
        linePlot((times,temp_out),figax=(fig,ax),label="Outlet Temperature [CTP2421]",color="firebrick")
        linePlot((times,mass_flow_meter),figax=(fig,ax),label="Massflow Meter [CFI2400]",color="forestgreen",y2label="Mass Flow (g/s)",secondaryaxis=True,secondaryaxisfunction=massflowFunction, secondaryaxislocation=1.1, secondaryaxisminorticklocator=1)
        linePlot((times,mass_flow_rpm),figax=(fig,ax),label="Massflow RPM [Calculated]",color="darkolivegreen")
        ax.set_facecolor(color="black")
        plt.legend(loc="upper left")
        print('--------------Ending Plotting--------------')
        #print(np.mean(q))
    except:
        print("Error Occured: Within Data Collection\n")
        traceback.print_exc()
        return
    return
if __name__ == "__main__":
    print("--------------Starting Program-------------\nContact Info: buhrig@jlab.org")
    try:
        #calc = HeCalc(3, 'P', 'T')
        #print(calc.run(1, 1))
        starttime = dt.now()
        start = time.process_time()
        main()
        end = time.process_time()
        totaltime = (dt.now()-starttime).total_seconds()
        print(f"Data Processing Took: {end-start:.2f}s\nTotal Program Time: {totaltime:.2f}s\n---------------Ending Program--------------")
        plt.show()
    except:
        print("Error Occured: On Initial Startup")
        traceback.print_exc()
    quit()