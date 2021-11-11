from random import randrange
from datetime import timedelta
from datetime import datetime
import random
import sys
import getopt
import json
import jsonlines

# Generates datarows with anomaly in it, random ip and writes it in the file


def generate_anomaly_data(file, index):
    for x in range(5):
        text = str(index + x) + ' | ' + str(random_date().strftime("%Y.%m.%d - %H:%M:%S")) + ' | ' + random_ip_NOTINRANGE() + \
            ' | 10.0.0.1 | HTTP | ' + str(random.randrange(
                1000, 2000)) + ' | POST /api/example/login/?venue=ask HTTP/1.1 (application/json)\n'
        file.write(text)
        generate_application_json_data(index + x, False)

    for x in range(5):
        text = str(index + x + 5) + ' | ' + str(random_date().strftime("%Y.%m.%d - %H:%M:%S")) + ' | ' + random_ip_NOTINRANGE() + \
            ' | 10.0.0.1 | HTTP | ' + str(random.randrange(
                3000, 10000)) + ' | POST /api/example/login/?venue=ask HTTP/1.1 (application/json)\n'
        file.write(text)
        generate_application_json_data(index + x + 5, False)

    for x in range(5):
        text = str(index + x + 10) + ' | ' + str(random_date().strftime("%Y.%m.%d - %H:%M:%S")) + ' | ' + random_ip_NOTINRANGE() + \
            ' | 10.0.0.1 | HTTP | ' + str(random.randrange(
                3000, 10000)) + ' | POST /api/example/login/?venue=ask HTTP/1.1 (application/json)\n'
        file.write(text)
        generate_application_json_data(index + x + 10, False)

# Generates datarows with random ip inside of the range and writes it in the file


def generate_valid_data_IPRANGE(file, iprange):
    for x in range(7500):
        text = str(x) + ' | ' + str(random_date().strftime("%Y.%m.%d - %H:%M:%S")) + ' | ' + random_ip_INRANGE(iprange) + \
            ' | 10.0.0.1 | HTTP | ' + str(random.randrange(
                1000, 2000)) + ' | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)\n'
        file.write(text)
        generate_application_json_data(x, True)

# Generates datarows with random ip outside of the range and writes it in the file


def generate_valid_data_WIDEIP(file):
    text = ''
    for x in range(2500):
        text = str(7500 + x) + ' | ' + str(random_date().strftime("%Y.%m.%d - %H:%M:%S")) + ' | ' + random_ip_NOTINRANGE() + \
            ' | 10.0.0.1 | HTTP | ' + str(random.randrange(
                1000, 2000)) + ' | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)\n'
        file.write(text)
        generate_application_json_data(x+7500, False)


# Return random date between 1.1.2021 and 30.10.2021


def random_date():
    delta = datetime.strptime('10/30/2021 1:30 PM', '%m/%d/%Y %I:%M %p') - \
        datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p') + timedelta(seconds=random_second)


# JavaScript Object Notation: application/json - data
#	Object
#		Member Key: 'email'
#			Sring: 'test.test.fi'
#			Key: 'email'
#		Memeber Key: 'password'
#			String: 'salasana'
#			Key: 'password'


def generate_application_json_data(index, bool):
    login_data = generate_valid_email()
    if bool:
        email = login_data[0]
        password = login_data[1]
    else:
        email = login_data[0]
        password = generate_random_string()

    data = {}
    data['JavaScript Object Notation: application/json'] = []
    data['JavaScript Object Notation: application/json'].append({
        'Object ' + str(index): {
            'Member Key:': {
                'email': {
                    'String': email,
                    'Key': 'email'
                },
                'password': {
                    'String': password,
                    'Key': 'password'
                }
            }
        }
    })
    with jsonlines.open('data.json', 'a') as json_file:
        json_file.write(data)
        json_file.close()

    # Json tiedoston lukeminen:
    # with jsonlines.open('data.json') as json_file:
    #   for obj in json_file:
    #       print(obj)


