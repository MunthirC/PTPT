# TVWS_bargraph - Munthir Chater

import plotly.graph_objs as go
import plotly.figure_factory as ff
import TVWS_main_filters
import TVWS_tools1


def barGraph(outdir, indir, filters, fil, index, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2):
    err = False

    try:
        if fil not in ["TCPFlowsserviceTypes", "figure7", "TCPFlowsPopURIreq","figure8", "sfTCPFlowsURI","figure9"]:
            func, fiel, data = customBar(indir, filters, fil, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2)
        else:
            if fil == "TCPFlowsserviceTypes" or fil == "figure7": func, fiel, data, data2 = figure7(indir, filters, dateFilter1, dateFilter2)
            elif fil == "TCPFlowsPopURIreq" or fil == "figure8": func, fiel, data = figure8(indir, filters, dateFilter1, dateFilter2)
            else: func, fiel, data, data2 = figure9(indir, filters, dateFilter1, dateFilter2)
    except Exception as e:
        print("Unable to obtain data points: ", e)
        err = True

    if err == False:
        try:
            print("Graphing... ")
            funcfiel = []
            for i in range(len(fiel)):
                funcfiel.append(fiel[i] + " (" + func[i] + ")")
            for i in range(len(data)):
                data[i] = float(data[i])

            if fil in ["TCPFlowsserviceTypes", "figure7", "sfTCPFlowsURI", "figure9"]:
                for i in range(len(data2)):
                    data2[i] = float(data2[i])

                fig = go.Figure(data = [
                    go.Bar(
                    name = 'Count %',
                    x = funcfiel,
                    y = data,
                    marker = dict(color = '#2f416c')),
                    go.Bar(
                    name = 'Total Bytes %',
                    x = funcfiel,
                    y = data2,
                    marker = dict(color = '#404040')) ])

                if fil in ["TCPFlowsserviceTypes", "figure7"]: title = "Bar Graph: Services Accessed - TCP Flows"
                else: title = "Bar Graph: Success/Failure of Popular URIs - TCP Flows"
                fig.update_layout(
                    title_text = title,
                    yaxis = dict(
                    tickmode = 'linear',
                    tick0 = 10,
                    dtick = 10) )

                fig.update_yaxes(range = [0,100])
                if outdir is not None: path = outdir + "/bar_" + fil + ".png"
            else:
                graph = [funcfiel, data]
                fig = ff.create_table(graph, height_constant=60)

                fig.add_trace(go.Bar(x = funcfiel, y = data, xaxis = 'x2', yaxis = 'y2', marker = dict(color = '#2f416c'),
                                     name = 'Field quantities'))

                fig.update_layout(
                    title_text = 'Bar Graph: Select Data Points',
                    height = 800,
                    margin = {'t': 75, 'l': 50},
                    yaxis = {'domain': [0, 0.5]},
                    xaxis2 = {'anchor': 'y2'},
                    yaxis2 = {'domain': [0.5, 1], 'anchor': 'x2'})

                if outdir is not None: path = outdir + "/bar_" + str(index) + ".png"

            if outdir is not None: fig.write_image(path)
            fig.show()
        except Exception as e: print("Unable to graph: ", e)


def customBar(indir, filters, fil, avgCalcs, totalCalcs, countCalcs, dateFilter1, dateFilter2):
    fields = ""
    tableFields = []
    bar_data = []

    if fil != "": print("Inputted selection is not a pre-defined bar graph. ")

    while fields != "exit":
        fields = input("Enter a field to append to the graph: ")
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
                else: print("Invalid command. Enter in format: <function type> <field> <code/service/site (if necessary)>")
            else: print("Invalid command. Enter in format: <function type> <field> <code/service/site (if necessary)>")

    if len(tableFields) != 0:
        func, fiel = [], []
        for field in tableFields:
            # If data point has already been calculated, fetch value
            if field[0] == "count" and field[1] in countCalcs: bar_data.append(countCalcs[field[1]])
            elif field[0] == "total" and field[1] in totalCalcs: bar_data.append(totalCalcs[field[1]])
            elif field[0] == "avg" and field[1] in avgCalcs: bar_data.append(avgCalcs[field[1]])
            # Else, calculate data point using 'calc' function via 'TVWS_tools1'
            else:
                if len(field) == 2: bar_data.append(TVWS_tools1.calc(field[0], field[1], filters, "", indir, 1, dateFilter1, dateFilter2))
                else: bar_data.append(TVWS_tools1.calc(field[0], field[1], filters, field[2], indir, 1, dateFilter1, dateFilter2))
            func.append(field[0])
            if len(field) == 2: fiel.append(field[1])
            else: fiel.append(field[1] + ": " + str(field[2]))

        return func, fiel, bar_data
    else: return None, None, None


