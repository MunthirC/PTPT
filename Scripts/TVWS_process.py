# TVWS_process - Munthir Chater

import os
import subprocess
import csv


# Function to process and output data
def process(InputDirectory, OutputDirectory, filters, displayFilters, filter3, filter4):
    datefilter = False
    if filter3 != "" and filter4 != "": datefilter = True

    if len(filters) != 0:
        print("Processing files... ")
        for file in os.listdir(InputDirectory):
            if file.endswith(".pcap"):
                if datefilter == True:
                    index = 12
                    date = ""
                    while index < 22:
                        date += file[index]
                        index += 1
                # If a data filter has been inputted, check to see if .pcap file is within specified time-frame
                if (datefilter == True and date >= filter3 and date <= filter4) or datefilter == False:
                    filename2 = os.path.splitext(file)[0] + '.csv'
                    # Create a new .csv file as output for processed data via the .pcap file
                    with open(OutputDirectory + "/" + filename2, "w") as outfile:
                        command = []
                        commandBegin = ["tshark", "-r", os.path.join(InputDirectory, file)]
                        for item in commandBegin:
                            command.append(item)
                        # Include display filter if inputted
                        if len(displayFilters) != 0:
                            command.append("-Y")
                            command.append(displayFilters)
                        # Include field filters if inputted
                        for fltr in filters:
                            command.append("-e")
                            command.append(fltr)
                        commandEnd = ["-T", "fields", "-E", "separator=,", "-E", "occurrence=f", "-N", "m"]
                        for item in commandEnd:
                            command.append(item)
                        try:
                            # Run Tshark command with all user-specified input
                            subprocess.run(command, stdout=outfile, check=True)
                        except Exception as err:
                            print("ERROR: Unable to run tshark command: ", err)
                            continue
                else: continue
        print("Files processed. ")
    else:
        print("ERROR: No filters specified. ")


