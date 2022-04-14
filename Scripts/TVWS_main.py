#!/usr/bin/env python3

# TVWS_main - Munthir Chater

import os
import TVWS_main_filters
import TVWS_process
import TVWS_tools1
import TVWS_cdf
import TVWS_bargraph
import TVWS_tablegraph

# GLOBALS
# Global dictionaries for count, total, and average values. Values are stored here to prevent re-calculating and save time
countCalcs, totalCalcs, avgCalcs = {}, {}, {}
# Global specification values that are inputted by user to run program
InputDirectory, OutputDirectory = None, None
graph = None
dateFilter1, dateFilter2 = "", ""
displayFilter = ""
fieldFilter = []
index, index2 = 0, 0


# Function to set or update path of current working directory
def set_directory(command, path):
    global InputDirectory
    global OutputDirectory
    loop = True

    while loop:
        if path == "exit": loop = False
        elif os.path.isdir(path):
            if command == "indir": InputDirectory = path
            else: OutputDirectory = path
            print("Directory path set. ")
            loop = False
        else: path = input("Directory does not exist, re-renter path: ")


# Function to set or update fields to be filtered when processing .pcap files
def set_filters(filterList):
    global fieldFilter
    fieldCount = 0

    if filterList[0] == "clear":
        fieldFilter.clear()
        print("Field filters removed. ")
    else:
        fieldFilter.clear()
        for field in filterList:
            if field != "filter" and field != "field":
                if field in TVWS_main_filters.fieldFilters:
                    fieldFilter.append(field)
                    fieldCount += 1
                else: print("Field: ", field, " not a valid field, or not supported.")
        print(fieldCount, " field(s) added to filter. ")


# Function to set or update display filters to be used when processing .pcap files
def set_displayFilter(disfilter):
    global displayFilter

    if disfilter == "clear":
        displayFilter = ""
        print("Display filter removed. ")
    else:
        displayFilter = ""
        if disfilter in TVWS_main_filters.displayFilters:
            displayFilter = displayFilter + disfilter
            print("Display filter added. ")
        else: print("Field: ", disfilter, " not a valid field, or not supported.")


# Function to set date filter to be used when processing .pcap files
def set_dateFilter(datefilter):
    global dateFilter1
    global dateFilter2
    index = 0
    date1 = True
    year1, year2, month1, month2, day1, day2, hour1, hour2 = "", "", "", "", "", "", "", ""

    if datefilter == "clear":
        check = input("Are you sure? This will reset saved calculations. ")
        if check.lower() == "yes":
            dateFilter1 = ""
            dateFilter2 = ""
            countCalcs.clear()
            totalCalcs.clear()
            avgCalcs.clear()
            print("Date filter removed. ")
    else:
        for char in datefilter:
            if char == "-" and date1 == True: date1 = False
            elif index <= 3 and date1 == True: year1 += char
            elif index >= 4 and index <= 5 and date1 == True: month1 += char
            elif index >= 6 and index <= 7 and date1 == True: day1 += char
            elif index >= 8 and index <= 9 and date1 == True: hour1 += char
            elif index >= 11 and index <= 14 and date1 == False: year2 += char
            elif index >= 15 and index <= 16 and date1 == False: month2 += char
            elif index >= 17 and index <= 18 and date1 == False: day2 += char
            elif index >= 19 and index <= 20 and date1 == False: hour2 += char
            index += 1

        validDates = True
        try:
            if (int(year1) < 2000 or int(year1) > 2022) or (int(year2) < 2000 or int(year2) > 2022): validDates = False
            if (int(month1) < 1 or int(month1) > 12) or (int(month2) < 1 or int(month2) > 12): validDates = False
            if (int(day1) < 1 or int(day1) > 31) or (int(day2) < 1 or int(day2) > 31): validDates = False
            if (int(hour1) < 0 or int(hour1) > 23) or (int(hour2) < 0 or int(hour2) > 23): validDates = False

            if validDates == True:
                check = input("Are you sure? This will reset saved calculations. ")
                if check.lower() == "yes":
                    dateFilter1 = year1 + month1 + day1 + hour1
                    dateFilter2 = year2 + month2 + day2 + hour2
                    countCalcs.clear()
                    totalCalcs.clear()
                    avgCalcs.clear()
                    print("Date filter added. ")
            else: print("Invalid date input. ")
        except: print("Invalid date input.")