def figure7(indir, filters, dateFilter1, dateFilter2):
    bar_data = []
    bar_data2 = []

    bar_data.append(TVWS_tools1.calc("count", "services_tcpflows", filters, [80], indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "services_tcpflows", filters, [6881, 6999], indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "services_tcpflows", filters, [443], indir, 1, dateFilter1, dateFilter2))

    bar_data2.append(TVWS_tools1.calc("total", "servicesbytes_tcpflows", filters, [80], indir, 1, dateFilter1, dateFilter2))
    bar_data2.append(TVWS_tools1.calc("total", "servicesbytes_tcpflows", filters, [6881, 6999], indir, 1, dateFilter1, dateFilter2))
    bar_data2.append(TVWS_tools1.calc("total", "servicesbytes_tcpflows", filters, [443], indir, 1, dateFilter1, dateFilter2))

    serCount = int(bar_data[0]) + int(bar_data[1]) + int(bar_data[2])
    serTotal = float(bar_data2[0]) + float(bar_data2[1]) + float(bar_data2[2])
    bar_data[0], bar_data[1], bar_data[2] = str((int(bar_data[0]) / serCount) * 100), str((int(bar_data[1]) / serCount) * 100),\
                                            str((int(bar_data[2]) / serCount) * 100)
    bar_data2[0], bar_data2[1], bar_data2[2] = str((float(bar_data2[0]) / serTotal) * 100), str((float(bar_data2[1]) / serTotal) * 100),\
                                               str((float(bar_data2[2]) / serTotal) * 100)
    func = ["%", "%", "%"]
    fiel = ["HTTP: Flow, Byte", "BitTorrent: Flow, Byte", "SSL: Flow, Byte"]

    return func, fiel, bar_data, bar_data2


def figure8(indir, filters, dateFilter1, dateFilter2):
    bar_data = []

    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Google", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "YouTube", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Facebook", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Twitter", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Yahoo", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "flw_tcpflows", filters, "", indir, 1, dateFilter1, dateFilter2))

    difference = int(bar_data[5]) - (int(bar_data[0]) + int(bar_data[1]) + int(bar_data[2]) + int(bar_data[3]) + int(bar_data[4]))

    bar_data[0]= str(int(bar_data[0]) / int(bar_data[5]))
    bar_data[1] = str(int(bar_data[1]) / int(bar_data[5]))
    bar_data[2] = str(int(bar_data[2]) / int(bar_data[5]))
    bar_data[3] = str(int(bar_data[2]) / int(bar_data[5]))
    bar_data[4] = str(int(bar_data[2]) / int(bar_data[5]))
    bar_data[5] = difference
    func = ["%", "%", "%"]
    fiel = ["Google: Flow, Byte", "YouTube: Flow, Byte", "Facebook: Flow, Byte", "Twitter: Flow, Byte"]

    return func, fiel, bar_data


def figure9(indir, filters, dateFilter1, dateFilter2):
    bar_data = []
    bar_data2 = []

    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Google", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "YouTube", indir, 1, dateFilter1, dateFilter2))
    bar_data.append(TVWS_tools1.calc("count", "site_tcpflows", filters, "Facebook", indir, 1, dateFilter1, dateFilter2))

    bar_data2.append(TVWS_tools1.calc("total", "siteBytes_tcpflows", filters, "Google", indir, 1, dateFilter1, dateFilter2))
    bar_data2.append(TVWS_tools1.calc("total", "siteBytes_tcpflows", filters, "YouTube", indir, 1, dateFilter1, dateFilter2))
    bar_data2.append(TVWS_tools1.calc("total", "siteBytes_tcpflows", filters, "Facebook", indir, 1, dateFilter1, dateFilter2))

    serCount = int(bar_data[0]) + int(bar_data[1]) + int(bar_data[2])
    serTotal = float(bar_data2[0]) + float(bar_data2[1]) + float(bar_data2[2])
    bar_data[0], bar_data[1], bar_data[2] = str(int(bar_data[0]) / serCount), str(int(bar_data[1]) / serCount), str(int(bar_data[2]) / serCount)
    bar_data2[0], bar_data2[1], bar_data2[2] = str(float(bar_data2[0]) / serTotal), str(float(bar_data2[1]) / serTotal), str(float(bar_data2[2]) / serTotal)
    func = ["%", "%", "%"]
    fiel = ["Google: Flow, Byte", "YouTube: Flow, Byte", "Facebook: Flow, Byte", "Twitter: Flow, Byte"]

    return func, fiel, bar_data, bar_data2