import numpy
#import SciPy
#import joblib
#import threadpoolctl
#import scikit
import sys
import getopt

# Execute script and spot anomaly


def execute(dataFile, jsonFile):
    print(dataFile)
    print(jsonFile)

# Entry method to check arguments


def main(argv):
    dataFile = ''
    jsonFile = ''
    print(argv)

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

    print(dataFile)
    print(jsonFile)
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


if __name__ == "__main__":
    print(len(sys.argv))
    main(sys.argv[1:])
