import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import FormatStrFormatter
from collections import defaultdict

class mimo_analytics:
    def __init__(self, filename):
        # Read CSV File containing control information
        with open(filename) as f:
            self.MU_groups = [{k:v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

        # Initialize counters for MU & SU transmissions
        self.mu_tx_counter = defaultdict(int)
        self.su_tx_counter = defaultdict(int)

        self.colors = {}
        self.handles = {}

        self.last_index = 0
        self.llast_index = 0

        self.packet_index = 0
        self.start_time = 0

        self.timestamps = []
        self.snrs = {}
        self.macs = {}

    ###################################################################################################################################
    #                                                     Scrolling Plot Functions                                                    #
    ###################################################################################################################################
    def refresh_scrolling_graph(self):
        start = self.start_time


        self.llast_index = self.last_index
        self.last_index = self.packet_index

        plt.cla()

        while True:
            time = self.timestamps[self.packet_index]

            if time > start + self.slice or self.packet_index >= len(self.timestamps):
                break

            macs = self.macs[time]
            snrs = self.snrs[time]

            for j in range(len(macs)):
                if macs[j] in self.handles:
                    plt.bar(time+(j*self.bar_width), int(snrs[j]), self.bar_width, color = self.colors[macs[j]])
                else:
                    self.handles[macs[j]] = plt.bar(time+(j*self.bar_width), int(snrs[j]), self.bar_width, color = self.colors[macs[j]])

            self.packet_index += 1

        self.ax.axis = [start, start+self.slice, 0, 65]
        plt.xlim(start - 0.01*self.slice, start+self.slice+(3*self.bar_width))
        plt.ylim(0, 55)

        labels = [mac[len(mac)-6:len(mac)-1] for mac in self.handles]
        handle = [self.handles[mac] for mac in self.handles]


        plt.legend(handle, labels, loc ='upper right', ncol = 5)
        print self.packet_index, self.last_index

        self.fig.canvas.draw()

    def keypress(self, event):
        if event.key == 'right':
            self.start_time += self.slice
        elif event.key == 'left':
            self.start_time -= self.slice
            self.packet_index = self.llast_index
            print "Indexed back to", self.packet_index
        else:
            exit()

        self.refresh_scrolling_graph()

    def plot_scrolling_graph(self, slice=0.015):
        plt.style.use("ggplot")
        #plt.clf()
        self.fig, self.ax = plt.subplots()
        self.slice = slice
        self.bar_width = self.slice/30

        # Process plotting data
        for i in self.MU_groups:
            for mac in i['addrs'].strip("[").replace("]", "").replace(" ", "").split(","):
                if mac in self.colors:
                    continue
                    
                self.colors[mac] = np.random.rand(3,1)

            t = float(i['time'].split(":")[1])*60 + float(i['time'].split(":")[2])
            self.timestamps.append(t)

            self.snrs[t] = i['SNRs'].strip("[").replace("]", "").replace(" ", "").split(",")
            self.macs[t] = i['addrs'].strip("[").replace("]", "").replace(" ", "").split(",")

        self.start_time = self.timestamps[0]

        self.fig.canvas.mpl_connect('key_press_event', self.keypress)  
        self.refresh_scrolling_graph()
        plt.show()

######################################################################################################################################



mu = mimo_analytics("15_1SS.csv")
mu.plot_scrolling_graph(slice=0.03)





