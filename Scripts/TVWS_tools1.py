# TVWS_tools1 - Munthir Chater

import os
import subprocess
import TVWS_main_filters
import TVWS_tools2

# GLOBALS
count, count2 = 0, 0
total, total2 = 0, 0
average, average2 = [], [[0,0]]


# Primary calc function which can perform calculations to obtain general packet statistics
def calc(func, filt, filters, codeOrService, directory, proto, date_filter, date_filter2, weather_filter, client_filter):
    global count, count2
    global total, total2
    global average, average2

    date_on, weather_on, client_on, client_on2 = False, False, "$1==\"\"||$1!=\"\"", "$3==\"\"||$3!=\"\""
    if date_filter != "" and date_filter2 != "": date_on = True
    if len(weather_filter) != 0: weather_on = True

    if client_filter != "":
        client_on = "$" + str(filters.index("ip.src") + 1) + "==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
        client_on2 = "$" + str(filters.index("ip.dst") + 1) + "==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
    client_filters = [client_on, client_on2, client_filter]

    if filt in filters:
        indx = (filters.index(filt))
        indx = str(indx + 1)

    count, count2 = 0, 0
    total, total2 = 0, 0
    average.clear()
    average2.clear()

    for file in os.listdir(directory):
        if file.endswith(".csv") and file != "TimestampsDuctingAndIcePeriod.csv":
            # Obtain date from file name
            if date_on == True:
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
            if (date_on == True and date >= date_filter and date <= date_filter2) or date_on == False:
                # If a weather filter has been inputted, check to see if .csv file met condition and is in dictionary
                if (weather_on is True and file in weather_filter) or weather_on is False:
                    if func == "count":
                        # Count calculations pertaining to various fields in .pcap files
                        if filt in filters and filt != "http.response.code":
                            try:
                                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($"+indx+"!=\"\"&&("+client_on+"))count=count+1}END{print count}\' "
                                                        + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                count += int(proc.communicate()[0].decode('ascii'))
                                if client_filter != "":
                                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($" + indx + "!=\"\"&&(" + client_on2 + "))count=count+1}END{print count}\' "
                                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                    count2 += int(proc.communicate()[0].decode('ascii'))
                            except:
                                print("ERROR: Could not perform calculation a count calculation. ")
                                continue

                        # Count calculations pertaining to HTTP response codes
                        elif filt == "http.response.code":
                            if "http.response.code" in filters:
                                indx1 = filters.index("http.response.code")
                                indx1 = str(indx1 + 1)
                                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($" + indx1 + "==\"" + codeOrService +
                                                        "\"&&("+client_on+"))count=count+1}END{print count}\' " +
                                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                codeTotal = int(proc.communicate()[0].decode('ascii'))
                                count += codeTotal
                                if client_filter != "":
                                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($" + indx1 + "==\"" + codeOrService +
                                                            "\"&&(" + client_on2 + "))count=count+1}END{print count}\' " +
                                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                    codeTotal = int(proc.communicate()[0].decode('ascii'))
                                    count2 += codeTotal
                            else:
                                print("'http.response.code' not in inputted filters. ")
                                break

                        # Count calculations pertaining to control packets (ACK, SYNS, FINS, and retransmissions)
                        elif filt == "cpkt":
                            indx1 = filters.index("tcp.analysis.retransmission")
                            indx2 = filters.index("tcp.flags")
                            indx3 = filters.index("tcp.len")
                            indx1, indx2, indx3 = indx1 + 1, indx2 + 1, indx3 + 1
                            indx1, indx2, indx3 = str(indx1), str(indx2), str(indx3)

                            proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if(($" + indx1 + "!=\"\"||((($" + indx2 +
                                                    "==\"0x00000001\"||$" + indx2 + "==\"0x0001\")||($" + indx2 +
                                                    "==\"0x00000002\"||$" + indx2 + "==\"0x0002\")||($" + indx2 +
                                                    "==\"0x00000010\"||$" + indx2 + "==\"0x0010\"))&&$" + indx3 +
                                                    "==\"0\"))&&("+client_on+"))count=count+1}END{print count}\' " +
                                                    os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            cpktTotal = int(proc.communicate()[0].decode('ascii'))
                            count += cpktTotal
                            if client_filter != "":
                                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if(($" + indx1 + "!=\"\"||((($" + indx2 +
                                                        "==\"0x00000001\"||$" + indx2 + "==\"0x0001\")||($" + indx2 +
                                                        "==\"0x00000002\"||$" + indx2 + "==\"0x0002\")||($" + indx2 +
                                                        "==\"0x00000010\"||$" + indx2 + "==\"0x0010\"))&&$" + indx3 +
                                                        "==\"0\"))&&("+client_on2+"))count=count+1}END{print count}\' " +
                                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                cpktTotal = int(proc.communicate()[0].decode('ascii'))
                                count2 += cpktTotal

                        # Count calculations pertaining to services accessed in TCP and UDP conversations
                        elif filt in TVWS_main_filters.servicesFields:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if filt in TVWS_main_filters.tcpflowFilters: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 1, codeOrService, client_filters)
                            elif filt in TVWS_main_filters.udpflowFilters: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 2, codeOrService, client_filters)
                            count += c1
                            count2 += c2

                        # Count calculations pertaining to domains accessed in TCP and UDP conversations
                        elif filt in TVWS_main_filters.tcpURIFilters or filt in TVWS_main_filters.udpURIFilters:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if filt in TVWS_main_filters.tcpURIFilters: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 1, codeOrService, client_filters)
                            elif filt in TVWS_main_filters.udpURIFilters: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 2, codeOrService, client_filters)
                            count += c1
                            count2 += c2

                        # Count calculations pertaining to TCP and UDP conversations that do not deal with services or domains accessed
                        else:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if proto == 1: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 1, None, client_filters)
                            else: c1, c2 = TVWS_tools2.calc2(func, filt, directory, file, 2, None, client_filters)
                            count += c1
                            count2 += c2

                    elif func == "total":
                        # Total calculations pertaining to various fields in .pcap files
                        if filt in filters:
                            try:
                                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($"+indx+"!=\"\"&&("+client_on+"))total=total+$"+indx+"}END{print total}\' "
                                                        + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                total += float(proc.communicate()[0].decode('ascii'))
                                if client_filter != "":
                                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($" + indx + "!=\"\"&&(" + client_on2 + "))total=total+$" + indx + "}END{print total}\' "
                                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                    total2 += float(proc.communicate()[0].decode('ascii'))
                            except:
                                print("ERROR: Could not perform calculation a total calculation. ")
                                continue

                        # Total calculations pertaining to services accessed in TCP and UDP conversations
                        elif filt in TVWS_main_filters.servicesFields:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if filt in TVWS_main_filters.tcpflowFilters: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 1, codeOrService, client_filters)
                            elif filt in TVWS_main_filters.udpflowFilters: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 2, codeOrService, client_filters)
                            total += t1
                            total2 += t2

                        # Total calculations pertaining to domains accessed in TCP and UDP conversations
                        elif filt in TVWS_main_filters.tcpURIFilters or filt in TVWS_main_filters.udpURIFilters:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if filt in TVWS_main_filters.tcpURIFilters: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 1, codeOrService, client_filters)
                            elif filt in TVWS_main_filters.udpURIFilters: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 2, codeOrService, client_filters)
                            total += t1
                            total2 += t2

                        # Total calculations pertaining to TCP and UDP conversations that do not deal with services or domains accessed
                        else:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if proto == 1: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 1, None, client_filters)
                            else: t1, t2 = TVWS_tools2.calc2(func, filt, directory, file, 2, None, client_filters)
                            total += t1
                            total2 += t2

                    elif func == "avg":
                        # Average calculations pertaining to various fields in .pcap files
                        if filt in filters:
                            try:
                                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($"+indx+"!=\"\"&&("+client_on+")){total=total+$"+
                                                        indx+";count=count+1}}END{print total,count}\' " +
                                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                result = str(proc.communicate()[0].decode('ascii'))
                                results = result.split()
                                total, count = float(results[0]), float(results[1])
                                average.append([total, count])
                                total, count = 0, 0
                                if client_filter != "":
                                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($"+indx+"!=\"\"&&("+client_on2+")){total=total+$"+
                                                            indx+";count=count+1}}END{print total,count}\' " +
                                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                                    result = str(proc.communicate()[0].decode('ascii'))
                                    results = result.split()
                                    total2, count2 = float(results[0]), float(results[1])
                                    average2.append([total2, count2])
                                    total2, count2 = 0, 0
                            except:
                                print("ERROR: Could not perform calculation an avg calculation. ")
                                continue

                        # Average calculations pertaining to services accessed in TCP and UDP conversations
                        elif filt in TVWS_main_filters.servicesFields:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if filt in TVWS_main_filters.tcpflowFilters: t1, c1, t2, c2 = TVWS_tools2.calc2(func, filt, directory, file, 1, codeOrService, client_filters)
                            elif filt in TVWS_main_filters.udpflowFilters: t1, c1, t2, c2 = TVWS_tools2.calc2(func, filt, directory, file, 2, codeOrService, client_filters)
                            average.append([t1, c1])
                            average2.append([t2, c2])

                        # Average calculations pertaining to TCP and UDP conversations that do not deal with services or domains accessed
                        else:
                            if client_filter != "":
                                client_on = "$1==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_on2 = "$3==\"" + TVWS_main_filters.clientFilters[client_filter] + "\""
                                client_filters = [client_on, client_on2, client_filter]
                            if proto == 1: t1, c1, t2, c2 = TVWS_tools2.calc2(func, filt, directory, file, 1, None, client_filters)
                            else: t1, c1, t2, c2 = TVWS_tools2.calc2(func, filt, directory, file, 2, None, client_filters)
                            average.append([t1, c1])
                            average2.append([t2, c2])

    if func == "count":
        print("RESULT: UPLINK - ", count, " / DOWNLINK - ", count2)
        return count
    elif func == "total":
        print("RESULT: UPLINK - ", total, " / DOWNLINK - ", total2)
        return total
    elif func == "avg":
        try:
            totalSum = 0
            totalCount = 0
            for item in average:
                totalSum += item[0]
                totalCount += item[1]
            avg = totalSum / totalCount

            totalSum = 0
            totalCount = 0
            for item in average2:
                totalSum += item[0]
                totalCount += item[1]
            avg2 = totalSum / totalCount

            print("RESULT: UPLINK - ", avg, " / DOWNLINK - ", avg2)
            return avg
        except:
            print("Error: Unable to perform calculation")
    else: return None
