# PTPT
Capstone project focusing on Television White Space (TVWS) technology for CSI 499 at SUNY Albany. This tool, regarded as the PCAP Trace Processing Tool (PTPT), allows researchers to process, analyze, and visualize network traces to gather insights on network performance and user behavior.

More specifically, the PTPT’s capabilities range from processing network traces at the packet and flow level, calculating 
important data points, and visualizing statistics in several ways. The tool is designed to provide an 
efficient way to view select, sought after data points without the burden of loading unnecessary extras.
Calculating specific, aggregate values without complication is present, as values can be obtained in a 
straightforward manner with simple commands. And the further utilization of visualization features 
permits an additional way to view values instead of solely relying on the numbers.


SET-UP:

Installations (software): 
- Wireshark (https://www.wireshark.org/#download)
- Tshark (https://www.wireshark.org/#download; *comes installed with Wireshark)
- AWK (http://gnuwin32.sourceforge.net/packages/gawk.htm)

Installations (libraries/packages):
- NumPY (‘pip install numpy’)
- Matplotlib (‘pip install matplotlib’)
- Plotly (‘pip install plotly’)
- Kaleido (‘pip install kaleido’)

Environment Settings:
- The path to Wireshark should be added to the PATH environment variable under system 
settings. Without this, Tshark commands to process network traces cannot be successfully 
executed. For Windows, this can be found under ‘System Properties -> Environment Variables -> 
System Variables’. This is the recommended approach, however an alternative would be to add 
the full path to Wireshark in the TVWS_process script instead. 
- Wireshark’s settings should ideally be set to default. Some settings, such as name resolution 
under ‘Edit -> Preferences -> Name Resolution’ are overridden and will not cause complications 
when running the software, however other changes may cause unforeseen issues. 
- The Python libraries need to be updated to the latest version.
