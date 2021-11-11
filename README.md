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

### SciPy, Matplotlib, IPython, Jupyter, Pandas, Sympy, Nose & Numpy
```
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```

## Data generator

Data generator is used to generate data for the Anomaly spotting script. Data will be training data so it will look like a real Login HTTP request but it's not real data.

### How does it work

DataGeneration script takes 2-3 arguments. With arguments user determinates which kind of data will be generated (Anomaly data or Valid data). However there can be anomalies in the valid data as well. Script adds both runs intothe same data.json file. Both generates 10000 lines of data. 

On normal data scenario script makes 7500 lines of data where ip range argument is base and ip space is randomly generated trough 255 different possibilities. 2500 lines of data will be generated with random ip addresses. 

#### Request file

Datas format is: Id/index | time | Source Ip | Destination ip | Method | Package size | Reaquest header

Id/index = position or better know index of the line

Time = randomly generated time the request have been made

Source Ip = Randomly generated ip address (not real/valid ip) which has eather set ip range as first 3 ip spaces and 1 randomly generated (between 0 and 255) or  all 4 spaces are randomly generated (between 0 and 255).

Destination Ip = Static value

Method = Static value

Package size = Randomly generated value between 1000 and 2000

Reaques header = Static value


Example of the output data:

```
6538 | 2021.04.10 - 02:46:26 | 198.168.0.82 | 10.0.0.1 | HTTP | 1583 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6539 | 2021.10.27 - 19:33:47 | 198.168.0.29 | 10.0.0.1 | HTTP | 1115 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6540 | 2021.05.30 - 06:03:33 | 198.168.0.192 | 10.0.0.1 | HTTP | 1334 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6541 | 2021.05.25 - 03:14:22 | 198.168.0.234 | 10.0.0.1 | HTTP | 1846 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6542 | 2021.08.23 - 08:14:17 | 198.168.0.194 | 10.0.0.1 | HTTP | 1723 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6543 | 2021.01.12 - 20:03:09 | 198.168.0.177 | 10.0.0.1 | HTTP | 1549 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6544 | 2021.02.09 - 17:39:13 | 198.168.0.190 | 10.0.0.1 | HTTP | 1748 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
6545 | 2021.07.15 - 15:15:07 | 241.42.190.54 | 10.0.0.1 | HTTP | 1376 | POST /api/example/login/?venue=dms HTTP/1.1 (application/json)
```

#### Data file

Data file is also generated trough the process and it containts request headers body (POST /api/example/login/?venue=dms HTTP/1.1 (application/json)). This body
includes username and password put into the JSON format.

Login's in the datafile are eather valid logins or invalid. 

In the script there is set of "Company" (valid) emails.

```
'aku.ankka@comppanyx.fi', 'minni.hiiri@comppanyx.fi', 'roope.ankka@comppanyx.fi', 'hessu.hopo@comppanyx.fi', 'milla.magia@comppanyx.fi', 'tupu.ankka@comppanyx.fi', 'lupu.ankka@comppanyx.fi', 'hupu.ankka@comppanyx.fi', 'it@comppanyx.fi', 'support@comppanyx.fi', 'asiakaspalvelu@comppanyx.fi'
```

These emails are set randomly to each login data.

There is also set of valid password for the each email and these are asigned to the valid logins.

```
'aku.ankka@comppanyx.fi': 'aku', 'minni.hiiri@comppanyx.fi': 'minni', 'roope.ankka@comppanyx.fi': 'roope', 'hessu.hopo@comppanyx.fi': 'hessu', 'milla.magia@comppanyx.fi': 'milla','tupu.ankka@comppanyx.fi': 'tupu', 'lupu.ankka@comppanyx.fi': 'lupu', 'hupu.ankka@comppanyx.fi': 'hupu', 'it@comppanyx.fi': 'it', 'support@comppanyx.fi': 'support', 'asiakaspalvelu@comppanyx.fi': 'aspa'
```

In invalid logins script generates random password with 7 letters long.

Example of the output data:

```
{"JavaScript Object Notation: application/json": [{"Object 303": {"Member Key:": {"email": {"String": "asiakaspalvelu@comppanyx.fi", "Key": "email"}, "password": {"String": "aspa", "Key": "password"}}}}]}
{"JavaScript Object Notation: application/json": [{"Object 304": {"Member Key:": {"email": {"String": "hessu.hopo@comppanyx.fi", "Key": "email"}, "password": {"String": "hessu", "Key": "password"}}}}]}
{"JavaScript Object Notation: application/json": [{"Object 306": {"Member Key:": {"email": {"String": "milla.magia@comppanyx.fi", "Key": "email"}, "password": {"String": "milla", "Key": "password"}}}}]}
{"JavaScript Object Notation: application/json": [{"Object 9994": {"Member Key:": {"email": {"String": "roope.ankka@comppanyx.fi", "Key": "email"}, "password": {"String": "ecgmang", "Key": "password"}}}}]}
{"JavaScript Object Notation: application/json": [{"Object 9995": {"Member Key:": {"email": {"String": "tupu.ankka@comppanyx.fi", "Key": "email"}, "password": {"String": "tevbhqc", "Key": "password"}}}}]}

```

### Usage

#### Generate data

You can generate data by running the script on commandline. Script takes 2 to 3 parameters. 

<b>Required:</b> Name of file as String where data will be generated
  -o['filename'] | --ofile['filename'] 
  
<b>Required:</b> Range of ips valid data will be generated along side of randomised ips data. Range of ip means first 3 address spaces between 0 and 255
  -ip[192.168.0.] | --iprange[192.168.0.]
  
<b>Optional:</b> Method to be used. Different options are "base" and "anomalydata"'. If not selected script generates base data. 
  -m['base'/'anomalydata'] | --method['base'/'anomalydata']

<b>Example line for valid data generation:</b>
```
python3 DataGeneration.py -m 'base' -o 'example.txt' -ip '192.168.0.'
```

<b>Example line for anomaly data generation:</b>
```
python3 DataGeneration.py -m 'anomalydata' -o 'example.txt' -ip '192.168.0.'
```

Output will be data.json file which holds login data and .txt file which hold's in request data.
