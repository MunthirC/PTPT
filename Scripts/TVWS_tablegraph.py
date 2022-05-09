# TVWS_tablegraph - Munthir Chater

import plotly.figure_factory as ff
import TVWS_main_filters
import TVWS_tools1


def tableGraph(outdir, indir, filters, fil, index, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter):
    err = False

    try:
        if fil not in ["genStats", "table1", "genTCPFlowStats", "table2", "udTCPFlowStats", "table3", "httpCodes", "table4",
                       "sfTCPFlowStats", "table6"]:
            func, fiel, data = customTable(indir, filters, fil, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter)
            if outdir is not None: path = outdir + "\\table_" + str(index) + ".png"
        else:
            if fil == "genStats" or fil == "table1":
                func, fiel, data = table1(indir, filters, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter)
            elif fil == "genTCPFlowStats" or fil == "table2":
                func, fiel, data = table2(indir, filters, avgCalcs, totalCalcs, dateFilter1, dateFilter2, weatherFilter)
            elif fil == "udTCPFlowStats" or fil == "table3":
                func, fiel, data = table3(indir, filters, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter)
            elif fil == "httpCodes" or fil == "table4": func, fiel, data = table4(indir, filters, dateFilter1, dateFilter2, weatherFilter)
            else: func, fiel, data = table6(indir, filters, countCalcs, dateFilter1, dateFilter2, weatherFilter)
            if outdir is not None: path = outdir + "\\table_" + fil + ".png"
    except Exception as e:
        print("Unable to obtain data points: ", e)
        err = True

    if err == False:
        try:
            print("Graphing... ")
            funcfiel = []
            for i in range(len(fiel)):
                funcfiel.append(fiel[i] + " (" + func[i] + ")")

            table = [funcfiel, data]
            fig = ff.create_table(table, height_constant=60)
            if outdir is not None: fig.write_image(path)
            fig.show()
        except Exception as e: print("Unable to graph: ", e)


def customTable(indir, filters, fil, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter):
    fields = ""
    tableFields = []
    table_data = []

    if fil != "": print("Inputted selection is not a pre-defined table. ")

    while fields != "exit":
        fields = input("Enter a field to append to the table: ")
        if fields == "info": print("- <function type> <field> <code/service/site (if necessary)> : Enters field")
        if fields != "exit" and fields != "info":
            fields = fields.split()
            # Graphing fields not pertaining to response codes, services or sites accessed
            if len(fields) == 2:
                if fields[0] in ["count", "total", "avg"]:
                    if fields[0] == "count" and (fields[1] in filters or fields[1] == "cpkt" or fields[1] in TVWS_main_filters.tcpflowFilters or
                                                 fields[1] in TVWS_main_filters.udpflowFilters) and fields[1] in TVWS_main_filters.countFilters:
                        tableFields.append([fields[0], fields[1]])
                    elif fields[0] == "total" and (fields[1] in filters or fields[1] in TVWS_main_filters.tcpflowFilters or fields[1] in
                                                   TVWS_main_filters.udpflowFilters) and fields[1] in TVWS_main_filters.totalFilters:
                        tableFields.append([fields[0], fields[1]])
                    elif fields[0] == "avg" and (fields[1] in filters or fields[1] in TVWS_main_filters.tcpflowFilters or
                                                 fields[1] in TVWS_main_filters.udpflowFilters) and fields[1] in TVWS_main_filters.averageFilters:
                        tableFields.append([fields[0], fields[1]])
                    else: print("Field not inputted in Settings or incompatible function type. ")
                else: print("Invalid function type. Enter 'count'/'total'/'avg' in the format: <function type> <field> <code/service/site (if necessary)>")
            # Graphing fields pertaining to response codes, services or sites accessed
            elif len(fields) == 3:
                if fields[1] == "http.response.code" or fields[1] in TVWS_main_filters.servicesFields or fields[1] in TVWS_main_filters.siteFilters:
                    if fields[1] == "http.response.code":
                        if fields[2] in TVWS_main_filters.codeList: tableFields.append([fields[0], fields[1], fields[2]])
                    elif fields[1] in TVWS_main_filters.servicesFields:
                        if fields[2] in TVWS_main_filters.services: tableFields.append([fields[0], fields[1], TVWS_main_filters.services[fields[2]]])
                    elif fields[1] in TVWS_main_filters.siteFilters:
                        if fields[2] in TVWS_main_filters.websiteList: tableFields.append([fields[0], fields[1], fields[2]])
                else: print( "Invalid command. Enter in format: <function type> <field> <code/service/site (if necessary)>")
            else: print("Invalid command. Enter in format: <function type> <field> <code/service/site (if necessary)>")

    if len(tableFields) != 0:
        func, fiel = [], []
        for field in tableFields:
            # If data point has already been calculated, fetch value
            if field[0] == "count" and field[1] in countCalcs: table_data.append(countCalcs[field[1]])
            elif field[0] == "total" and field[1] in totalCalcs: table_data.append(totalCalcs[field[1]])
            elif field[0] == "avg" and field[1] in avgCalcs: table_data.append(avgCalcs[field[1]])
            # Else, calculate data point using 'calc' function via 'TVWS_tools1'
            else:
                if len(field) == 2:
                    table_data.append(TVWS_tools1.calc(field[0], field[1], filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
                else:
                    table_data.append(TVWS_tools1.calc(field[0], field[1], filters, field[2], indir, 1, dateFilter1, dateFilter2, weatherFilter))
            func.append(field[0])
            if len(field) == 2: fiel.append(field[1])
            else: fiel.append(field[1] + ": " + str(field[2]))

        return func, fiel, table_data
    else: return None, None, None


def table1(indir, filters, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter):
    table_data = []

    if "frame.len" not in totalCalcs:
        table_data.append(TVWS_tools1.calc("total", "frame.len", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(totalCalcs["frame.len"])
    if "frame.len" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "frame.len", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["frame.len"])
    if "cpkt" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "cpkt", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["cpkt"])
    if "tcp.analysis.ack_rtt" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "tcp.analysis.ack_rtt", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["tcp.analysis.ack_rtt"])
    if "tcp.analysis.retransmission" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "tcp.analysis.retransmission", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["tcp.analysis.retransmission"])

    table_data[4] = str((int(table_data[4]) / int(table_data[1])) * 100)
    table_data[2] = str((float(table_data[2]) / float(table_data[1])) * 100)
    table_data[1] = str(int(table_data[1]) / 1000000)
    table_data[0] = str(float(table_data[0]) / 1073741824)
    func = ["Total, GB", "Count, 10^6", "Count, %", "Avg, s", "Count, %"]
    fiel = ["Data", "Packets", "Control Packets", "RTT", "Retransmissions"]

    return func, fiel, table_data


