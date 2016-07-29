import pyshark
from collections import defaultdict
import time

def from2s_compliment(num):
    if (1 << 8) & num:
        return (num ^ 0xFF) + 1
    else:
        return num

def parse(pcap_filename, csv_filename, num_packets):
    MU_groups = []
    group_ids = {}
    group_count = 0
    CBF_count = -1

    SU_MU_Flag = 0

    capture = pyshark.FileCapture(input_file=pcap_filename, display_filter='(wlan.fc.type==0 && wlan.fc.subtype==14) || (wlan.fc.type_subtype==0x15)')

    if num_packets <= 0:
        num_packets = 20000

    for i in range(1,num_packets):
        try:
            packet = capture.next()
        except:
            print "Total Packets Processed:", i-1
            break       
            
        if packet['wlan'].fc_type_subtype == '21':
            try:
                CBF_count = len([i for i in packet['wlan'].vht_ndp_sta_info.all_fields])
            except:
                continue
            current_group = {}
            current_group['time'] = packet.sniff_time.isoformat()
            current_group['addrs'] = []
            current_group['SNRs'] = []
            current_group['bssid'] = packet['wlan'].ta
            
        if packet['wlan'].fc_subtype=='14' and CBF_count > 0:
            try:
                SNR = 22 + (from2s_compliment(int(packet['wlan_mgt'].wlan_vht_compressed_beamforming_report.split(':')[0], 16)) >> 2)
            except:
                continue
                
            CBF_count -= 1
            
            current_group['addrs'].append(packet['wlan'].ta)
            current_group['SNRs'].append(SNR)
            
            if CBF_count == 0:
                addrs = ''
                for addr in current_group['addrs']:
                    addrs += addr
                    
                if addrs not in group_ids:
                    group_count += 1
                    group_ids[addrs] = group_count
                    current_group['Gid'] = group_count
                else:
                    current_group['Gid'] = group_ids[addrs]
                    
                MU_groups.append(current_group)

    import csv
    with open(csv_filename, 'w') as csvfile:
        fieldnames = [i for i in MU_groups[0].keys()]
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(MU_groups)