# Function to set graph type for data visualization
def set_graph():
    global graph
    loop2 = True

    while loop2:
        choice = input("Select graph type: ")
        if choice == "exit":
            loop2 = False
        elif choice == "info":
            print("Process Info: " +
                  "\nInput: " +
                  "\n- 'plot' : Set graph to plot" +
                  "\n- 'scatter' : Set graph to scatter" +
                  "\n- 'bar' : Set graph to bar")
        elif choice == "plot" or choice == "scatter" or choice == "bar":
            graph = choice
            print("Graph set.")
        else: print("Invalid entry, re-renter. ")


# Function for settings menu
def settings():
    loop = True

    while loop:
        choice = input("Settings: ")
        choiceList = choice.split()
        if len(choiceList) != 0:
            if choiceList[0] == "info":
                print("Settings Info: " +
                      "\nInput: " +
                      "\n- 'clear' <input>: Clear previous filter input (field, display, date)" +
                      "\n- '<type>dir' <path>: Enter input and output directory paths" +
                      "\n- 'filter' <filter type> <filter value>: Filter .pcap files from specified directory" +
                      "\n- 'graph' <graph type>: Enter fields to be present in graph and type of graph")

            elif choiceList[0] == "clear":
                if len(choiceList) > 1:
                    if choiceList[1] == "field": set_filters(choiceList)
                    elif choiceList[1] == "display": set_displayFilter(choiceList[0])
                    elif choiceList[1] == "date": set_dateFilter(choiceList[0])
                    else: print("Invalid input. ")
                else: print("Need additional argument - input to clear. ")

            elif choiceList[0] == "indir" or choiceList[0] == "outdir":
                if len(choiceList) > 1: set_directory(choiceList[0], choiceList[1])
                else: print("Need additional argument - directory path. ")

            elif choiceList[0] == "filter":
                if len(choiceList) >= 3 and choiceList[1] == "field": set_filters(choiceList)
                elif len(choiceList) == 3 and choiceList[1] == "display": set_displayFilter(choiceList[2])
                elif len(choiceList) == 3 and choiceList[1] == "date": set_dateFilter(choiceList[2])
                else: print("Invalid filter command. Enter in the form: 'filter <filter type> <filter value>' ")

            elif choiceList[0] == "graph": set_graph()

            elif choiceList[0] == "exit": loop = False

            else: print("Invalid command, re-enter. ")
        else: print("Enter a command. ")


