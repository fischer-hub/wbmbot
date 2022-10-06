import sys, time, datetime, hashlib, yaml, os.path
from src import utils
import re

class User:
    def __init__(self):
        self.first_name = ''
        self.last_name  = ''
        self.street     = ''
        self.zip_code   = ''
        self.city       = ''
        self.email      = ''
        self.phone      = ''
        self.wbs        = False
        self.wbs_date   = ''
        self.wbs_rooms  = ''
        self.filter     = ''

    def parse_config_file(self, config_file_path):
        with open(config_file_path, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)

                self.first_name = config['first_name']
                self.last_name  = config['last_name']
                self.street     = config['street']
                self.zip_code   = config['zip_code']
                self.city       = config['city']
                self.email      = config['email'].split(',')
                self.phone      = config['phone']
                self.wbs        = True if 'yes' in config['wbs'] else False
                self.wbs_date   = config['wbs_date'].replace('/', '')
                self.wbs_rooms  = config['wbs_rooms']
                self.filter     = config['filter'].split(',')
                
                if '100' in config['wbs_num']:
                    self.wbs_num  = 'WBS 100'
                elif '140' in config['wbs_num']:
                    self.wbs_num  = 'WBS 140'
                elif '160' in config['wbs_num']:
                    self.wbs_num  = 'WBS 160'
                elif '180' in config['wbs_num']:
                    self.wbs_num  = 'WBS 180'
                else:
                    self.wbs_num  = ''
            except yaml.YAMLError as exc:
                print(f"[{utils.date()}] Error opening config file! ")
    
    def parse_user_input(self, user_input_ls):
        if user_input_ls[0] and user_input_ls[1] and user_input_ls[5]:
            self.first_name = user_input_ls[0]
            self.last_name  = user_input_ls[1]
            self.street     = user_input_ls[2]
            self.zip_code   = user_input_ls[3]
            self.city       = user_input_ls[4]
            self.email      = user_input_ls[5]
            self.phone      = user_input_ls[6]
            self.wbs        = True if user_input_ls[7] else False
            self.wbs_date   = user_input_ls[8]
            self.wbs_rooms  = user_input_ls[9]
            self.filter     = user_input_ls[10]
        else:
            print(f"[{utils.date()}] Please fill out at least all red fields! ")
    
    def check(self):
        if self.zip_code and not self.zip_code.isdigit(): return 'Zip code contains non numerical character!'
        if self.phone and not self.phone.isdigit(): return 'Phone number contains non numerical character!'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email): return 'Email address is not valid!'