# Function to process and output data for TCP and UDP flows
def process_flows(proto, InputDirectory, OutputDirectory, filter3, filter4):
    datefilter = False
    if filter3 != "" and filter4 != "": datefilter = True

    print("Obtaining flows...")
    # Process to obtain flow data via each .pcap file in the directory and put it into a .conv file
    for file in os.listdir(InputDirectory):
        if file.endswith(".pcap"):
            if datefilter == True:
                index = 12
                date = ""
                while index < 22:
                    date += file[index]
                    index += 1
            # If a data filter has been inputted, check to see if .pcap file is within specified time-frame
            if (datefilter == True and date >= filter3 and date <= filter4) or datefilter == False:
                filename2 = os.path.splitext(file)[0] + '.csv'
                with open(OutputDirectory + "/" + filename2, "w") as outfile:
                    if proto == 1: command = ["tshark", "-r", os.path.join(InputDirectory, file), "-N", "m", "-q", "-z", "conv,tcp"]
                    else: command = ["tshark", "-r", os.path.join(InputDirectory, file), "-N", "m", "-q", "-z", "conv,udp"]
                    try:
                        # Run Tshark command to obtain all TCP/UDP conversations within a .pcap file and output into .conv format
                        subprocess.run(command, stdout=outfile, check=True)
                    except Exception as err:
                        print("ERROR: Unable to run tshark command: ", err)
                        continue
            else: continue

    print("Converting flows...")
    # Convert the .conv file to a .csv file such that calculations can be automated with awk and are easier to perform
    if proto == 1: end = "_tcpflowtemp.csv"
    else: end = "_udpflowtemp.csv"
    for file in os.listdir(OutputDirectory):
        i = 1
        if file.endswith(".csv"):
            file2 = os.path.splitext(file)[0] + end
            with open(os.path.join(OutputDirectory, file)) as infile, open(OutputDirectory + "/" + file2, "w") as outfile:
                csv_reader = csv.reader(infile, delimiter=',')
                csv_writer = csv.writer(outfile, lineterminator='\n')
                for row in csv_reader:
                    line = row[0]
                    fieldList = line.split()
                    if fieldList[0] != "================================================================================":
                        if i > 5:
                            # Get source IP address and port number
                            endPort = False
                            sourceIP = ""
                            sourcePort = ""
                            index = len(fieldList[0]) - 1
                            while index != -1:
                                char = fieldList[0][index]
                                if char != ":" and endPort == False: sourcePort = char + sourcePort
                                elif char == ":" and endPort == False: endPort = True
                                else: sourceIP = char + sourceIP
                                index -= 1
                            # Get destination IP address and port number
                            endPort = False
                            destIP = ""
                            destPort = ""
                            index = len(fieldList[2]) - 1
                            while index != -1:
                                char = fieldList[2][index]
                                if char != ":" and endPort == False: destPort = char + destPort
                                elif char == ":" and endPort == False: endPort = True
                                else: destIP = char + destIP
                                index -= 1
                            '''
                            # Get total packets' size sent in flow
                            totPktsSize = fieldList[10]
                            if fieldList[11][0] == 'M': totPktsSize = str(int(totPktsSize) * 1000000)
                            elif fieldList[11][0] == 'k': totPktsSize = str(int(totPktsSize) * 1000)
                            # Get total source packets' size
                            sourcePktsSize = fieldList[7]
                            if fieldList[8][0] == 'M': sourcePktsSize = str(int(sourcePktsSize) * 1000000)
                            elif fieldList[8][0] == 'k': sourcePktsSize = str(int(sourcePktsSize) * 1000)
                            # Get total destination packets' size
                            dstPktsSize = fieldList[4]
                            if fieldList[5][0] == 'M': dstPktsSize = str(int(dstPktsSize) * 1000000)
                            elif fieldList[5][0] == 'k': dstPktsSize = str(int(dstPktsSize) * 1000)
                            '''
                            # FieldList2: Source IP, Source Port, Dest. IP, Dest. Port, Total Packets, Total Bytes,
                            #  Uplink Packets, Uplink Bytes, Downlink Packets, Downlink Bytes, Rel. Start, Duration
                            fieldList2 = [sourceIP, sourcePort, destIP, destPort, fieldList[7], fieldList[8], fieldList[5],
                                          fieldList[6], fieldList[3], fieldList[4], fieldList[9], fieldList[10]]

                            csv_writer.writerow(fieldList2)
                            i += 1
                        else: i += 1
                    else: i += 1

            # Discard temporary file (.conv files)
            os.remove(os.path.join(OutputDirectory, file))

    # For TCP flows, determine completion/failure state
    if proto == 1:
        print("Adding additional data to flows...")
        for file in os.listdir(OutputDirectory):
            if file.endswith(end):
                filename1 = file.replace(end, ".pcap")
                filename2 = "successfulFlows.csv"
                with open(OutputDirectory + "/" + filename2, "w") as outfile:
                    try:
                        # Find all FIN packets in .pcap file and obtain 4-value tuple to identify flow membership
                        command = ["tshark", "-r", os.path.join(InputDirectory, filename1), "-Y", "tcp.flags.fin==1", "-e", "ip.src",
                                   "-e", "tcp.srcport", "-e", "ip.dst", "-e", "tcp.dstport", "-e", "tcp.stream", "-T", "fields", "-E",
                                   "separator=,", "-E", "occurrence=f", "-N", "m"]
                        subprocess.run(command, stdout=outfile, check=True)
                    except Exception as err:
                        print(err)

                filename3 = file.replace(end, "_tcpflow.csv")
                with open(os.path.join(OutputDirectory, file)) as f1, open(os.path.join(OutputDirectory, filename3), "w") as f3:
                    csv_reader1 = csv.reader(f1, delimiter=',')
                    csv_writer = csv.writer(f3, lineterminator="\n")
                    for row1 in csv_reader1:
                        # Omit flows consisting of 1 packet
                        if row1[4] == "1":
                            list = []
                            for value in row1: list.append(value)
                            list.append("N/A")
                            csv_writer.writerow(list)
                            continue
                        else:
                            with open(os.path.join(OutputDirectory, filename2)) as f2:
                                csv_reader2 = csv.reader(f2, delimiter=',')
                                fin = False
                                for row2 in csv_reader2:
                                    # If flow's 4-value tuple matches a FIN packet's 4-value tuple, that indicates a successful flow
                                    if row1[0] == row2[0] and row1[1] == row2[1] and row1[2] == row2[2] and row1[3] == row2[3]:
                                        list = []
                                        for value in row1: list.append(value)
                                        list.append("success")
                                        csv_writer.writerow(list)
                                        fin = True
                                        break
                                if fin == False:
                                    list = []
                                    for value in row1: list.append(value)
                                    list.append("fail")
                                    csv_writer.writerow(list)

                # Discard temporary files (_<tcp,udp>flowtemp.csv files, successfulFlows.csv files)
                os.remove(os.path.join(OutputDirectory, file))
                os.remove(os.path.join(OutputDirectory, filename2))

    print("Flows processed. ")