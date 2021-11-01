# Koneoppimismenetelmät - KYBS3050

## Installation

To download Git repository use git clone command.
```
git clone https://github.com/Mus4J/machinelearning-course.git
```


## Dependences

In order to run the project you need some dependence packages

### Python3
https://www.python.org/downloads/

### Jsonline
```
pip install jsonlines
```


## Usage

### Generate data

You can generate data by running the script on commandline. Script takes 2 to 3 parameters. 

<b>Required:</b> Name of file as String where data will be generated
  -o['filename'] | --ofile['filename'] 
  
Required: Range of ips valid data will be generated along side of randomised ips data. Range of ip means first 3 address spaces between 0 and 255
  -ip[192.168.0.] | --iprange[192.168.0.]
  
Optional: Method to be used. Different options are "base" and "anomalydata"'. If not selected script generates base data. 
  -m['base'/'anomalydata'] | --method['base'/'anomalydata']

Example line:
```
python3 DataGeneration.py -m base -o 'example.txt' -ip 192.168.0.
```
