# Koneoppimismenetelm├Ąt - KYBS3050

## Explanation

This section includes my toughts on the assigment and how did i manage to do. More details on how to install and use the scripts you can find from Installation and Usage parts of this file.

### Data

In this scirpt data will be generated to mimic HTTP POST Request made on websites Login page. Way the data looks and feels is like in a real enviroment. Alltough all the ip addresses used are not real ip addresses so we cant use real world ip address detect libraries. But as i have explained and higlighted in the code it can be achieved. This way there is possibilities to get even more features of ip addresses. 

In the datageneration script data generated is splitted in to the 4 groups. Three of the groups are created in "base" -method. Those 3 groups of data contain:

  1. Data where ip range is inside of the companys (given as argument) whitelisted like ips. In this data group all the log in's are valid ones.
  2. Data where ip's are randomized, but actions done are some what valid and therefore flagged as normal behavior. This mimic remote accessees (home office,     
     business trip etc.). In this data group log in passwords might be incorrect, but they can been seen as failed log ins, not intrusion.
  3. Anomaly or close to anomaly. Ip's are from countries or behavior is somewhat intrusive or fishy. There can be too large payloads, fishy ip's and multiple    
     failed logins in a small period of time.

Fourt group of data is made with "anomalydata" -method. This group of data contains only anomaly behavior. In theree ip's are from blacklisted ip's or from fishy countries (countries where company's employees should not be accessing to the website). Payloads are huge (comparing normal behavior), headers can be temperatured and other kind of anomaly including behaviors.

When data is created its allways added to the same files script makes. Script makes two files, which are .txt file for the header and content of the HTTP POST request and .json file which contains log in information. Normally log in information will be found insede HTTP POST reaquest.

### Data processing

Data is processed in a way that different features of the HTTP POST reaquest are found. These features are then calculated by weighted average to give points to each data entry. Other things there will be higlighted are point's gathered from ip. This feature is processed by machine learning algorithm which calculates occurance of each ip -address and adjusting ip scores of different ip ranges. For and example if there is a lot of log in's from Sweden, algorithm concludes that those ip's from Sweden are trusted. By using real ip's this could be pinged in smaler scale to detect part of the town in different countries, network service provider, public vs private network etc. This way algorithm could be trained to detect and follow different features of the ip's and with those finding adjust score system to detect better ip's that are normal behavior vs. fishy behavior.

Third main feature im calculating is log in points. Log in points include time of login (which is also machine learning based) and success vs unsuccess log in's. From the time of log in is most dominant feature. With this feature can algorithm be trained to detect different users/ip's on what are they trends to log in. For an example someone could log in mostly night time because they like to work that period of time.

#### Clustering

Processed data is clustured by the ip-ranges and exact ip's so that time occurances and other features can be cross referenced and analysed. This way algrotihm can better detect trends in different ips, and different ip ranges.

#### Classification

Data is classified by it features. Each data entry can also get anomlay flag (anomaly == True) and then it can be straightly classified as anomaly without futher analysis. One example of this is if the ip address is in the blocklist. I tried to classifie the data as a whole by its features, and as individual feature by it self.

#### Analysis

I think data prosessing i have done is working really well and it surely can detect anomaly like behavior. Alltough its working mostly as rule based machine learning algorithm, it have machine learning features and with valid ip data and fine tuning it could be implemented as more dominant machine learning algorithm including in depth user analysis and behavioral analysis.

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


You can generate data by running the script on commandline. Script takes 2 to 3 parameters. 

<b>Required:</b> Name of file as String where data will be generated
  -o['testifile.txt'] | --ofile['testifile.txt'] 
  
<b>Required:</b> Range of ips valid data will be generated along side of randomised ips data. Range of ip means first 3 address spaces between 0 and 255
  -i[192.168.0.] | --iprange[192.168.0.]
  
<b>Optional:</b> Method to be used. Different options are "base" and "anomalydata"'. If not selected script generates base data. 
  -m['base'/'anomalydata'] | --method['base'/'anomalydata']

<b>Example line for valid data generation:</b>
```
python3 DataGeneration.py -m 'base' -o 'example.txt' -i '192.168.0.'
```

<b>Example line for anomaly data generation:</b>
```
python3 DataGeneration.py -m 'anomalydata' -o 'example.txt'
```

<b>NOTE! Anomalydata generation dosent need ip range</b>

#### Optimal usage of the script:

First generate file with base data:
```
python3 DataGeneration.py -m 'base' -o 'example.txt' -i '192.168.0.'
```
Then generate anomaly data into the same file
```
python3 DataGeneration.py -m 'anomalydata' -o 'example.txt'
```

Output will be data.json file which holds login data and .txt file which hold's in request data.

## Spot Anomaly

SpotAnomaly script is used to process the files containing data, formatting data into the more machine readable format and plotting data into the figure.

### How does it work

SpotAnomaly script runs in 3 steps: 

1. Processing lines and formatting data,
2. Generating outputfile from formatted data,
3. Drawing figure

#### Processing lines and formatting data

##### Data lines

Goes trough each line of data and calculates points for each feature on the line. 

Features script calculates are:

1. Time - Is the request made during the business hours or outside of it. If inside business hours this feature gets 1.0 as the value. If outside the range value is decreased on how far from the business hours it is down to 0.15 points.

2. Source Ip - Which ip is the request made from. If is made from Ip range set in arguments this feature gets value of 1.0. If Ip belongs to blacklisted ip's (if set in arguments) this feature gets value of 0.0. Other vice it's calculated by the predefined countries ip ranges. This feature is calculated from the first ip space on the ip addresses. This way is not optimal, but it gives clear feeling how this could work, and work even better with proper librarys and valid ip's. <b>NOTE! These could be done with ipinfo (https://github.com/ipinfo/python) library if script would use real ips.</b>

Predifend countries with predifened values:

Australia(ips: 1-30) - 0.700000
Russia(ips: 31-60) - 0.300000
Pakistan(ips: 61-90) - 0.500000
Intia(ips: 91-120) - 0.700000
Israel(ips: 121-150) - 0.300000
China(ips: 151-180) - 0.300000
Finland(ips: 180-) - 0.900000

These predifened ip values by countries are tweak by the occurance of ip ranges. More ips's in the set range are occured better default points it gets. 

3. Size - If size is smaller than 3000 it gets value of 1.0, else if its 3000 or bigger and smaller than 5000 it gets value of 0.5, and if its bigger than 5000 it gets value of 0.

4. Method - Method can be eather 1.0 or 0.0. Its determinated by waether method is exact with the default method (POST /api/example/login/?venue=dms HTTP/1.1 (application/json)) if not it gets 0.0, because it should always be exact with the default.

5. Average - Weighted average from all feature values. It uses <b>numpy</b> method average(). Weightning:

```
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
```
Index 0 is time, Index 1 is Source Ip, Index 2 is Size and index 3 is Method. Which means that if the size feature is closer to the 0.0 it weights size more (=dominand trait). Also if the method points are other than 1.0 it gets weight value of 4 (=dominand trait).

##### JSON lines

When data lines are processed and formatted script goes trough JSON file. If the login related data line belongs to Ip range and login is success valu of login feature is set to 1.0. If the login related data line belongs to Ip range and login is not success valu of login feature is set to 0.8 Other difference outcoms are:

  Finland - Success: 0.8 and Not Success: 0.6
  Bad ip adress (ip feature points < 0) - Success: 0 and Not Success: 0.1
  Ip from world (ip feature points < 0.5) - Success: 0 (if feature points are really small) or (ip feature points) * 0.5 and Not Success: (ip feature points) * (ip feature points)
  
 This feature and valu is added to the same line with other data

##### Grouping data

After all data is processed lines will be grouped by ip's. When data is grouped by ip's script checks what is the occurance of the logins from the various ip's. If there is more than 3 logins from the same ip and they are all inside of 1 minute its flagged as anomaly (True) otherwise its normal log in behavior (False).

Example of the line generated in the script:

```
{'Id': '147.60.76.170', 'time': '2021.10.03-03:29:05', 'time_points': 0.25, 'Country_flag': 'ISR', 'ip': 0.30649299999982627, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.0939379590488935, 'Time_anomaly': 'False'}
```

### Usage

SpotAnomaly script takes 2 arguments and you can run it from the commandline.

<b>Required:</b> Name of file as String where request data is
  -d[testifile.txt] | --dataFile['testifile.txt'] 
  
<b>Required:</b> Name of file as String where login data is
  -j[testi.json] | --jsonFile[testi.json]

<b>Required:</b> Range of ips valid data will be generated along side of randomised ips data. Range of ip means first 3 address spaces between 0 and 255
  -i[192.168.0.] | --iprange[192.168.0.]
  
<b>Optional:</b> Black listed ips seperated with semicolon(;). Accepts only digits
  -b[255;244;249;230] | --blacklist[255;244;249;230]

<b>Example line for valid usage:</b>
```
python3 SpotAnomaly.py -d 'testi.txt' -j 'testi.json' -i '192.168.0.'
```

<b>Example line for valid usage with blacklist parameter:</b>
```
python3 SpotAnomaly.py -d 'testi.txt' -j 'testi.json' -i '192.168.0.' -b '255;244;249;230'
```

<b>NOTE! IP RANGE SHOULD BE SAME AS USED IN DATA GENERATION</b>

Output will generate result.txt file containing all the processed data on inlines and figure.

Example of data in the outputfile:

```
'233.173.185.48': [{'Id': '233.173.185.48', 'time': '2021.02.01-16:22:29', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.6, 'Time_anomaly': 'False'}], 

'115.84.250.26': [{'Id': '115.84.250.26', 'time': '2021.07.25-13:08:10', 'time_points': 1.0, 'Country_flag': 'INT', 'ip': 0.6906259999997304, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.4769642718756276, 'Time_anomaly': 'False'}], 

'192.168.0.170': [{'Id': '192.168.0.170', 'time': '2021.04.17-19:49:58', 'time_points': 0.6, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.09.07-07:15:09', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.01.09-11:52:10', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.07.27-06:27:03', 'time_points': 0.5, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.01.26-02:00:47', 'time_points': 0.15, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.08.02-18:28:52', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.10.05-07:51:27', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.05.07-08:09:01', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.08.19-16:55:59', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.03.28-13:13:24', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.10.02-01:51:27', 'time_points': 0.05, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.02.23-01:56:14', 'time_points': 0.05, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.09.20-16:52:04', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.09.03-19:21:30', 'time_points': 0.6, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.01.29-05:11:29', 'time_points': 0.4, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.09.01-06:52:21', 'time_points': 0.5, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.04.14-16:35:04', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.04.11-14:56:48', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.08.12-12:23:32', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.08.04-16:04:51', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.03.03-22:30:34', 'time_points': 0.3, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.09.28-20:43:04', 'time_points': 0.55, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.05.09-11:45:23', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.04.15-03:31:07', 'time_points': 0.25, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.01.13-07:31:20', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.170', 'time': '2021.05.23-13:54:45', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8}, {'Id': '192.168.0.170', 'time': '2021.09.23-07:03:58', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8}],

'192.168.0.229':[{'Id': '192.168.0.229', 'time': '2021.09.08-09:08:34', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.10.05-06:48:34', 'time_points': 0.5, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.05.11-20:24:37', 'time_points': 0.55, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.06.07-08:00:11', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.07.07-00:41:46', 'time_points': 0.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.08.18-07:03:40', 'time_points': 0.7, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.08.14-11:11:27', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.10.23-04:43:17', 'time_points': 0.35, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.06.16-04:41:34', 'time_points': 0.35, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.01.12-22:48:33', 'time_points': 0.3, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.4, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.10.08-09:22:07', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8, 'Time_anomaly': 'False'}, {'Id': '192.168.0.229', 'time': '2021.08.14-11:36:50', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8}, {'Id': '192.168.0.229', 'time': '2021.06.22-11:17:58', 'time_points': 1.0, 'Country_flag': 'SUO', 'ip': 0.9, 'size': 1.0, 'method': 1.0, 'average': 0.8, 'logIn': 0.8}]}
```

#### Figure

After the data is formatted and .txt file is created script draws 3D figure of the data. Figure will have 3 different features:

1. Datapoints inside of the Ip range - drawn with blue
2. Datapoints outside of the Ip range, but not marked as anomaly - drawn with green
3. Datapoints marked as anomaly - drawn with red, having * as marker and size is bigger than other datapoints

Example figure:

![Na╠łytto╠łkuva 2021-11-11 kello 14 26 44](https://user-images.githubusercontent.com/77785795/141302646-667caaac-dc9d-4f1a-8745-d8fad31f3435.png)

Example figure 2:

<img width="1201" alt="Na╠łytto╠łkuva 2021-12-2 kello 19 22 00" src="https://user-images.githubusercontent.com/77785795/144471960-2660a530-d1c2-4ee4-98e8-ea997906de82.png">


## Scripts evaluation

I used Minimial learning machine training to evaluate how the script works. My goal was to evaluate if my SpotAnomaly script features and calculates were in line with the Machine Learning algorithms used in Minimal learning machine -algorithm. 

MLM explained by the teacher:
```
The minimall learning machine consists in building a linear mapping between input and output distance matrices. In the generalization phase, the learned distance map is used to provide an estimate of the distance from output reference points to the unknown target output value. Then, the output estimation is formulated as multilateration problem based on the predicted output distance and the locations of the reference points. 

The MLM is a two-step method designed to
  1. reconstructing the mapping existing between input and output distances;estimating the 
  2. response from the configuration of the output points.
```

### Usage
  
MachineLearning script takes one argument and you can run it from the commandline.

<b>Required:</b> Name of file as String where data is
  -i[result.txt] | --ifile['result.txt'] 

<b>Example line for valid usage:</b>
```
python3 MachineLearning.py -i 'result.txt'  
```

<b>NOTE! File need to be created with SpotAnomaly script</b>


### How does it work

MachineLearning script process the data in the file into the 2 numpy arrays. First one will be averages which is used to create base for the findings. Second one is for the MLM algorithm to prosess. It contains 2D numpy array where each row is dataset containing 5 different features (in columns): time_points-, ip-, size-, method- and logIn -points generated by the SpotAnomaly script. NOTE! Both numpy arrays will only contain those dataset's where is only 1 unique ip entry (=excluding ip range data entries).

Then data will be normalised and shaped and it will be passed to the training. Then training data will be classified without optimization. 

After all the training and testing 4 figures will be created. First 2 will contain averages data to terminated weather MLM can match with the shape/line of it. Second 2 will containt trained and classified data containing all the detected features.


### Findings
  
MLM matched quite well with the SpotAnomaly detection. It was able to get similiar or at least same inline conclusions than SpotAnomaly script did. On side note, one of the reason for that might be that the data was pre-prosessed in SpotAnomaly script. 

Hardest part was to tune MLM to work in the use case and be able to fit the data in it. This is shown especially with the average data, because it has only one dimension (1D). Therefore it was hard to normalize all the data to fit in to the model.  Second hardes part was setting up parameters/features to get indendent results out of the algorithm. 

I think i was able to tackle both challenges quite well because results were so well in line with the SpotAnomaly results.

One think i could have done better was creting more samelike figures to emphesise even better similarities in the results.
  
Result figure:

<img width="1316" alt="Na╠łytto╠łkuva 2021-12-8 kello 12 05 36" src="https://user-images.githubusercontent.com/77785795/145189371-5fb1b613-c8ff-4d4d-aa7e-161b07a95a99.png">


