# TVWS_tools2 - Munthir Chater

import os
import subprocess
import csv
import socket
import TVWS_main_filters

# GLOBALS
filterIndices = {"successfulTCPFlows": "$13==\"success\"", "failedTCPFlows": "$13==\"fail\"",
                 "pkt_tcpflows": "5", "pkt_udpflows": "5", "uppkt_tcpflows": "7", "uppkt_udpflows": "7",
                 "dwpkt_tcpflows": "9", "dwpkt_udpflows": "9", "flwsiz_tcpflows": "6", "flwsiz_udpflows": "6",
                 "upflwsiz_tcpflows": "8", "upflwsiz_udpflows": "8", "dwflwsiz_tcpflows": "10",
                 "dwflwsiz_udpflows": "10", "pkts_successfulTCPFlows": "$13==\"success\"", "pkts_failedTCPFlows": "$13==\"fail\"",
                 "flwsiz_successfulTCPFlows": "$13==\"success\"", "flwsiz_failedTCPFlows": "$13==\"fail\"",
                 "pktsiz_tcpflows": ["6", "5"], "pktsiz_udpflows": ["6", "5"], "uppktsiz_tcpflows": ["8", "7"],
                 "uppktsiz_udpflows": ["8", "7"], "dwpktsiz_tcpflows": ["10", "9"], "dwpktsiz_udpflows": ["10", "9"],
                 "servicespackets_tcpflows": "5", "servicespackets_udpflows": "5", "servicesbytes_tcpflows": "6",
                 "servicesbytes_udpflows": "6", "servicesupbytes_tcpflows": "8", "servicesupbytes_udpflows": "8",
                 "servicesdwbytes_tcpflows": "10", "servicesdwbytes_udpflows": "10"}


# Supplementary function which conducts reverse DNS lookups and checks whether the IP address leads to the specified domain
def callLookup(ipAddr, codeOrService):
    try:
        domain_name = socket.gethostbyaddr(ipAddr)[0]
        if codeOrService.lower() in domain_name: return True
        else: return False
    except: return False

    '''
    proc = subprocess.Popen('ping -a ' + ipAddr, shell=True, stdout=subprocess.PIPE)
    st = str(proc.communicate()[0].decode('ascii'))
    try:
        st = st.split("Pinging ")
        st = st[1].split(" with")
        if codeOrService in st[0]: return True
        else: return False
    except Exception as e:
        print("Lookup error: ", e)
        return False

    try:
        addr = reversename.from_address(ipAddr)
        addr2 = str(resolver.resolve(addr,"PTR")[0])
        # print("Service: " + codeOrService + " ADDR: " +addr2)
        if codeOrService.lower() in addr2: return True
        else: return False
    except: return False
    '''


