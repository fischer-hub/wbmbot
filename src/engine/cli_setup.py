import yaml
from src import utils

def setup(config_file_path):
            data = {}
            data['first_name'] = input("Please input your first name and confirm with enter: ")
            data['last_name'] = input("Please input your last name and confirm with enter: ")
            email, email_ls, c = '', '', 1
            while 'exit' not in email:
                email = input(f"Please input email adress {c} and confirm with enter, type 'exit' to exit: ")
                email_ls += email.lower()
                email_ls += ','
                c += 1
            data['email'] = email_ls.replace(',exit,','')
            data['street'] = input("Please input your street and confirm with enter or leave empty and skip with enter: ")
            data['zip_code'] = input("Please input your zip_code and confirm with enter or leave empty and skip with enter: ")
            data['city'] = input("Please input your city and confirm with enter or leave empty and skip with enter: ")
            data['phone'] = input("Please input your phone number and confirm with enter or leave empty and skip with enter: ")
            data['wbs'] = input("Do you have a WBS (Wohnberechtigungsschein)?\nPlease type yes / no: ")
            if 'yes' in data['wbs']:
                data['wbs_date'] = input("Until when will the WBS be valid?\nPlease enter the date in format month/day/year: ")
                data['wbs_num'] = input("What WBS number (Einkommensgrenze nach Einkommensbescheinigung § 9) does your WBS show?\nPlease enter WBS 100 / WBS 140 / WBS 160 / WBS 180: ")
                data['wbs_rooms'] = input("For how many rooms is your WBS valid?\nPlease enter a number: ")
            else:
                data['wbs_date'] = ''
                data['wbs_num'] = ''
                data['wbs_rooms'] = ''
            if 'yes' in input("Do you want to enter keywords to exclude specific flats from the search results?\nPlease type yes / no: "):
                keyword, filter = '', ''
                while 'exit' not in keyword:
                    keyword = input("Please enter a keyword and confirm with enter, type 'exit' to exit: ")
                    filter += keyword.lower()
                    filter += ','
                data['filter'] = filter.replace(',exit,','')
            else:
                data['filter'] = ''

            print(f"[{utils.date()}]Done! Writing config file..")

            with open(config_file_path, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)