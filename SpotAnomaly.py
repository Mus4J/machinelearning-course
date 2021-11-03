import numpy
#import SciPy
#import joblib
#import threadpoolctl
#import scikit
import sys
import getopt
import numpy as np
from datetime import datetime
import statistics

ip_map = {}  # list wit ip as key and whole line as data
#matrix = np.array()
ip_range = '198.168.0.'
black_list = ['203', '254', '225']
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


def get_ip_data(ip):
    # print(ip_fragment)
    # oikealla datalla käytetäisiin IPinfo kirjastoa - https://github.com/ipinfo/python

    if(ip.rsplit('.', 1)[0] + '.' == ip_range):
        return ip_fragment[1]  # company ip

    for black_list_ip in black_list:
        if(black_list_ip == ip.split('.')[0]):
            return ip_fragment[0]

    current_ip = int(ip.split('.')[0])

    if(current_ip >= 1 and current_ip <= 30):
        calculate_ipfragment(0)
        return ip_fragment[2]  # australia

    elif(current_ip >= 31 and current_ip <= 60):
        calculate_ipfragment(1)
        return ip_fragment[3]  # russia

    elif(current_ip >= 61 and current_ip <= 90):
        calculate_ipfragment(2)
        return ip_fragment[4]  # pakistan

    elif(current_ip >= 91 and current_ip <= 120):
        calculate_ipfragment(3)
        return ip_fragment[5]  # intia

    elif(current_ip >= 121 and current_ip <= 150):
        calculate_ipfragment(4)
        return ip_fragment[6]  # israel

    elif(current_ip >= 151 and current_ip <= 180):
        calculate_ipfragment(5)
        return ip_fragment[7]  # china
    else:
        calculate_ipfragment(6)
        return ip_fragment[8]  # suomi


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

    for key in data_set_fragments:
        list_of_numbers.append(int(data_set_fragments[key]))

    size_points = list_of_numbers[2]
    if(size_points != 1):
        if(size_points >= 0.7 and size_points < 1):
            weights_for = [2, 1, 2, 1]
        elif(size_points > 0.4 and size_points < 0.7):
            weights_for = [2, 1, 3, 1]
        elif(size_points < 0.4):
            weights_for = [2, 1, 4, 1]
    else:
        weights_for = [2, 1, 1, 1]

    return np.average(list_of_numbers, weights=weights_for)

    # Käy läpi ja prosessoi kunkin rivin


def processLine(line_data):
    # print(line_data)
    data_set_fragments = {}
    for index, data in enumerate(line_data):
        if(index == 1):  # time
            data_set_fragments['time'] = business_hours(data)

        elif(index == 2):  # ip
            data_set_fragments['ip'] = get_ip_data(data)

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
    print(line_data[2], data_set_fragments['average'])
    ip_map[line_data[2]] = line_data[1]
    return data_set_fragments


def calculatePoinst(data_file, json_file):
    processed_data = []  # prosessoitu data pisteytyksineen
    with open(data_file, 'r') as dataFile:
        for x in dataFile:
            line = x.strip()
            line_data = line.split(' | ')
            processed_data.append(processLine(line_data))
    print(processed_data)

# Execute script and spot anomaly


def execute(dataFile, jsonFile):
    calculatePoinst(dataFile, jsonFile)

# Entry method to check arguments


def main(argv):
    dataFile = ''
    jsonFile = ''

    try:
        opts, args = getopt.getopt(
            argv, "h:data:json", ["help=", "dataFile=", "jsonFile="])
    except getopt.GetoptError:
        print('Message: Error')
        print()
        print('     -data  | --dataFile       Name of file where data will be get')
        print('     -json  | --jsonFile       Name of file where json data will be get')
        print()
        print('Example line: SpotAnomaly.py -data <dataFile> -json <jsonFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-data", "--dataFile"):
            dataFile = arg
        elif opt in ("-json", "--jsonFile"):
            jsonFile = arg

    if(dataFile != '' and jsonFile != ''):
        execute(dataFile, jsonFile)
    else:
        print('Message: Argument missing.')
        print()
        print('     -data  | --dataFile       Name of file where data will be get')
        print('     -json  | --jsonFile       Name of file where json data will be get')
        print()
        print('Example line: SpotAnomaly.py -i <file>')
        sys.exit(2)


# argumentit:
    # blacklist_ips
    # whitelist_ips
if __name__ == "__main__":
    # print(len(sys.argv))
    main(sys.argv[1:])
