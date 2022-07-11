# TVWS_main_filters - Munthir Chater

# Values for field filters, response codes, services, and sites; hardcoded to check user input and ensure validity/compatibility

# Popular websites whose IP addresses are public, thus allowing traffic to their domain to be analyzed.
websiteList = ["Yahoo", "Amazon", "Microsoft", "Bing", "MSN", "Google", "YouTube", "Facebook", "Twitter"]

# HTTP response codes referenced via https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
#  and https://www.tutorialrepublic.com/html-reference/http-status-codes.php
codeList = ["100", "200", "204", "206", "300", "301", "302", "303", "304", "400", "401", "403", "404", "408", "500",
            "501", "503"]

# Port numbers referenced via https://packetlife.net/media/library/23/common_ports.pdf
#  and https://www.godaddy.com/garage/whats-an-ssl-port-a-technical-guide-for-https/
services = {"HTTP": [80], "SSL": [443], "HTTPS": [443], "FTP": [21], "SFTP": [22], "SSH": [22], "FTPs": [990],
            "MySQL": [3306],
            "Telnet": [23], "SMPTP": [25], "DNS": [53],
            "BitTorrent": [6881, 6999], "Napster": [6699, 6701], "Gnutella": [6346, 6347],
            "WinMX": [6257], "eMule": [4672], "WASTE": [1337], "Kazaa": [1214], "Direct": [411, 412]}

# Display filters that can be used in Tshark commands when processing .pcap files
displayFilters = ["tcp", "udp"]

# Client filters correlating CPE IDs to IP addresses
clientFilters = {"101-u1" : "184.11.31.61", "101-u2" : "184.11.31.76", "101-u3" : "184.11.31.25", "101-u4" : "184.11.31.62",
                 "101-u5" : "184.11.31.66", "101-u6" : "184.11.31.32", "101-u7" : "184.11.31.08", "101-u8" : "184.11.31.35",
                 "101-u9" : "184.11.31.80", "102-u1" : "184.11.31.90", "102-u2" : "184.11.31.04", "102-u4" : "184.11.31.24",
                 "102-u5" : "184.11.31.57", "102-u6" : "184.11.31.30", "102-u7" : "184.11.31.55", "103-u2" : "184.11.31.53",
                 "103-u3" : "184.11.31.43", "103-u4" : "184.11.31.20", "104-u3" : "184.11.31.83", "104-u4" : "184.11.31.81",
                 "105-u2" : "184.11.31.54", "105-u3" : "184.11.31.12", "106-u2" : "184.11.31.77", "106-u3" : "184.11.31.85",
                 "106-u4" : "184.11.31.46", "106-u5" : "184.11.31.23"}

# Fields that can be used in 'count' operations
countFilters = ["frame.time_epoch", "frame.time_delta", "frame.len", "ip.src", "ip.dst", "eth.src", "eth.dst",
                "tcp.len", "ip.proto", "ip.ttl", "tcp.srcport", "tcp.dstport", "udp.srcport", "udp.dstport",
                "tcp.flags", "tcp.flags.ack", "tcp.flags.syn", "tcp.flags.fin", "tcp.analysis.ack_rtt", "cpkt",
                "tcp.analysis.retransmission", "tcp.time_delta", "udp.time_delta", "tcp.analysis.bytes_in_flight",
                "tcp.window_size", "http.request", "http.request.uri", "http.request.full_uri", "http.host",
                "http.request.uri.path", "http.request.uri.query", "http.response.code", "icmp.type", "flw_tcpflows",
                "successfulTCPFlows", "failedTCPFlows", "pkt_tcpflows", "uppkt_tcpflows", "dwpkt_tcpflows",
                "pkts_successfulTCPFlows", "pkts_failedTCPFlows", "services_tcpflows", "servicespackets_tcpflows",
                "site_tcpflows", "siteSuccess_tcpflows", "siteFail_tcpflows", "sitePackets_tcpflows",
                "siteSuccessPackets_tcpflows", "siteFailPackets_tcpflows", "flw_udpflows", "pkt_udpflows",
                "uppkt_udpflows", "dwpkt_udpflows", "services_udpflows", "servicespackets_udpflows", "site_udpflows",
                "sitePackets_udpflows", ]

# Fields that can be used in 'total' operations
totalFilters = ["frame.time_epoch", "frame.time_delta", "frame.len", "tcp.len", "ip.ttl", "tcp.analysis.ack_rtt",
                "tcp.time_delta", "udp.time_delta", "tcp.analysis.bytes_in_flight", "tcp.window_size",
                "pkt_tcpflows", "uppkt_tcpflows", "dwpkt_tcpflows", "flwsiz_tcpflows", "upflwsiz_tcpflows",
                "dwflwsiz_tcpflows", "flwsiz_successfulTCPFlows", "flwsiz_failedTCPFlows", "pkts_successfulTCPFlows",
                "pkts_failedTCPFlows", "sitePackets_tcpflows", "siteSuccessPackets_tcpflows", "siteFailPackets_tcpflows",
                "siteBytes_tcpflows", "siteSuccessBytes_tcpflows", "siteFailBytes_tcpflows", "pkt_udpflows",
                "uppkt_udpflows", "dwpkt_udpflows", "flwsiz_udpflows", "upflwsiz_udpflows", "dwflwsiz_udpflows",
                "pktsiz_udpflows", "uppktsiz_udpflows", "dwpktsiz_udpflows", "sitePackets_udpflows", "siteBytes_udpflows",
                "servicespackets_tcpflows", "servicespackets_udpflows", "servicesbytes_tcpflows", "servicesbytes_udpflows",
                "servicesupbytes_tcpflows", "servicesupbytes_udpflows", "servicesdwbytes_tcpflows", "servicesdwbytes_udpflows"]

