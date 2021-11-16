import numpy
# import SciPy
# import joblib
# import threadpoolctl
# import scikit
import sys
import getopt
import numpy as np
from datetime import datetime, time
import statistics
import re
import pandas as pd
from collections import defaultdict
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

ip_map = {}  # list wit ip as key and whole line as data
# matrix = np.array()
ip_fragment = [0.0, 1.0, 0.700000, 0.300000,
               0.500000, 0.700000, 0.300000, 0.300000, 0.900000]
groups = {}

# Kun ip esiintyy kasvatetaan sen kerrointa 0.00001 ja jos jokin muu ip kyseessä niin vähennetään vastaavasti --> vähän esiintyvät poikkeuksia?


def calculate_ipfragment(country):
    for index, data in enumerate(ip_fragment[2:]):
        if(country != index):
            ip_fragment[index] -= 0.000001
            continue
        ip_fragment[index] += 0.000001

# Palauttaa ko. ip:n pisteet. Jos kuuluu rangeen niin palautetaan 1 ja jos on blacklist niin palautetaan 0. Muuten palttaa ip_fragment kertoimen
# Korvataan kirjastolla, joka osaa katso mihin ryhmään kuuluu ja laskee pisteet ryhmän esiintyvyyden mukaan.
# Block_list ryhmällä ei muuttuva arvo


def get_ip_data(ip, ipRange, blackList):
    # oikealla datalla käytetäisiin IPinfo kirjastoa - https://github.com/ipinfo/python
    ip_data = []

    if(ip.rsplit('.', 1)[0] + '.' == ipRange):
        ip_data.append('C')
        ip_data.append(ip_fragment[1])
        return ip_data  # company ip

    if(len(blackList) > 0):
        for black_list_ip in blackList:
            if(black_list_ip == ip.split('.')[0]):
                ip_data.append('B')
                ip_data.append(ip_fragment[0])
                return ip_data

    current_ip = int(ip.split('.')[0])

    if(current_ip >= 1 and current_ip <= 30):
        calculate_ipfragment(0)
        ip_data.append('AUS')
        ip_data.append(ip_fragment[2])
        return ip_data  # australia

    elif(current_ip >= 31 and current_ip <= 60):
        calculate_ipfragment(1)
        ip_data.append('RUS')
        ip_data.append(ip_fragment[3])
        return ip_data  # russia

    elif(current_ip >= 61 and current_ip <= 90):
        calculate_ipfragment(2)
        ip_data.append('PAK')
        ip_data.append(ip_fragment[4])
        return ip_data  # pakistan

    elif(current_ip >= 91 and current_ip <= 120):
        calculate_ipfragment(3)
        ip_data.append('INT')
        ip_data.append(ip_fragment[5])
        return ip_data  # intia

    elif(current_ip >= 121 and current_ip <= 150):
        calculate_ipfragment(4)
        ip_data.append('ISR')
        ip_data.append(ip_fragment[6])
        return ip_data  # israel

    elif(current_ip >= 151 and current_ip <= 180):
        calculate_ipfragment(5)
        ip_data.append('CHI')
        ip_data.append(ip_fragment[7])
        return ip_data  # china
    else:
        calculate_ipfragment(6)
        ip_data.append('SUO')
        ip_data.append(ip_fragment[8])
        return ip_data  # suomi


# Katsotaan onko aika työajan sisällä

def business_hours(time):
    date_time = time.split('-')
    hours = int(date_time[1].split(':')[0].strip())
    if(hours >= 8 and hours <= 16):
        return 1.0  # työajan sisällä
    elif(hours >= 7 and hours < 8):
        return 0.7
    elif(hours >= 6 and hours < 7):
        return 0.5
    elif(hours >= 5 and hours < 6):
        return 0.40
    elif(hours >= 4 and hours < 5):
        return 0.35
    elif(hours >= 3 and hours < 4):
        return 0.25
    elif(hours >= 2 and hours < 3):
        return 0.15
    elif(hours >= 1 and hours < 2):
        return 0.05
    elif(hours >= 16 and hours < 19):
        return 0.7
    elif(hours >= 19 and hours < 20):
        return 0.6
    elif(hours >= 20 and hours < 21):
        return 0.55
    elif(hours >= 21 and hours < 22):
        return 0.45
    elif(hours >= 22 and hours < 23):
        return 0.3
    elif(hours >= 23 and hours < 24):
        return 0.15
    elif(hours > 0 and hours < 1):
        return 0.15
    return 0.0

    # TODO: Tehdään lopussa
    # onko lähellä olevia aikoja samalla ipllä? - Epäilyttävää jos on pommitettu
    # Katsotaan monestikko on olemassa tehdään vasta kun kaikki prosessoitu
    # for key, value in ip_map.items():
    #                if(key == data):
    #                    data_set_fragments['number_ip_occured']


