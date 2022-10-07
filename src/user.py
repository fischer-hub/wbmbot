import yaml, re

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
        self.wbs_num    = ''


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
                self.wbs        = True if config['wbs'] else False
                self.wbs_date   = config['wbs_date'].replace('/', '')
                self.wbs_rooms  = config['wbs_rooms']
                self.filter     = config['filter'].split(',')
                
                # Necessary for CLI mode
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
                return f"Error opening config file!\n{exc}"
    

    def parse_user_input(self, user_input_ls):
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
        self.wbs_num    = user_input_ls[11]
    

    def merge(self, user):
        if not self.first_name: self.first_name = user.first_name
        if not self.last_name:  self.last_name  = user.last_name
        if not self.street:     self.street     = user.street
        if not self.zip_code:   self.zip_code   = user.zip_code
        if not self.city:       self.city       = user.city
        if not self.email:      self.email      = user.email
        if not self.phone:      self.phone      = user.phone
        if not self.wbs:        self.wbs        = user.wbs
        if not self.wbs_date:   self.wbs_date   = user.wbs_date
        if not self.wbs_rooms:  self.wbs_rooms  = user.wbs_rooms
        if not self.filter:     self.filter     = user.filter
        if not self.wbs_num:    self.wbs_num    = user.wbs_num



    def check(self):
        if not bool(self.first_name and self.last_name and self.email): return 'Please fill out at least all red fields!'
        if self.zip_code and not self.zip_code.isdigit(): return 'Zip code contains non numerical character!'
        if self.zip_code and len(self.zip_code) < 5: return 'Zip code has to be 5 digits long!'
        if self.phone and not self.phone.isdigit(): return 'Phone number contains non numerical character!'
        if not any(re.match(r"[^@]+@[^@]+\.[^@]+", email) for email in self.email): return 'Email address is not valid!'
        if (not self.wbs) and bool(self.wbs_date or self.wbs_num or self.wbs_rooms): return 'WBS data was provided but the WBS checkbox was unchecked!'
    

    def small_check(self):
        if self.zip_code and not self.zip_code.isdigit(): return 'Zip code contains non numerical character!'
        if self.zip_code and len(self.zip_code) < 5: return 'Zip code has to be 5 digits long!'
        if self.phone and not self.phone.isdigit(): return 'Phone number contains non numerical character!'
        if not any(re.match(r"[^@]+@[^@]+\.[^@]+", email) for email in self.email): return 'Email address is not valid!'
        if (not self.wbs) and bool(self.wbs_date or self.wbs_num or self.wbs_rooms): return 'WBS data was provided but the WBS checkbox was unchecked!'