emails = ['aku.ankka@comppanyx.fi', 'minni.hiiri@comppanyx.fi', 'roope.ankka@comppanyx.fi', 'hessu.hopo@comppanyx.fi', 'milla.magia@comppanyx.fi',
          'tupu.ankka@comppanyx.fi', 'lupu.ankka@comppanyx.fi', 'hupu.ankka@comppanyx.fi', 'it@comppanyx.fi', 'support@comppanyx.fi', 'asiakaspalvelu@comppanyx.fi']
passwords = {'aku.ankka@comppanyx.fi': 'aku', 'minni.hiiri@comppanyx.fi': 'minni', 'roope.ankka@comppanyx.fi': 'roope', 'hessu.hopo@comppanyx.fi': 'hessu', 'milla.magia@comppanyx.fi': 'milla',
             'tupu.ankka@comppanyx.fi': 'tupu', 'lupu.ankka@comppanyx.fi': 'lupu', 'hupu.ankka@comppanyx.fi': 'hupu', 'it@comppanyx.fi': 'it', 'support@comppanyx.fi': 'support', 'asiakaspalvelu@comppanyx.fi': 'aspa'}
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']

# Generoi sähköpostiosoitteita ankkalinnalaisista tms. jotka ovat yrityksen työntekijöitä


def generate_valid_email():
    data = []
    data.append(emails[randrange(11)])
    data.append(passwords[data[0]])
    return data
    # kävisikö myös return random.sample(email, 1)[0]


# Generoi random merkkijonon jota voidaan käyttää sekä sähköpostiin, että salasanaan
def generate_random_string():
    string = ''
    for _ in range(7):
        letter = random.sample(letters, 1)[0]
        string += letter

    return string

# Generates random ip which is inside of set range


def random_ip_INRANGE(ip_range):
    ip = ip_range
    ip += '.'.join('%s' % random.randint(0, 255) for i in range(1))
    return ip

# Generates totally random ip address


def random_ip_NOTINRANGE():
    ip = '.'.join('%s' % random.randint(0, 255) for i in range(4))
    return ip


def execute_anomalydatageneration(outputfile):
    with open(outputfile, 'r') as file:
        first_line = file.readline()
        for last_line in file:
            pass
        index_of_the_data = int(last_line.split('|')[0].strip())+1
    file.close()
    with open(outputfile, 'a') as file:
        generate_anomaly_data(file, index_of_the_data)
    file.close()


# Entry method to generate file
# Testi tiedosto = data.txt
# Testi iprange = '192.168.'


def execute_validdatageneration(outputfile, iprange):
    file = open(outputfile, 'w')
    generate_valid_data_IPRANGE(file, iprange)
    generate_valid_data_WIDEIP(file)
    file.close()

# Entry method to check arguments


def main(argv):
    outputfile = ''
    ip_range = ''
    method = ''

    try:
        opts, args = getopt.getopt(
            argv, "h:m:o:i:", ["help=", "method=", "ofile=", "iprange="])
    except getopt.GetoptError:
        print('Message: Error')
        print()
        print('     -o  | --ofile       Name of file where data will be generated\n     -i | --iprange     Range of ips valid data will be generated along side of randomised ips data')
        print(
            "     -m  | --method      Method to be used. Different options are 'base' and 'anomalydata'. If not selected script generates base data. -m['base'/'anomalydata'] | --method['base'/'anomalydata']")
        print()
        print('Example line: test.py -m <method> -o <outputfile> -ip <iprange>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-i", "--iprange"):
            if(len(arg) < 10):
                print('IP range length is too small')
            elif(len(arg) > 10):
                print('IP range length is too large')
            else:
                ip_range = arg
        elif opt in ("-m", "--method"):
            method = arg
    if(outputfile != '' and ip_range != '' and method == 'base'):
        execute_validdatageneration(outputfile, ip_range)
    elif(outputfile != '' and method == 'anomalydata'):
        execute_anomalydatageneration(outputfile)
    else:
        print('Message: Argument missing.')
        print()
        print('     -o  | --ofile       Name of file where data will be generated\n     -i | --iprange     Range of ips valid data will be generated along side of randomised ips data')
        print(
            "     -m  | --method      Method to be used. Different options are 'base' and 'anomalydata'. If not selected script generates base data. -m['base'/'anomalydata'] | --method['base'/'anomalydata']")
        print()
        print('Example line: test.py -m <method> -o <outputfile> -ip <iprange>')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