# Function for tools menu
def tools():
    global graph, index, index2
    loop = True

    while loop:
        repeat = False
        choice = input("Tools: ")
        choiceList = choice.split()
        codeOrService = ""
        if choiceList[0] == "rep": repeat = True

        if len(choiceList) == 2 and repeat != True:
            tool = choiceList[0]
            func = choiceList[1]
        if len(choiceList) == 3 and repeat != True:
            tool = choiceList[0]
            func = choiceList[1]
            filt = choiceList[2]
        elif len(choiceList) == 4 and repeat == True:
            tool = choiceList[1]
            func = choiceList[2]
            filt = choiceList[3]
        elif len(choiceList) == 4 and repeat != True:
            tool = choiceList[0]
            func = choiceList[1]
            filt = choiceList[2]
            codeOrService = choiceList[3]
            if codeOrService not in TVWS_main_filters.websiteList and codeOrService not in TVWS_main_filters.codeList and\
                    codeOrService not in TVWS_main_filters.services:
                print("Invalid website, code, or service input. ")
                continue
            if filt == "http.response.code":
                if codeOrService not in TVWS_main_filters.codeList:
                    print("Invalid code entry. ")
                    continue
            elif filt in TVWS_main_filters.servicesFields:
                if codeOrService not in TVWS_main_filters.services:
                    print("Invalid service entry. ")
                    continue
                else: codeOrService = TVWS_main_filters.services[codeOrService]
            elif filt in TVWS_main_filters.siteFilters:
                if codeOrService not in TVWS_main_filters.websiteList:
                    print("Invalid website entry. ")
                    continue
        elif len(choiceList) == 5 and repeat == True:
            tool = choiceList[1]
            func = choiceList[2]
            filt = choiceList[3]
            codeOrService = choiceList[4]
            if codeOrService not in TVWS_main_filters.websiteList and codeOrService not in TVWS_main_filters.codeList and \
                    codeOrService not in TVWS_main_filters.services:
                print("Invalid website, code, or service input. ")
                continue
            if filt == "http.response.code":
                if codeOrService not in TVWS_main_filters.codeList:
                    print("Invalid code entry. ")
                    continue
            elif filt in TVWS_main_filters.servicesFields:
                if codeOrService not in TVWS_main_filters.services:
                    print("Invalid service entry. ")
                    continue
                else: codeOrService = TVWS_main_filters.services[codeOrService]
            elif filt in TVWS_main_filters.siteFilters:
                if codeOrService not in TVWS_main_filters.websiteList:
                    print("Invalid website entry. ")
                    continue

        compatibleFunc = False
        if choice == "exit": loop = False

        elif choice == "info":
            print("Settings Info: " +
                  "\nInput: " +
                  "\n- 'calc' <function type> <field> <code/service/site (if necessary)> : Perform calculation on data" +
                  "\n- 'graph' <graph_type> <field> : Output type visualization of data" +
                  "\n- 'exit' : Exit tools")

        elif (len(choiceList) == 2) and tool == "graph" and func in ["table", "bar"]:
            if func == "table":
                TVWS_tablegraph.tableGraph(OutputDirectory, InputDirectory, fieldFilter, "", index2, avgCalcs,
                                           totalCalcs, countCalcs, dateFilter1, dateFilter2)
                index2 += 1
            else:
                TVWS_bargraph.barGraph(OutputDirectory, InputDirectory, fieldFilter, "", index, avgCalcs, totalCalcs,
                                         countCalcs, dateFilter1, dateFilter2)
                index += 1

        elif (len(choiceList) >= 3 and len(choiceList) <= 5) and tool == "calc":
            if func == "count" or func == "total" or func == "avg":
                if func == "count":
                    if filt in TVWS_main_filters.countFilters: compatibleFunc = True
                elif func == "total":
                    if filt in TVWS_main_filters.totalFilters: compatibleFunc = True
                elif func == "avg":
                    if filt in TVWS_main_filters.averageFilters: compatibleFunc = True
                if compatibleFunc == True:
                    if filt in TVWS_main_filters.fieldFilters or \
                            (filt == "cpkt" and "tcp.analysis.retransmission" in TVWS_main_filters.fieldFilters and
                             "tcp.flags" in TVWS_main_filters.fieldFilters and "tcp.len" in TVWS_main_filters.fieldFilters) \
                            or filt in TVWS_main_filters.tcpflowFilters or filt in TVWS_main_filters.udpflowFilters:

                        if func == "count":
                            if filt in countCalcs and repeat == False: print(countCalcs[filt])
                            else:
                                if filt in TVWS_main_filters.tcpflowFilters: count = \
                                    TVWS_tools1.calc("count", filt, fieldFilter, codeOrService, InputDirectory, 1, dateFilter1, dateFilter2)
                                elif filt in TVWS_main_filters.udpflowFilters: count = \
                                    TVWS_tools1.calc("count", filt, fieldFilter, codeOrService, InputDirectory, 2, dateFilter1, dateFilter2)
                                else: count = \
                                    TVWS_tools1.calc("count", filt, fieldFilter, codeOrService, InputDirectory, 0, dateFilter1, dateFilter2)
                                countCalcs[filt] = count
                                print("COUNT: ", count)

                        elif func == "total":
                            if filt in totalCalcs and repeat == False: print(totalCalcs[filt])
                            else:
                                if filt in TVWS_main_filters.tcpflowFilters: total = \
                                    TVWS_tools1.calc("total", filt, fieldFilter, codeOrService, InputDirectory, 1, dateFilter1, dateFilter2)
                                elif filt in TVWS_main_filters.udpflowFilters: total = \
                                    TVWS_tools1.calc("total", filt, fieldFilter, codeOrService, InputDirectory, 2, dateFilter1, dateFilter2)
                                else: total = \
                                    TVWS_tools1.calc("total", filt, fieldFilter, codeOrService, InputDirectory, 0, dateFilter1, dateFilter2)
                                totalCalcs[filt] = total
                                print("TOTAL: ", total)

                        elif func == "avg":
                            if filt in avgCalcs and repeat == False: print(avgCalcs[filt])
                            else:
                                if filt in TVWS_main_filters.tcpflowFilters: avg = \
                                    TVWS_tools1.calc("avg", filt, fieldFilter, codeOrService, InputDirectory, 1, dateFilter1, dateFilter2)
                                elif filt in TVWS_main_filters.udpflowFilters: avg = \
                                    TVWS_tools1.calc("avg", filt, fieldFilter, codeOrService, InputDirectory, 2, dateFilter1, dateFilter2)
                                else: avg = \
                                    TVWS_tools1.calc("avg", filt, fieldFilter, codeOrService, InputDirectory, 0, dateFilter1, dateFilter2)
                                avgCalcs[filt] = avg
                                print("AVERAGE: ", avg)

                    else: print("Invalid filter, or relevant filter(s) not added in settings menu. ")
                else: print("Invalid function for specified field; they are incompatible. ")
            else: print("Invalid function. Choose from 'count', 'total', or 'avg'. ")

        elif len(choiceList) == 3 and tool == "graph":
            if func == "CDF" and filt in fieldFilter:
                TVWS_cdf.cdf_graph(OutputDirectory, InputDirectory, filt, fieldFilter, dateFilter1, dateFilter2)
            elif func == "bar":
                TVWS_bargraph.barGraph(OutputDirectory, InputDirectory, fieldFilter, filt, index, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2)
                index += 1
            elif func == "table":
                TVWS_tablegraph.tableGraph(OutputDirectory, InputDirectory, fieldFilter, filt, index2, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2)
                index2 += 1
            else: print("Invalid command - Ensure correct graph utility and field has been inputted. ")
        else: print("Invalid command, re-enter. ")