# Calculates average of points


def getAverage(data_set_fragments):
    list_of_numbers = []

    for x, key in enumerate(data_set_fragments):
        if(x == 0 or x == 1):
            continue
        elif(x == 3):
            if(data_set_fragments[key] == 'B'):
                return 0
            else:
                continue
        list_of_numbers.append(int(data_set_fragments[key]))

    size_points = list_of_numbers[2]
    if(list_of_numbers[3] != 1):
        method_points = 4
    else:
        method_points = 1
    if(size_points != 1):
        if(size_points >= 0.7 and size_points < 1):
            weights_for = [2, 1, 2, method_points]
        elif(size_points > 0.4 and size_points < 0.7):
            weights_for = [2, 1, 3, method_points]
        elif(size_points < 0.4):
            weights_for = [2, 1, 4, method_points]
    else:
        weights_for = [2, 1, 1, method_points]

    return np.average(list_of_numbers, weights=weights_for)


# List of all the login information in the company
login_information = {'aku.ankka@comppanyx.fi': 'aku', 'minni.hiiri@comppanyx.fi': 'minni', 'roope.ankka@comppanyx.fi': 'roope', 'hessu.hopo@comppanyx.fi': 'hessu', 'milla.magia@comppanyx.fi': 'milla',
                     'tupu.ankka@comppanyx.fi': 'tupu', 'lupu.ankka@comppanyx.fi': 'lupu', 'hupu.ankka@comppanyx.fi': 'hupu', 'it@comppanyx.fi': 'it', 'support@comppanyx.fi': 'support', 'asiakaspalvelu@comppanyx.fi': 'aspa'}


# Goes trough login information and which ip/country they are done / attempted

def processJsonLine(line_data, processed_data):
    if(processed_data['Country_flag'] == 'C'):
        # onnistunut oikea kirjautuminen yrityksensisältä
        if(login_information[line_data[1]] == line_data[3]):
            return 1
        else:   # väärä kirjautuminen yrityksen sisältä
            return 0.8
    elif(processed_data['Country_flag'] == 'SUO'):
        # onnistunut oikea kirjautuminen Suomesta
        if(login_information[line_data[1]] == line_data[3]):
            return 0.8
        else:   # väärä kirjautuminen Suomesta
            return 0.6
    else:
        if(processed_data['ip'] < 0):
            # onnistunut oikea kirjautuminen huonosta ip:stä
            if(login_information[line_data[1]] == line_data[3]):
                return 0
            else:   # väärä kirjautuminen huonosta ip:stä
                return 0.1
        else:
            # onnistunut oikea kirjautuminen maailmalta
            if(login_information[line_data[1]] == line_data[3]):
                if(processed_data['ip'] < 0.5):
                    return 0
                else:
                    return processed_data['ip'] * 0.5
            else:   # väärä kirjautuminen maailmalta
                return processed_data['ip'] * processed_data['ip']


# Käy läpi ja prosessoi kunkin rivin


def processLine(line_data, ipRange, blackList):
    data_set_fragments = {}
    for index, data in enumerate(line_data):
        data_set_fragments['Id'] = line_data[2]
        if(index == 1):  # time
            data_set_fragments['time'] = data.replace(' - ', '-')
            data_set_fragments['time_points'] = business_hours(data)

        elif(index == 2):  # ip
            ip_data = []
            ip_data = get_ip_data(data, ipRange, blackList)
            data_set_fragments['Country_flag'] = ip_data[0]
            data_set_fragments['ip'] = ip_data[1]

        elif(index == 5):  # size
            if(int(data) > 3000 and int(data) < 5000):
                data_set_fragments['size'] = 0.5
            elif(int(data) > 5001):
                data_set_fragments['size'] = 0.0
            else:
                data_set_fragments['size'] = 1.0

        elif(index == 6):  # method
            if(data != 'POST /api/example/login/?venue=dms HTTP/1.1 (application/json)'):
                data_set_fragments['method'] = 0.0
            else:
                data_set_fragments['method'] = 1.0
    data_set_fragments['average'] = getAverage(data_set_fragments)

    ip_map[line_data[2]] = line_data[1]
    return data_set_fragments


