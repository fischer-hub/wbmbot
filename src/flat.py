import hashlib

class Flat:
    def __init__(self):
        flat_attr       = ''
        attr_size       = ''
        self.title      = ''
        self.district   = ''
        self.street     = ''
        self.zip_code   = ''
        self.city       = ''
        self.total_rent = ''
        self.size       = ''
        self.rooms      = ''
        self.wbs        = False
        self.hash       = ''

    def parse_flat_elem(self, flat_elem):
        flat_attr       = flat_elem.text.split('\n')
        attr_size       = len(flat_attr)
        self.title      = flat_attr[0] if attr_size > 0 else ''
        self.district   = flat_attr[4] if attr_size > 4 else ''
        self.street     = flat_attr[5] if attr_size > 5 else ''
        self.zip_code   = flat_attr[6].split(' ')[0] if attr_size > 6 else ''
        self.city       = flat_attr[6].split(' ')[1] if attr_size > 6 else ''
        self.total_rent = flat_attr[8] if attr_size > 8 else ''
        self.size       = flat_attr[10] if attr_size > 10 else ''
        self.rooms      =  flat_attr[12] if attr_size > 12 else ''
        self.wbs        = True if ('wbs' in flat_elem.text or 'WBS' in flat_elem.text) else False
        self.hash       = hashlib.sha256(flat_elem.text.encode('utf-8')).hexdigest()

    def text(self):
        flat_text = ''
        for _, value in self.__dict__.items():
            flat_text += str(value)
        return flat_text