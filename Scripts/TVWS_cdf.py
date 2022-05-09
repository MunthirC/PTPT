# TVWS_cdf - Jace O'Connor

import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import TVWS_main_filters


#Functions for the vizualization of a CDF graph using a selected filter.
def cdf_graph(outdir, indir, filter, filters, dateFilter1, dateFilter2, weatherFilter):
    datefilter, weatherFilt = False, False
    if dateFilter1 != "" and dateFilter2 != "": datefilter = True
    if len(weatherFilter) != 0: weatherFilt = True
    #Gets the index of the filter.
    tempIndex = int(filters.index(filter))
    #Create the figure.
    fig, ax = plt.subplots()
    #Initialize axis
    xaxis = []
    yaxis = []

    #Go through directory.
    for file in os.listdir(indir):
        #Locate .csv files
        if file.endswith(".csv") and file != "TimestampsDuctingAndIcePeriod.csv":
            # Obtain date from file name
            if datefilter == True:
                try:
                    index = 12
                    date = ""
                    while index < 22:
                        date += file[index]
                        index += 1
                except Exception as err:
                    print("Unable to obtain date from file name: '", file, "'. Error: ", err)
                    continue
            # If a date filter has been inputted, check to see if .csv file is within specified time-frame
            if (datefilter == True and date >= dateFilter1 and date <= dateFilter2) or datefilter == False:
                # If a weather filter has been inputted, check to see if .csv file met condition and is in dictionary
                if (weatherFilt is True and file in weatherFilter) or weatherFilt is False:
                    #CDF for frame length size.
                    if filter in ["frame.len", "tcp.len"]:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                     "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                     os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                elif len(xaxis) == 100000000: break
                                else:
                                    if float(i) > 5000.0: continue
                                    else: xaxis.append(float(i))
                            if len(xaxis) == 100000000: break
                            plt.xlabel(filter + " (bytes)")
                        except Exception as e: continue

                    #CDF for Round Trip Time
                    elif "tcp.analysis.ack_rtt" in filter:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                     "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                     os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                else:
                                    if float(i) > 10: continue
                                    else: xaxis.append(float(i))
                            plt.xlabel("TCP Round Trip Time (seconds)")
                        except Exception as e: continue

                    #CDF for bytes in flight
                    elif "tcp.analysis.bytes_in_flight" in filter:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                     "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+ os.path.join(indir, file),
                                                     shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                else:
                                    if float(i) > 5000.0: continue
                                    else: xaxis.append(float(i))
                            plt.xlabel("Bytes in Flight (bytes)")
                        except Exception as e: continue

                    #CDF for TCP time to live.
                    elif "ip.ttl" in filter:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                     "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                     os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                else:
                                    if float(i) > 100: continue
                                    else: xaxis.append(float(i))
                            plt.xlabel("Time to Live (seconds)")
                        except Exception as e: continue

                    #Gets the TCP time delta CDF graph.
                    elif filter in ["frame.time_delta", "tcp.time_delta", "udp.time_delta"]:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                     "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                     os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                else:
                                    if float(i) > 15: continue
                                    else: xaxis.append(float(i))
                            plt.xlabel("Time Delta: " + filter + " (seconds)")
                        except Exception as e: continue

                    #CDF for TCP window size
                    elif "tcp.window_size" in filter:
                        try:
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+
                                                     str(tempIndex+1)+"!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                     os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2: continue
                                elif i == ' ': continue
                                else:
                                    if float(i) > 5000.0: continue
                                    else: xaxis.append(float(i))
                            plt.xlabel("TCP Window Length (bytes)")
                        except Exception as e: continue

                    #Generic CDF, gives no unit of measurement.
                    else:
                        if filter in TVWS_main_filters.averageFilters:
                            try:
                                #Gets the values of each value for first field that is not empty.
                                proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$"+str(tempIndex+1)+"}($"+str(tempIndex+1)+
                                                         "!=\\\"\\\"){print $"+str(tempIndex+1)+"}\" "+
                                                         os.path.join(indir, file), shell=True, stdout=subprocess.PIPE)
                                temp1 = str(proc2.communicate()[0].decode('ascii'))
                                temp2 = temp1.splitlines()
                                for i in temp2:
                                    if len(i) < 2: continue
                                    elif i == ' ': continue
                                    else: xaxis.append(float(i))
                                plt.xlabel(filter)
                            except Exception as e: continue

    if filter in TVWS_main_filters.averageFilters and len(xaxis) > 0:
        #Calulates the CDF.
        width = 0.005
        x = np.sort(xaxis)
        y = 0.25 * np.exp((-x ** 2)/8)
        y = y/(np.sum(width * y))
        cdf = np.cumsum(y * width)

        #Condenses the data into graphable data points.
        if "frame" in filter:
            xaxis2 = []
            cdf2 = []
            tempI = 0
            for i in x:
                if i not in xaxis2:
                    xaxis2.append(i)
                    tempCDF = cdf[tempI]
                    cdf2.append(tempCDF)
                    tempI = tempI+1
                elif i in xaxis2:
                    if cdf[tempI] >= 1: continue
                    else:
                        tempCDFIndex = xaxis2.index(i)
                        cdf2[tempCDFIndex] = cdf[tempI]
                        tempI = tempI+1
                else: continue

        try:
            # Sets up graph and plots the elements found within the CDF.
            plt.rcParams['font.family'] = "serif"
            if "frame" in filter: ax.plot(xaxis2, cdf2, "o", lw=1)
            else: ax.plot(x, cdf, "o", lw=1)
            loc = plticker.MultipleLocator(base=.1)
            ax.yaxis.set_major_locator(loc)
            ax.set_axisbelow(True)
            ax.yaxis.grid(True, color='#EEEEEE')
            ax.xaxis.grid(False)
            #Sets the label of the y axis.
            plt.ylabel("CDF")
            #Set the title.
            plt.title("CDF Graph: " + filter)
            # Saves and shows the plotted CDF Graph.
            if outdir is not None: plt.savefig(outdir + "\\" + filter + 'xCDF.png', bbox_inches='tight')
            plt.show()
        except Exception as e: print("Unable to graph: ", e)
    else: print(filter + " could not be plotted against a CDF. ")