# Formats JSON data into the more readable and usable format
# Jos olisi oikea/oikein formatoitu JSON file voitaisiin tehdä tämä eri tavalla

def getJsonData(line):
    tmp = re.sub(
        '{"JavaScript Object Notation: application/json": [{"Object \\[0-9]*": {"Member Key:": {', '', line)
    tmp = re.sub('": {"String": "', '|', tmp)
    tmp = tmp.replace('}', '').replace(']', '')
    tmp = re.sub('", "Key": "password"', '', tmp)
    tmp = re.sub('", "Key": "email", "', '|', tmp)
    tmp = tmp.replace('"', '')
    tmp = tmp.replace('\n', '')
    return tmp.split('|')


# Groups data by IP-Addresses

def groupData(all_data):
    result_of_time_occurance = {}

    for x, data in enumerate(all_data):
        if str(data['Id']) in groups:
            groups[data['Id']].append(data)
        else:
            groups[str(data['Id'])] = []
            groups[data['Id']].append(data)

    for key in groups:
        if(len(groups[key]) > 1):
            result_of_time_occurance = createListOfDatas(groups[key])

            time_keys = result_of_time_occurance.keys()

            # TODO Pitäisi toimia, mutta tarvitsee varmistaa anomoaliaa sisältävällä datalla
            for l, timeKey in enumerate(time_keys):
                groups[key][int(result_of_time_occurance[timeKey])
                            ]['Time_anomaly'] = timeKey.split(':')[0]
        else:
            groups[key][0]['Time_anomaly'] = 'False'

# Calulates weather difference betweem date times is too small (less than 20 sec) and it occures at least 4 times in order
# TODO Pitäisi toimia, mutta tarvitsee varmistaa anomoaliaa sisältävällä datalla