def table2(indir, filters, avgCalcs, totalCalcs, dateFilter1, dateFilter2, weatherFilter):
    table_data = []

    if "flwsiz_tcpflows" not in totalCalcs:
        table_data.append(TVWS_tools1.calc("total", "flwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(totalCalcs["flwsiz_tcpflows"])
    if "flwsiz_tcpflows" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "flwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["flwsiz_tcpflows"])

    table_data[0] = str(float(table_data[0]) / 1073741824)
    func = ["Total, GB", "Avg, B"]
    fiel = ["Flow size", "Flow size"]

    return func, fiel, table_data


def table3(indir, filters, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2, weatherFilter):
    table_data = []

    if "flw_tcpflows" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "flw_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["flw_tcpflows"])
    if "upflwsiz_tcpflows" not in totalCalcs:
        table_data.append(TVWS_tools1.calc("total", "upflwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(totalCalcs["upflwsiz_tcpflows"])
    if "dwflwsiz_tcpflows" not in totalCalcs:
        table_data.append(TVWS_tools1.calc("total", "dwflwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(totalCalcs["dwflwsiz_tcpflows"])
    if "upflwsiz_tcpflows" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "upflwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["upflwsiz_tcpflows"])
    if "dwflwsiz_tcpflows" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "dwflwsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["dwflwsiz_tcpflows"])
    if "uppktsiz_tcpflows" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "uppktsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["uppktsiz_tcpflows"])
    if "dwpktsiz_tcpflows" not in avgCalcs:
        table_data.append(TVWS_tools1.calc("avg", "dwpktsiz_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(avgCalcs["dwpktsiz_tcpflows"])

    table_data[2] = str(float(table_data[2]) / 1073741824)
    table_data[1] = str(float(table_data[1]) / 1073741824)
    table_data[0] = str(int(table_data[0]) / 100000)
    func = ["Count, 10^5", "Total, GB", "Total, GB", "Avg, B", "Avg, B", "Avg, B", "Avg, B"]
    fiel = ["Flows", "Uplink Flow Size", "Downlink Flow Size", "Uplink Flow Size", "Downlink Flow Size", "Uplink Packet Size",
            "Downlink Packet Size"]

    return func, fiel, table_data


def table4(indir, filters, dateFilter1, dateFilter2, weatherFilter):
    table_data = []

    table_data.append(TVWS_tools1.calc("count", "http.response.code", filters, "200", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    table_data.append(TVWS_tools1.calc("count", "http.response.code", filters, "400", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    table_data.append(TVWS_tools1.calc("count", "http.response.code", filters, "408", indir, 1, dateFilter1, dateFilter2, weatherFilter))

    func = ["Count", "Count", "Count"]
    fiel = ["HTTP Re-Code: 200", "HTTP Re-Code: 400", "HTTP Re-Code: 408"]

    return func, fiel, table_data


def table6(indir, filters, countCalcs, dateFilter1, dateFilter2, weatherFilter):
    table_data = []

    if "successfulTCPFlows" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "successfulTCPFlows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["successfulTCPFlows"])
    if "failedTCPFlows" not in countCalcs:
        table_data.append(TVWS_tools1.calc("count", "failedTCPFlows", filters, "", indir, 1, dateFilter1, dateFilter2, weatherFilter))
    else: table_data.append(countCalcs["failedTCPFlows"])

    temp = int(table_data[1])
    table_data[1] = str((int(table_data[1]) / (int(table_data[1]) + int(table_data[0])) * 100))
    table_data[0] = str((int(table_data[0]) / (temp + int(table_data[0])) * 100))
    func = ["Count, %", "Count, %"]
    fiel = ["Successful Flows", "Failed Flows"]

    return func, fiel, table_data