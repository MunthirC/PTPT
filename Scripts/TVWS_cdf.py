# TVWS_cdf - Jace O'Connor

import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import TVWS_main_filters


#Functions for the vizualization of a CDF graph using a selected filter.
def cdf_graph(outdir, indir, filter, filters, dateFilter1, dateFilter2):
    datefilter = False
    if dateFilter1 != "" and dateFilter2 != "": datefilter = True
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
        if file.endswith(".csv"):
            if datefilter == True:
                index = 12
                date = ""
                while index < 22:
                    date += file[index]
                    index += 1
            # If a data filter has been inputted, check to see if .csv file is within specified time-frame
            if (datefilter == True and date >= dateFilter1 and date <= dateFilter2) or datefilter == False:
                #CDF for frame length size.
                if filter in ["frame.len", "tcp.len"]:
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
                            if float(i) > 5000.0: continue
                            else: xaxis.append(float(i))
                    plt.xlabel(filter + " (bytes)")

                #CDF for Round Trip Time
                elif "tcp.analysis.ack_rtt" in filter:
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

                #CDF for bytes in flight
                elif "tcp.analysis.bytes_in_flight" in filter:
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

                #CDF for TCP time to live.
                elif "ip.ttl" in filter:
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

                #Gets the TCP time delta CDF graph.
                elif filter in ["frame.time_delta", "tcp.time_delta", "udp.time_delta"]:
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

                #CDF for TCP window size
                elif "tcp.window_size" in filter:
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

                #Generic CDF, gives no unit of measurement.
                else:
                    if filter in TVWS_main_filters.averageFilters:
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

    if filter in TVWS_main_filters.averageFilters and len(xaxis) > 0:
        #Calulates the CDF.
        width = 0.005
        x = np.sort(xaxis)
        y = 0.25 * np.exp((-x ** 2)/8)
        y = y/(np.sum(width * y))
        cdf = np.cumsum(y * width)

        try:
            # Sets up graph and plots the elements found within the CDF.
            plt.rcParams['font.family'] = "serif"
            ax.plot(x, cdf, "o", lw=1)
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