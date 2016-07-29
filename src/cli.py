from plot_tools import plot_tools
import parse_pcap
import sys

print "#####################\n# MU-MIMO Analytics #\n#####################"
options = """1. Process pcap file into csv file.
2. Plot MU-MIMO groups per NDPA against time.
3. Plot MU-MIMO and SU-MIMO NDPA count per client.
4. Plot NDPA count per MU-MIMO group.
5. Exit
Enter Choice:"""

plotter = 0
choice = 0
while choice != 5:
	print options
	try:
		choice = int(raw_input())
	except:
		choice = 0

	if choice == 1:
		pcap_filename = raw_input("Enter Pcap Filename: ")
		csv_filename = raw_input("Enter output CSV Filename: ")
		numpackets = raw_input("Maximum Packets to Process: ")
		parse_pcap.parse(pcap_filename, csv_filename, 100000)

	elif choice > 1 and choice < 5:
		if plotter == 0:
			filename = raw_input("Enter CSV Filename: ")
			plotter = plot_tools(filename)

		if choice == 2:
			plotter.plot_scrolling_graph()
		elif choice == 3:
			plotter.plot_su_mu_count_per_addr()
		elif choice == 4:
			plotter.plot_group_counts()