def calculateTimeOccurance(dates):
    list_of_ranges = []

    for x, date in enumerate(range(len(dates)-1)):
        val = dates[x+1] - dates[x]
        list_of_ranges.append(val)

    counter = 0
    start_index = 0
    anomaly_indexer = 0
    normal_indexer = 0
    result = {}

    for y, td in enumerate(range(len(list_of_ranges)-1)):
        days = list_of_ranges[y].days
        hours, remainder = divmod(list_of_ranges[y].seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # days, hours, minutes, seconds
        if(days == 0 and hours == 0 and minutes == 0 and seconds >= 10):
            if(counter == 0):
                start_index = y
            counter += 1
        else:
            if(counter >= 3):
                anomaly_indexer += 1
            counter = 0

            result['False: '+str(normal_indexer)] = str(y)
            normal_indexer += 1

        if(counter >= 3):
            result['True: '+str(anomaly_indexer)
                   ] = str(start_index) + '-' + str(y)
    return result


# Creates list of all the dates in a data group
# TODO Pitäisi toimia, mutta tarvitsee varmistaa anomoaliaa sisältävällä datalla

def createListOfDatas(data_group):
    list_of_dates = []

    for x, data in enumerate(data_group):
        tmp = data['time'].split('-')
        date = tmp[0].split('.')
        time = tmp[1].split(':')

        date_time = datetime(int(date[0]), int(date[1]), int(
            date[2]), int(time[0]), int(time[1]), int(time[2]))

        list_of_dates.append(date_time)
        list_of_dates = sorted(list_of_dates)

    return calculateTimeOccurance(list_of_dates)


def calculatePoinst(data_file, json_file, ipRange, blackList):
    processed_data = []  # prosessoitu data pisteytyksineen

    with open(data_file, 'r') as dataFile:
        for x in dataFile:
            line = x.strip()
            line_data = line.split(' | ')
            processed_data.append(processLine(line_data, ipRange, blackList))

    with open(json_file, 'r') as jsonFile:
        for x, y in enumerate(jsonFile):
            json_line_data = getJsonData(y)
            if(x >= len(processed_data)):
                print(
                    'ERROR: There is more data in JSON file than in processed_data file')
                break
            elif(x < len(processed_data)):
                processed_data[x]['logIn'] = processJsonLine(
                    json_line_data, processed_data[x])

    groupData(processed_data)


# Generates outputfile of data

def generateOutputFile():
    with open('result.txt', 'w') as outfile:
        json.dump(groups, outfile, indent=4)


# Draws data with plot
# TODO


def drawResult(ipRange):
    x = []
    y = []
    z = []
    xl = []
    yl = []
    zl = []
    xs = []
    ys = []
    zs = []

    ip_range = ipRange.split('.')

    fig = plt.figure(figsize=(10, 10))

    ax = plt.axes(projection='3d')
    ax.grid(False)

    for key in groups:
        for data in groups[key]:
            feature_points = 0
            tmp = data['Id'].split('.')
            if not 'Time_anomaly' in data:
                points_list = [data['average'], data['logIn']]
                feature_points = np.average(points_list, weights=[3, 1])
            else:
                if(data['Time_anomaly'] == 'True'):
                    xs.append(int(tmp[0]))
                    ys.append(int(tmp[1]))
                    zs.append(int(tmp[2]) + int(tmp[3]))
                else:
                    points_list = [data['average'], data['logIn']]
                    feature_points = np.average(points_list, weights=[3, 1])
            if(feature_points < 0.3):
                xs.append(int(tmp[0]))
                ys.append(int(tmp[1]))
                zs.append(int(tmp[2]) + int(tmp[3]))
            else:
                if(ipRange in data['Id']):
                    xl.append(int(tmp[0]))
                    yl.append(int(tmp[1]))
                    zl.append(int(tmp[2]) + int(tmp[3]))
                else:
                    x.append(int(tmp[0]))
                    y.append(int(tmp[1]))
                    z.append(int(tmp[2]) + int(tmp[3]))

    ax.scatter3D(x, y, z, s=5, marker='o', c='green')
    ax.scatter3D(xl, yl, zl, s=5, marker='o', c='blue')
    ax.scatter3D(xs, ys, zs, s=20, marker='*', c='red')

    data_toPlot = draw_scatter_2D(groups, ipRange)

    x1 = data_toPlot[2]
    y1 = data_toPlot[0]
    x2 = data_toPlot[3]
    y2 = data_toPlot[1]
    x3 = data_toPlot[5]
    y3 = data_toPlot[4]
    x4 = data_toPlot[7]
    y4 = data_toPlot[6]

    fig = plt.figure(figsize=(10, 10))
    fig.suptitle('Scatter Plot', fontsize=14, fontweight='bold')
    ay = fig.add_subplot(111)

    fig.subplots_adjust(top=0.85)
    ay.set_xlabel('Time')
    ay.set_ylabel('Value (AVG)')

    total_txt = 'Total of entries: ' + str(len(x1)+len(x2)+len(x3))
    total_txt2 = 'IP range: GREEN'
    total_txt3 = 'Normal: SKYBLUE'
    total_txt4 = 'Low IP points (close to anomaly): GREY'
    total_txt5 = 'Anomaly: RED'

    text_x_axis_value = 0.9
    ay.text(text_x_axis_value, 0.90, total_txt, horizontalalignment='center',
            verticalalignment='center', transform=ay.transAxes)
    ay.text(text_x_axis_value, 0.87, total_txt2, horizontalalignment='center',
            verticalalignment='center', transform=ay.transAxes)
    ay.text(text_x_axis_value, 0.85, total_txt3, horizontalalignment='center',
            verticalalignment='center', transform=ay.transAxes)
    ay.text(text_x_axis_value, 0.83, total_txt4, horizontalalignment='center',
            verticalalignment='center', transform=ay.transAxes)
    ay.text(text_x_axis_value, 0.81, total_txt5, horizontalalignment='center',
            verticalalignment='center', transform=ay.transAxes)

    ay.plot_date(x1, y1, xdate=True, ydate=False, color='skyblue')
    ay.plot_date(x2, y2, xdate=True, ydate=False, color='red')
    ay.plot_date(x3, y3, xdate=True, ydate=False, color='grey')
    ay.plot_date(x4, y4, xdate=True, ydate=False, color='green')

    plt.show()


def draw_scatter_2D(groups, ipRange):
    normal_data_avg = []
    anomaly_data_avg = []
    normal_data_dates = []
    anomaly_data_dates = []
    ipFlag_data_dates = []
    ipFlag_data_avg = []
    ipRange_data_dates = []
    ipRange_data_avg = []

    for key in groups:
        for data in groups[key]:
            if(data['average'] >= 0.4):
                if not 'Time_anomaly' in data:
                    normal_data_avg.append(data['average'])
                    normal_data_dates.append(
                        pd.to_datetime(data['time'].split('-')[0].replace('.', '-')))
                    continue
                if(data['Time_anomaly'] == True):
                    anomaly_data_avg.append(data['average'])
                    anomaly_data_dates.append(pd.to_datetime(
                        data['time'].split('-')[0].replace('.', '-')))
                elif(data['ip'] < 0.3):
                    ipFlag_data_avg.append(data['average'])
                    ipFlag_data_dates.append(pd.to_datetime(
                        data['time'].split('-')[0].replace('.', '-')))
                elif(ipRange in data['Id']):
                    ipRange_data_dates.append(data['average'])
                    ipRange_data_avg.append(
                        pd.to_datetime(data['time'].split('-')[0].replace('.', '-')))
                else:
                    normal_data_avg.append(data['average'])
                    normal_data_dates.append(
                        pd.to_datetime(data['time'].split('-')[0].replace('.', '-')))
            else:
                anomaly_data_avg.append(data['average'])
                anomaly_data_dates.append(
                    pd.to_datetime(data['time'].split('-')[0].replace('.', '-')))

    return [normal_data_avg, anomaly_data_avg,
            normal_data_dates, anomaly_data_dates, ipFlag_data_avg, ipFlag_data_dates, ipRange_data_dates, ipRange_data_avg]


# Execute script and spot anomaly


def execute(dataFile, jsonFile, ipRange, blackList):
    calculatePoinst(dataFile, jsonFile, ipRange, blackList)
    # generateOutputFile()
    drawResult(ipRange)

# Entry method to check arguments


def main(argv):
    dataFile = ''
    jsonFile = ''
    ipRange = ''
    blackList = []

    try:
        opts, args = getopt.getopt(
            argv, "h:d:j:i:b:", ["help=", "dataFile=", "jsonFile=", "iprange=", "blacklist="])
    except getopt.GetoptError:
        print('Message: Error')
        print()
        print('     -d     | --dataFile       Name of file where data will be get')
        print('     -j     | --jsonFile       Name of file where json data will be get')
        print('     -i     | --iprange        Ip range used to terminate company wide ip range')
        print('     -b     | --blacklist      Blacklisted ips seperated with semicolon(;)')
        print()
        print('Example line: SpotAnomaly.py -data <dataFile> -json <jsonFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--dataFile"):
            dataFile = arg
        elif opt in ("-j", "--jsonFile"):
            jsonFile = arg
        elif opt in ("-i", "--iprange"):
            if(len(arg) < 10):
                print('Ip range length too small')
            elif(len(arg) > 10):
                print('Ip range length too big')
            else:
                ipRange = arg
        elif opt in ("-b", "--blacklist"):
            if not (any(i.isdigit() for i in arg)):
                print('Message: Blacklist can only contain digits')
                print()
                print(
                    '     -d     | --dataFile       Name of file where data will be get')
                print(
                    '     -j     | --jsonFile       Name of file where json data will be get')
                print(
                    '     -i     | --iprange        Ip range used to terminate company wide ip range')
                print(
                    '     -b     | --blacklist      Blacklisted ips seperated with semicolon(;)')
                print()
                print('Example line: SpotAnomaly.py -data <dataFile> -json <jsonFile>')
                sys.exit(2)
            else:
                if ';' in arg:
                    blackList = arg.split(';')
                elif(len(arg) > 0):
                    blackList.append(arg)
                for str in blackList:
                    if(len(str) > 3):
                        print(
                            'Message: Some ip or ips in the blacklist are longer than 3 digits')
                        print()
                        print(
                            '     -d     | --dataFile       Name of file where data will be get')
                        print(
                            '     -j     | --jsonFile       Name of file where json data will be get')
                        print(
                            '     -i     | --iprange        Ip range used to terminate company wide ip range')
                        print(
                            '     -b     | --blacklist      Blacklisted ips seperated with semicolon(;)')
                        print()
                        print(
                            'Example line: SpotAnomaly.py -data <dataFile> -json <jsonFile>')
                        sys.exit(2)
    if(dataFile != '' and jsonFile != '' and ipRange != ''):
        execute(dataFile, jsonFile, ipRange, blackList)
    else:
        print('Message: Argument missing.')
        print()
        print('     -d     | --dataFile       Name of file where data will be get')
        print('     -j     | --jsonFile       Name of file where json data will be get')
        print('     -i     | --iprange        Ip range used to terminate company wide ip range')
        print('     -b     | --blacklist      Blacklisted ips seperated with semicolon(;)')
        print()
        print('Example line: SpotAnomaly.py -i <file>')
        sys.exit(2)


# argumentit:
    # blacklist_ips
if __name__ == "__main__":
    main(sys.argv[1:])