def main():
    print("PCAP Trace Processing Tool")
    loop = True

    while loop:
        choice = input("Main Menu: ")
        if choice == "info":
            print("Main Menu Info: " +
                  "\nInput: " +
                  "\n- 'settings' : Settings menu for setting directory paths, fields and filters, and graph type" +
                  "\n- 'process' : Processes .pcap files in specified directory with chosen fields, and outputs them" +
                  " into csv files" +
                  "\n- 'process_<tcp/udp>flows' : Processes .pcap files in specified directory in regards to tcp or udp" +
                  " flows and outputs them into csv files" +
                  "\n- 'tools' : Tools menu for performing calculations and visualizing data" +
                  "\n- 'exit' : Exits PCAP Trace Processing Tool")
        elif choice == "settings": settings()
        elif choice == "process":
            if InputDirectory == None or OutputDirectory == None: print("Input and output directory path not set. ")
            else: TVWS_process.process(InputDirectory, OutputDirectory, fieldFilter, displayFilter, dateFilter1, dateFilter2)
        elif choice == "process_tcpflows" or choice == "process_udpflows":
            if choice == "process_tcpflows": TVWS_process.process_flows(1, InputDirectory, OutputDirectory, dateFilter1, dateFilter2)
            else: TVWS_process.process_flows(2, InputDirectory, OutputDirectory, dateFilter1, dateFilter2)
        elif choice == "tools":
            if InputDirectory == None: print("Input directory path not set. ")
            else: tools()
        elif choice == "exit": loop = False
        else: print("Invalid command, re-enter. ")


main()