# Secondary calc function which can perform calculations to obtain general TCP/UDP flow statistics
def calc2(func, filt, directory, file, proto, codeOrService, client_filters):
    if proto == 1: end = "_tcpflow.csv"
    elif proto == 2: end = "_udpflow.csv"

    if file.endswith(end):

        if func == "count":
            # Calculation to obtain the number of total flows
            if filt == "flw_tcpflows" or filt == "flw_udpflows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($1!=\"\"&&("+client_filters[0]+"))count=count+1}END{print count}\' "
                                        + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                flowCount = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": flowCount2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($1!=\"\"&&("+client_filters[1]+"))count=count+1}END{print count}\' "
                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    flowCount2 = int(proc.communicate()[0].decode('ascii'))
                return flowCount, flowCount2

            # Calculation to obtain the number of successful or failed flows
            elif filt == "successfulTCPFlows" or filt == "failedTCPFlows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if(" + filterIndices[filt] +
                                        "&&("+client_filters[0]+"))count=count+1}END{print count}\' " + os.path.join(directory, file),
                                        shell=True, stdout=subprocess.PIPE)
                sfFlowCount = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": sfFlowCount2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if(" + filterIndices[filt] +
                                            "&&(" + client_filters[1] + "))count=count+1}END{print count}\' " + os.path.join(directory, file),
                                            shell=True, stdout=subprocess.PIPE)
                    sfFlowCount2 = int(proc.communicate()[0].decode('ascii'))
                return sfFlowCount, sfFlowCount2

            # Calculation to obtain the the number of successful or failed packets
            elif filt == "pkts_successfulTCPFlows" or filt == "pkts_failedTCPFlows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                        "&&("+client_filters[0]+"))total=total+$5}END{print total}\' " + os.path.join(directory, file),
                                        shell=True, stdout=subprocess.PIPE)
                sfpacketsTotal = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": sfpacketsTotal2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                            "&&(" + client_filters[1] + "))total=total+$5}END{print total}\' " + os.path.join(directory, file),
                                            shell=True, stdout=subprocess.PIPE)
                    sfpacketsTotal2 = int(proc.communicate()[0].decode('ascii'))
                return sfpacketsTotal, sfpacketsTotal2

            # Calculation to obtain the number of (all, uplink, or downlink) packets
            elif filt in ["pkt_tcpflows", "pkt_udpflows", "uppkt_tcpflows", "uppkt_udpflows", "dwpkt_tcpflows", "dwpkt_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($" + filterIndices[filt] +
                                        "!=\"\"&&("+client_filters[0]+"))count=count+$" + filterIndices[filt] + "}END{print count}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                packetCount = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": packetCount2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($" + filterIndices[filt] +
                                            "!=\"\"&&(" + client_filters[1] + "))count=count+$" + filterIndices[filt] + "}END{print count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    packetCount2 = int(proc.communicate()[0].decode('ascii'))
                return packetCount, packetCount2

            # Calculation to obtain the number of times a particular service was accessed (count per flow or by packets)
            elif filt in ["services_tcpflows", "services_udpflows", "servicespackets_tcpflows", "servicespackets_udpflows"]:
                if filt == "services_tcpflows" or filt == "services_udpflows":
                    if len(codeOrService) == 1:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4==\"" + str(codeOrService[0]) +
                                                "\"&&("+client_filters[0]+"))count=count+1}END{print count}\' " +
                                                os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        serCount = int(proc.communicate()[0].decode('ascii'))
                        if client_filters[1] == "$3==\"\"||$3!=\"\"": serCount2 = 0
                        else:
                            proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4==\"" + str(codeOrService[0]) +
                                                    "\"&&(" + client_filters[1] + "))count=count+1}END{print count}\' " +
                                                    os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            serCount2 = int(proc.communicate()[0].decode('ascii'))
                        return serCount, serCount2
                    elif len(codeOrService) == 2:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4>=\"" + str(codeOrService[0]) +
                                                "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&("+client_filters[0]+"))count=count+1}END{print count}\' " +
                                                os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        serCount = int(proc.communicate()[0].decode('ascii'))
                        if client_filters[1] == "$3==\"\"||$3!=\"\"": serCount2 = 0
                        else:
                            proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4>=\"" + str(codeOrService[0]) +
                                                    "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&(" + client_filters[1] + "))count=count+1}END{print count}\' " +
                                                    os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            serCount2 = int(proc.communicate()[0].decode('ascii'))
                        return serCount, serCount2
                else:
                    if len(codeOrService) == 1:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4==\"" + str(codeOrService[0]) +
                                                "\"&&("+client_filters[0]+"))count=count+$5}END{print count}\' " + os.path.join(directory, file),
                                                shell=True, stdout=subprocess.PIPE)
                        serCount = int(proc.communicate()[0].decode('ascii'))
                        if client_filters[1] == "$3==\"\"||$3!=\"\"": serCount2 = 0
                        else:
                            proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4==\"" + str(codeOrService[0]) +
                                                    "\"&&(" + client_filters[1] + "))count=count+$5}END{print count}\' " + os.path.join(directory, file),
                                                    shell=True, stdout=subprocess.PIPE)
                            serCount2 = int(proc.communicate()[0].decode('ascii'))
                        return serCount, serCount2
                    elif len(codeOrService) == 2:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4>=\"" + str(codeOrService[0]) +
                                                "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&("+client_filters[0]+"))count=count+$5}END{print count}\' " +
                                                os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        serCount = int(proc.communicate()[0].decode('ascii'))
                        if client_filters[1] == "$3==\"\"||$3!=\"\"": serCount2 = 0
                        else:
                            proc = subprocess.Popen("awk -F \",\" \'BEGIN{count=0}{if($4>=\"" + str(codeOrService[0]) +
                                                    "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&(" + client_filters[1] + "))count=count+$5}END{print count}\' " +
                                                    os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            serCount2 = int(proc.communicate()[0].decode('ascii'))
                        return serCount, serCount2

            #  Calculation to obtain the total traffic (in packets or bytes) of a visited domain
            elif filt in TVWS_main_filters.tcpURIFilters or filt in TVWS_main_filters.udpURIFilters:
                domCount = 0
                with open(os.path.join(directory, file)) as f:
                    csv_reader = csv.reader(f, delimiter=',')
                    # Iterate through flows
                    for row in csv_reader:
                        line = row[0].rstrip()
                        if line:
                            try:
                                if client_filters[0] == "$1==\"\"||$1!=\"\"":
                                    # Find HTTP/HTTPS traffic
                                    if row[3] == "80" or row[3] == "443":
                                        ipAddr = row[2]
                                        # Conduct reverse DNS lookup and see if domain matches
                                        inNet = callLookup(ipAddr, codeOrService)
                                        if inNet == True:
                                            if filt == "site_tcpflows" or filt == "site_udpflows": domCount += 1
                                            elif filt == "siteSuccess_tcpflows" and row[12] == "success": domCount += 1
                                            elif filt == "siteFail_tcpflows" and row[12] == "fail": domCount += 1
                                            elif filt == "sitePackets_tcpflows" or filt == "sitePackets_udpflows": domCount += int(row[4])
                                            elif filt == "siteSuccessPackets_tcpflows" and row[12] == "success": domCount += int(row[4])
                                            elif filt == "siteFailPackets_tcpflows" and row[12] == "fail": domCount += int(row[4])
                                else:
                                    # Find HTTP/HTTPS traffic
                                    if (row[3] == "80" or row[3] == "443") and (row[0] == TVWS_main_filters.clientFilters[client_filters[2]]):
                                        ipAddr = row[2]
                                        # Conduct reverse DNS lookup and see if domain matches
                                        inNet = callLookup(ipAddr, codeOrService)
                                        if inNet == True:
                                            if filt == "site_tcpflows" or filt == "site_udpflows": domCount += 1
                                            elif filt == "siteSuccess_tcpflows" and row[12] == "success": domCount += 1
                                            elif filt == "siteFail_tcpflows" and row[12] == "fail": domCount += 1
                                            elif filt == "sitePackets_tcpflows" or filt == "sitePackets_udpflows": domCount += int(row[4])
                                            elif filt == "siteSuccessPackets_tcpflows" and row[12] == "success": domCount += int(row[4])
                                            elif filt == "siteFailPackets_tcpflows" and row[12] == "fail": domCount += int(row[4])
                            except: continue
                return domCount, 0

        elif func == "total":
            # Calculation to obtain the total size of (all, uplink, or downlink) flows
            if filt in ["flwsiz_tcpflows", "flwsiz_udpflows", "upflwsiz_tcpflows", "upflwsiz_udpflows",
                        "dwflwsiz_tcpflows", "dwflwsiz_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($" + filterIndices[filt] +
                                        "!=\"\"&&("+client_filters[0]+"))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                flowsizeTotal = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": flowsizeTotal2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($" + filterIndices[filt] +
                                            "!=\"\"&&(" + client_filters[1] + "))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    flowsizeTotal2 = int(proc.communicate()[0].decode('ascii'))
                return flowsizeTotal, flowsizeTotal2

            # Calculation to obtain the total size of successful or failed flows
            elif filt == "flwsiz_successfulTCPFlows" or filt == "flwsiz_failedTCPFlows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                        "&&("+client_filters[0]+"))total=total+$6}END{print total}\' " + os.path.join(directory, file),
                                        shell=True, stdout=subprocess.PIPE)
                sfflowsizeTotal = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": sfflowsizeTotal2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                            "&&(" + client_filters[1] + "))total=total+$6}END{print total}\' " + os.path.join(directory, file),
                                            shell=True, stdout=subprocess.PIPE)
                    sfflowsizeTotal2 = int(proc.communicate()[0].decode('ascii'))
                return sfflowsizeTotal, sfflowsizeTotal2

            # Calculation to obtain the the number of successful or failed packets
            elif filt == "pkts_successfulTCPFlows" or filt == "pkts_failedTCPFlows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                        "&&("+client_filters[0]+"))total=total+$5}END{print total}\' " + os.path.join(directory, file),
                                        shell=True, stdout=subprocess.PIPE)
                sfpacketsTotal = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": sfpacketsTotal2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if(" + filterIndices[filt] +
                                            "&&(" + client_filters[1] + "))total=total+$5}END{print total}\' " + os.path.join(directory, file),
                                            shell=True, stdout=subprocess.PIPE)
                    sfpacketsTotal2 = int(proc.communicate()[0].decode('ascii'))
                return sfpacketsTotal, sfpacketsTotal2

            # Calculation to obtain the number of (all, uplink, or downlink) packets
            elif filt in ["pkt_tcpflows", "pkt_udpflows", "uppkt_tcpflows", "uppkt_udpflows", "dwpkt_tcpflows", "dwpkt_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($" + filterIndices[filt] +
                                        "!=\"\"&&("+client_filters[0]+"))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                packetTotal = int(proc.communicate()[0].decode('ascii'))
                if client_filters[1] == "$3==\"\"||$3!=\"\"": packetTotal2 = 0
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($" + filterIndices[filt] +
                                            "!=\"\"&&(" + client_filters[1] + "))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    packetTotal2 = int(proc.communicate()[0].decode('ascii'))
                return packetTotal, packetTotal2

            # Calculation to obtain the number of times a particular service was accessed (total packets, or (total, uplink, or downlink) bytes)
            elif filt in ["servicespackets_tcpflows", "servicespackets_udpflows", "servicesbytes_tcpflows",
                          "servicesbytes_udpflows", "servicesupbytes_tcpflows", "servicesupbytes_udpflows",
                          "servicesdwbytes_tcpflows", "servicesdwbytes_udpflows"]:
                if len(codeOrService) == 1:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($4==\"" + str(codeOrService[0]) +
                                            "\"&&("+client_filters[0]+"))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    serTotal = int(proc.communicate()[0].decode('ascii'))
                    if client_filters[1] == "$3==\"\"||$3!=\"\"": serTotal2 = 0
                    else:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($4==\"" + str(codeOrService[0]) +
                                                "\"&&(" + client_filters[1] + "))total=total+$" + filterIndices[filt] + "}END{print total}\' " +
                                                os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        serTotal2 = int(proc.communicate()[0].decode('ascii'))
                    return serTotal, serTotal2
                elif len(codeOrService) == 2:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($4>=\"" + str(codeOrService[0]) +
                                            "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&("+client_filters[0]+"))total=total+$" + filterIndices[filt] +
                                            "}END{print total}\' " + os.path.join(directory, file), shell=True,
                                            stdout=subprocess.PIPE)
                    serTotal = int(proc.communicate()[0].decode('ascii'))
                    if client_filters[1] == "$3==\"\"||$3!=\"\"": serTotal2 = 0
                    else:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0}{if($4>=\"" + str(codeOrService[0]) +
                                                "\"&&$4<=\"" + str(codeOrService[1]) + "\"&&(" + client_filters[1] + "))total=total+$" + filterIndices[filt] +
                                                "}END{print total}\' " + os.path.join(directory, file), shell=True,
                                                stdout=subprocess.PIPE)
                        serTotal2 = int(proc.communicate()[0].decode('ascii'))
                    return serTotal, serTotal2

            # Calculation to obtain the total traffic (in packets or bytes) of a visited domain
            elif filt in TVWS_main_filters.tcpURIFilters or TVWS_main_filters.udpURIFilters:
                domTotal = 0
                with open(os.path.join(directory, file)) as f:
                    csv_reader = csv.reader(f, delimiter=',')
                    # Iterate through flows
                    for row in csv_reader:
                        line = row[0].rstrip()
                        if line:
                            try:
                                if client_filters[0] == "$1==\"\"||$1!=\"\"":
                                    # Find HTTP/HTTPS traffic
                                    if row[3] == "80" or row[3] == "443":
                                        ipAddr = row[2]
                                        # Conduct reverse DNS lookup and see if domain matches
                                        inNet = callLookup(ipAddr, codeOrService)
                                        if inNet == True:
                                            if filt == "sitePackets_tcpflows" or filt == "sitePackets_udpflows": domTotal += int(row[4])
                                            elif filt == "siteSuccessPackets_tcpflows" and row[12] == "success": domTotal += int(row[4])
                                            elif filt == "siteFailPackets_tcpflows" and row[12] == "fail": domTotal += int(row[4])
                                            elif filt == "siteBytes_tcpflows" or filt == "siteBytes_udpflows": domTotal += int(row[5])
                                            elif filt == "siteSuccessBytes_tcpflows" and row[12] == "success": domTotal += int(row[5])
                                            elif filt == "siteFailBytes_tcpflows" and row[12] == "fail": domTotal += int(row[5])
                                else:
                                    # Find HTTP/HTTPS traffic
                                    if (row[3] == "80" or row[3] == "443") and (row[0] == TVWS_main_filters.clientFilters[client_filters[2]]):
                                        ipAddr = row[2]
                                        # Conduct reverse DNS lookup and see if domain matches
                                        inNet = callLookup(ipAddr, codeOrService)
                                        if inNet == True:
                                            if filt == "sitePackets_tcpflows" or filt == "sitePackets_udpflows": domTotal += int(row[4])
                                            elif filt == "siteSuccessPackets_tcpflows" and row[12] == "success": domTotal += int(row[4])
                                            elif filt == "siteFailPackets_tcpflows" and row[12] == "fail": domTotal += int(row[4])
                                            elif filt == "siteBytes_tcpflows" or filt == "siteBytes_udpflows": domTotal += int(row[5])
                                            elif filt == "siteSuccessBytes_tcpflows" and row[12] == "success": domTotal += int(row[5])
                                            elif filt == "siteFailBytes_tcpflows" and row[12] == "fail": domTotal += int(row[5])
                            except: continue
                return domTotal, 0

        elif func == "avg":
            # Calculation to obtain the average size of (all, uplink, or downlink) flows
            if filt in ["flwsiz_tcpflows", "flwsiz_udpflows", "upflwsiz_tcpflows", "upflwsiz_udpflows",
                        "dwflwsiz_tcpflows", "dwflwsiz_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt] +
                                        "!=\"\"&&("+client_filters[0]+")){total=total+$" + filterIndices[filt] + ";count=count+1}}END{print total,count}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                result = str(proc.communicate()[0].decode('ascii'))
                results = result.split()
                if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt] +
                                            "!=\"\"&&(" + client_filters[1] + ")){total=total+$" + filterIndices[filt] + ";count=count+1}}END{print total,count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results2 = result.split()
                return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])

            # Calculation to obtain the average size of successful or failed flows
            elif filt == "flwsiz_successfulTCPFlows" or filt == "flwsiz_failedTCPFlows":
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if(" + filterIndices[filt] +
                                        "&&("+client_filters[0]+")){total=total+$6;count=count+1}}END{print total,count}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                result = str(proc.communicate()[0].decode('ascii'))
                results = result.split()
                if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if(" + filterIndices[filt] +
                                            "&&(" + client_filters[1] + ")){total=total+$6;count=count+1}}END{print total,count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results2 = result.split()
                return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])

            # Calculation to obtain the average number of (all, uplink, or downlink) packets
            elif filt in ["pkt_tcpflows", "pkt_udpflows", "uppkt_tcpflows", "uppkt_udpflows", "dwpkt_tcpflows", "dwpkt_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt] +
                                        "!=\"\"&&("+client_filters[0]+")){total=total+$" + filterIndices[filt] + ";count=count+1}}END{print total,count}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                result = str(proc.communicate()[0].decode('ascii'))
                results = result.split()
                if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt] +
                                            "!=\"\"&&(" + client_filters[1] + ")){total=total+$" + filterIndices[filt] + ";count=count+1}}END{print total,count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results2 = result.split()
                return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])

            # Calculation to obtain the average size of (all, uplink, or downlink) packets
            elif filt in ["pktsiz_tcpflows", "pktsiz_udpflows", "uppktsiz_tcpflows", "uppktsiz_udpflows", "dwpktsiz_tcpflows", "dwpktsiz_udpflows"]:
                proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt][0] +
                                        "!=\"\"&&("+client_filters[0]+")){total=total+$" + filterIndices[filt][0] + ";count=count+$" +
                                        filterIndices[filt][1] + "}}END{print total,count}\' " +
                                        os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                result = str(proc.communicate()[0].decode('ascii'))
                results = result.split()
                if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                else:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($" + filterIndices[filt][0] +
                                            "!=\"\"&&(" + client_filters[1] + ")){total=total+$" + filterIndices[filt][0] + ";count=count+$" +
                                            filterIndices[filt][1] + "}}END{print total,count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results2 = result.split()
                return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])

            # Calculation to obtain the number of times a particular service was accessed (total packets, or (total, uplink, or downlink) bytes)
            elif filt in ["servicespackets_tcpflows", "servicespackets_udpflows", "servicesbytes_tcpflows", "servicesbytes_udpflows",
                          "servicesupbytes_tcpflows", "servicesupbytes_udpflows", "servicesdwbytes_tcpflows", "servicesdwbytes_udpflows"]:
                if len(codeOrService) == 1:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($4==\"" + str(codeOrService[0]) +
                                            "\"&&("+client_filters[0]+")){total=total+$" + filterIndices[filt] + ";count=count+1}}END{print total,count}\' " +
                                            os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results = result.split()
                    if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                    else:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if($4==\"" + str(codeOrService[0]) +
                                                "\"&&(" + client_filters[1] + ")){total=total+$" + filterIndices[filt] +
                                                ";count=count+1}}END{print total,count}\' " +
                                                os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        result = str(proc.communicate()[0].decode('ascii'))
                        results2 = result.split()
                    return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])
                elif len(codeOrService) == 2:
                    proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if(($4>=\"" + str(codeOrService[0]) +
                                            "\"&&$4<=\"" + str(codeOrService[1]) + "\")&&(" + client_filters[0] + ")){total=total+$" +
                                            filterIndices[filt] + ";count=count+1}}END{print total,count}\' "
                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results = result.split()
                    if client_filters[1] == "$3==\"\"||$3!=\"\"": results2 = [0, 0]
                    else:
                        proc = subprocess.Popen("awk -F \",\" \'BEGIN{total=0;count=0}{if(($4>=\"" + str(codeOrService[0]) +
                                                "\"&&$4<=\"" + str(codeOrService[1]) + "\")&&(" + client_filters[1] + ")){total=total+$" +
                                                filterIndices[filt] + ";count=count+1}}END{print total,count}\' "
                                                + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        result = str(proc.communicate()[0].decode('ascii'))
                        results2 = result.split()
                    return float(results[0]), float(results[1]), float(results2[0]), float(results2[1])

    else:
        if func == "avg": return 0, 0, 0, 0
        else: return 0, 0
