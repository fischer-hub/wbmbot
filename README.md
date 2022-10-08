# GUI (EXPERIMENTAL)
START GUI WITH 
```
./wbmbot.py
```
This does not interact with the bot yet!!

# WBMBOT
A simple selenium based python bot to check the website of WBM Wohnungsbaugesellschaft Berlin-Mitte mbH for new flats and automatically apply for them, since only the first 1000 applicants will be considered in the random selection process for apartment viewing.

# Getting started

## Running the packaged version
The usage of the packaged version of the wbmbot is pretty simple, just download the package version for your operating system and open the program like anyother desktop application.

## Running the source code directly
If you want to run the project on your own you first have to clone the repository and install the necessary dependencies. Clone the repository and change to the project directory by running the following command in your terminal:

```
# clone the repository
git clone https://github.com/fischer-hub/wbmbot.git

# change to project directory
cd wbmbot
```

To install all dependencies you can either use the python index package index [`pip`](https://pypi.org/) or the [`conda`](https://docs.conda.io/en/latest/) package manager. (Or install everything manually if you insist on it...)

### Pip
If you want to use the `python package index` install the requirements define in the `requirements.txt` file located in the project directory as follows:
```
pip install -r requirements.txt
```

### Conda
If you want to use the `conda` package manager, create an environment from the `environment.yaml` file located in the project directory as follows:
```
# create conda environment form environment file
conda env create -f environment.yaml

# activate conda environment
conda activate wbmbot
```

# Start the wbmbot

To start the bot with its GUI simply run the below command in your terminal in the project directory:
```
python3 wbmbot.py
```

To start the bot in command line mode run the below command in your terminal in the project directory:
```
python3 wbmbot.py -c
```

If you are running the bot in command line mode for the first time the bot will start the setup process asking all the necessary information for applications on wbm.de.
Note that these informations will be saved unencrypted to a local `config.yaml` file in *human readable* format!!
If you don't want to use the setup process for this, you can just create a `config.yaml` file yourself in the project directory of format:

```
city: "cityname"
email: "email@adress1,email@adress2,..."
first_name: "Max"
filter: "keyword1,keyword2,..."
last_name: "Mustermann"
phone: "0123456789"
street: "Streetname 42"
wbs: "yes"
wbs_date: "23/04/1972"
wbs_num: "WBS 160"
wbs_rooms: '2'
zip_code: '12345'
```

# Parameters
```
usage: wbmbot.py [-h] [-c] [-t] [-H] [-i INTERVAL] [-l LATENCY_WAIT] [-y YAML] [-o LOG]

optional arguments:
  -h, --help            Show this help message and exit.
  -c, --cli             If set, run bot on command line only instead of starting the GUI.
  -H, --headless_off    If set, turn off headless run. The bot will run in the opened browser.
  -t, --test            If set, run test-run on the test data. This does not actually connect to wbm.de.
  -i, --interval        Set the time interval in minutes to check for new flats on wbm.de. [default: 5]
  -l  --latency_wait    Set time to wait after interaction with website. Slow connections might need a higher latency-wait-time. [default: 1.5s]
  -y  --yaml            Provide configuration file name to load config from.[default: 'config.yaml']
  -o  --log             Provide log file name to write log data to. [default: 'log.txt']
```

# Filtering
Currently the bot will apply to all available flats on the WBM website, which most of the time is only like one per every 3 days anyway..
However a filtering feature is planned and will (probably) be implemented soon.

# Additional
The bot will save all successfull applications to a `log.txt` file. This file is also used to apply to every flat only once, so don't delete it unless you want to reapply to all available flats!
During the setupt process you will be able to submit multiple email adresses. The bot will then apply for every flat with your user data once per email adress.
Per default wbm.de will be reloaded and checked for new flats every 5 minutes. There currently is no timeout or bot check / captcha on the website (lets hope it stays like this), but I dont think its necessary to check more often, as there are not many flats available anyway (in contrast to e.g. immoscout24).

Let the hunt begin! Good luck!
