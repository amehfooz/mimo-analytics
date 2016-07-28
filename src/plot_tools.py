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
        with open(str(filename)) as f:
            self.MU_groups = [{k:v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

        # Initialize counters for MU & SU transmissions
        self.mu_tx_counter = defaultdict(int)
        self.su_tx_counter = defaultdict(int)

        self.color_options = [
            "#ff0000", "#00ff00", "#0000ff", "#4a0055", "#552200", "#ffff00", "#114400", 
            "#ff9999", "#10333a", "#ff9900", "#ff0099", "#00ff99", "#0099ff", "#99ff00",
            "#990000", "#9900ff", "#009900", "#000099", "#555555", "#ff00ff", "#9999ff"
        ]
        self.colors = {}
        self.handles = {}

        self.last_index = 0
        self.llast_index = 0

        self.packet_index = 0
        self.start_time = 0

        self.timestamps = []

        self.time_index = {}

        self.snrs = {}
        self.macs = {}

    ###################################################################################################################################
    #                                                     Scrolling Plot Functions                                                    #
    ###################################################################################################################################
    def refresh_scrolling_graph(self, direction):
        start = self.start_time 

        if start not in self.time_index:
            self.time_index[start] = self.packet_index
        else:
            self.packet_index = self.time_index[start]

        plt.cla()

        while True:
            time = self.timestamps[self.packet_index]

            if time < start or time >= start + self.slice or self.packet_index >= len(self.timestamps):
                break

            self.packet_index += 1

            macs = self.macs[time]
            snrs = self.snrs[time]

            for j in range(len(macs)):
                if macs[j] in self.handles:
                    plt.bar(time+(j*self.bar_width), int(snrs[j]), self.bar_width, color = self.colors[macs[j]])
                else:
                    self.handles[macs[j]] = plt.bar(time+(j*self.bar_width), int(snrs[j]), self.bar_width, color = self.colors[macs[j]])

        self.ax.axis = [start, start+self.slice, 0, 65]
        plt.xlim(start - 0.01*self.slice, start+self.slice+(3*self.bar_width))
        plt.ylim(0, 55)

        labels = [mac[len(mac)-6:len(mac)-1] for mac in self.handles]
        handle = [self.handles[mac] for mac in self.handles]

        plt.ylabel('SNR')
        plt.xlabel('Time (s)')

        plt.legend(handle, labels, loc ='upper right', ncol = 5)

        self.fig.canvas.draw()

    def keypress(self, event):
        self.packet_index = max(self.packet_index, 0)

        if event.key == 'right':
            self.start_time += self.slice
            self.refresh_scrolling_graph(1)

        elif event.key == 'left':
            self.start_time -= self.slice
            self.refresh_scrolling_graph(1)

        else:
            exit()

    def plot_scrolling_graph(self, slice=0.02):
        plt.style.use("ggplot")

        self.fig, self.ax = plt.subplots()
        self.slice = slice
        self.bar_width = self.slice/40

        color_index = 0
        # Process plotting data
        for i in self.MU_groups:
            for mac in i['addrs'].strip("[").replace("]", "").replace(" ", "").split(","):
                if mac in self.colors:
                    continue
                
                if color_index < len(self.color_options):
                    self.colors[mac] = self.color_options[color_index]
                    color_index += 1
                else:
                    self.colors[mac] = np.random.rand(3,1)

            t = float(i['time'].split(":")[1])*60 + float(i['time'].split(":")[2])
            self.timestamps.append(t)

            self.snrs[t] = i['SNRs'].strip("[").replace("]", "").replace(" ", "").split(",")
            self.macs[t] = i['addrs'].strip("[").replace("]", "").replace(" ", "").split(",")

        self.start_time = self.timestamps[0]

        self.fig.canvas.mpl_connect('key_press_event', self.keypress)  
        self.refresh_scrolling_graph(1)

        try:
            plt.get_current_fig_manager().window.showMaximized()
        except:
            pass

        plt.show()

######################################################################################################################################
    def plot_su_mu_count_per_addr(self):
        for i in self.MU_groups:
            macs = i['addrs'].strip("[").replace("]", "").replace(" ", "").split(",")

            if len(macs) > 1:
                for m in macs:
                    self.mu_tx_counter[m] += 1
            elif len(macs) == 1:
                self.su_tx_counter[macs[0]] += 1
        plt.style.use("ggplot")
        plt.clf()
        N = len(self.mu_tx_counter)
        ind = np.array(range(0,N))    # the x locations for the groups

        width = 4.0/N       # the width of the bars: can also be len(x) sequence
        space = 0.01

        plt.xlim(0-2*width, N+2*width)
        p1 = plt.bar(ind, [self.su_tx_counter[j] for j in self.mu_tx_counter], width, color='c')

        p2 = plt.bar(ind+width+space, [self.mu_tx_counter[j] for j in self.mu_tx_counter], width, color='#ee7722')

        plt.xticks(ind + space/2.0 + width, ([mac[len(mac)-6:len(mac)-1] for mac in self.mu_tx_counter]))
        plt.legend((p1, p2), ("SU", "MU"))
        plt.xlabel("Mac Address")
        plt.ylabel("Number of NDPAs")

        try:
            plt.get_current_fig_manager().window.showMaximized()
        except:
            pass

        plt.show()
######################################################################################################################################
    def scroll(self, event):
        if event.key == 'right':
            self.start += 20
            self.end += 20
        elif event.key == 'left':
            self.start -= 20
            self.end -= 20

        while len(self.text):
            t = self.text.pop()
            t.remove()

        # Label bars
        for rect, labels in zip([p.patches for p in self.handles[max(0,self.start-1):self.end-1]], self.macaddrs[max(0, self.start-1):self.end-1]):
            height = rect[0].get_height()
            for label in labels:
                label = label.replace("\'", "")[12:]
                t = self.ax.text(rect[0].get_x() + rect[0].get_width()/2, height+4, label, ha='center', va='bottom', fontsize=self.fsize)
                self.text.append(t)
                height += 1.25*self.fsize
        plt.xlim(self.start-0.1, self.end)
        self.fig.canvas.draw()

    def plot_group_counts(self, fsize=9):
        self.start = 1
        self.end = 21
        self.fsize = fsize
        self.text = []

        plt.style.use("ggplot")
        self.fig, self.ax = plt.subplots()

        color_index = 0
        group_count = defaultdict(int)
        group_macs = {}
        group_color = {}
        # Process plotting data
        for i in self.MU_groups:
            macs = i['addrs'].strip("[").replace("]", "").replace(" ", "").split(",")
            i['Gid'] = int(i['Gid'])
            
            if i['Gid'] not in group_color:
                if color_index < len(self.color_options):
                    group_color[i['Gid']] = self.color_options[color_index]
                    color_index += 1
                else:
                    group_color[i['Gid']] = np.random.rand(3,1)

            group_count[i['Gid']] += 1
            group_macs[i['Gid']] = macs

        self.handles = []
        self.macaddrs = []
        counts = []

        ax = plt.gca()
        # Plot all bars
        for key in sorted(group_count):
            p = plt.bar(key, group_count[key], 0.7, color=group_color[key])
            self.handles.append(p)
            self.macaddrs.append(group_macs[key])

         # Label bars
        for rect, labels in zip([p.patches for p in self.handles[max(0,self.start-1):self.end-1]], self.macaddrs[max(0,self.start-1):self.end-1]):
            height = rect[0].get_height()
            for label in labels:
                label = label.replace("\'", "")[12:]
                t = self.ax.text(rect[0].get_x() + rect[0].get_width()/2, height+4, label, ha='center', va='bottom', fontsize=self.fsize)
                self.text.append(t)
                height += 1.25*self.fsize


        plt.xticks([key+0.35 for key in sorted(group_count)], [key for key in sorted(group_count)])

        plt.xlim(self.start - 0.1, self.end)
        plt.xlabel("Group ID")
        plt.ylabel("Number of NDPAs")

        try:
            plt.get_current_fig_manager().window.showMaximized()
        except:
            pass

        self.fig.canvas.mpl_connect('key_press_event', self.scroll)
        plt.show()

mu = mimo_analytics("15_1SS.csv")
mu.plot_scrolling_graph()