# Fields that can be used in 'avg' operations
averageFilters = ["frame.time_epoch", "frame.time_delta", "frame.len", "tcp.len", "ip.ttl", "tcp.analysis.ack_rtt",
                  "tcp.time_delta", "udp.time_delta", "tcp.analysis.bytes_in_flight", "tcp.window_size",
                  "pkt_tcpflows", "uppkt_tcpflows", "dwpkt_tcpflows", "flwsiz_tcpflows", "upflwsiz_tcpflows",
                  "dwflwsiz_tcpflows", "flwsiz_successfulTCPFlows", "flwsiz_failedTCPFlows", "pktsiz_tcpflows",
                  "uppktsiz_tcpflows", "dwpktsiz_tcpflows", "pkt_udpflows", "uppkt_udpflows", "dwpkt_udpflows",
                  "flwsiz_udpflows", "upflwsiz_udpflows", "dwflwsiz_udpflows", "pktsiz_udpflows", "uppktsiz_udpflows",
                  "dwpktsiz_udpflows", "servicespackets_tcpflows", "servicespackets_udpflows", "servicesbytes_tcpflows",
                  "servicesbytes_udpflows", "servicesupbytes_tcpflows", "servicesupbytes_udpflows",
                  "servicesdwbytes_tcpflows", "servicesdwbytes_udpflows"]

# All fields that can be used in Tshark commands when processing .pcap files
fieldFilters = ["frame.time_epoch", "frame.time_delta", "frame.len", "ip.src", "ip.dst", "eth.src", "eth.dst", "tcp.len",
                "ip.proto", "ip.ttl", "tcp.srcport", "tcp.dstport", "udp.srcport", "udp.dstport", "tcp.flags",
                "tcp.flags.ack", "tcp.flags.syn", "tcp.flags.fin", "tcp.analysis.ack_rtt", "tcp.analysis.retransmission",
                "tcp.time_delta", "udp.time_delta", "tcp.analysis.bytes_in_flight", "tcp.window_size",
                "http.request", "http.request.uri", "http.request.full_uri", "http.host", "http.request.uri.path",
                "http.request.uri.query", "http.response.code", "icmp.type"]

# All fields associated with tcp flows - used when performing calculations
tcpflowFilters = ["flw_tcpflows", "successfulTCPFlows", "failedTCPFlows", "pkt_tcpflows", "uppkt_tcpflows",
                  "dwpkt_tcpflows", "flwsiz_tcpflows", "upflwsiz_tcpflows", "dwflwsiz_tcpflows", "flwsiz_successfulTCPFlows",
                  "flwsiz_failedTCPFlows", "pktsiz_tcpflows", "uppktsiz_tcpflows", "dwpktsiz_tcpflows",
                  "pkts_successfulTCPFlows", "pkts_failedTCPFlows", "services_tcpflows", "servicespackets_tcpflows",
                  "servicesbytes_tcpflows", "servicesupbytes_tcpflows", "servicesdwbytes_tcpflows", "site_tcpflows",
                  "siteSuccess_tcpflows", "siteFail_tcpflows", "sitePackets_tcpflows", "siteSuccessPackets_tcpflows",
                  "siteFailPackets_tcpflows", "siteBytes_tcpflows", "siteSuccessBytes_tcpflows", "siteFailBytes_tcpflows"]

# All fields associated with udp flows - used when performing calculations
udpflowFilters = ["flw_udpflows", "pkt_udpflows", "uppkt_udpflows", "dwpkt_udpflows", "flwsiz_udpflows", "upflwsiz_udpflows",
                  "dwflwsiz_udpflows", "pktsiz_udpflows", "uppktsiz_udpflows", "dwpktsiz_udpflows", "services_udpflows",
                  "servicespackets_udpflows", "servicesbytes_udpflows", "servicesupbytes_udpflows", "servicesdwbytes_udpflows",
                  "site_udpflows", "sitePackets_udpflows", "siteBytes_udpflows"]

# All fields associated with service analytics - used when performing calculations
servicesFields = ["services_tcpflows", "servicespackets_tcpflows", "services_udpflows", "servicespackets_udpflows",
                  "servicesbytes_tcpflows", "servicesbytes_udpflows", "servicesupbytes_tcpflows", "servicesupbytes_udpflows",
                  "servicesdwbytes_tcpflows", "servicesdwbytes_udpflows"]

# All fields associated with site analytics - used when performing calculations
siteFilters = ["site_tcpflows", "siteSuccess_tcpflows", "siteFail_tcpflows", "sitePackets_tcpflows",
               "siteSuccessPackets_tcpflows", "siteFailPackets_tcpflows", "site_udpflows", "sitePackets_udpflows"]

tcpURIFilters = ["site_tcpflows", "siteSuccess_tcpflows", "siteFail_tcpflows", "sitePackets_tcpflows",
                 "siteSuccessPackets_tcpflows", "siteFailPackets_tcpflows", "siteBytes_tcpflows",
                 "siteSuccessBytes_tcpflows", "siteFailBytes_tcpflows"]

udpURIFilters = ["site_udpflows", "sitePackets_udpflows", "siteBytes_udpflows"]
