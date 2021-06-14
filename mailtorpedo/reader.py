from csv import Sniffer

class CSVReader():
    def __init__(self, filename: str, email_field = 'email', encoding = 'utf-8'):
        self.filename = filename
        self.encoding = encoding
        self.required = False
        self.email_field = email_field
    
        with open(self.filename, 'r', encoding = self.encoding) as csvfile:
            topline = csvfile.readline().rstrip()
            self.delimiter = Sniffer().sniff(topline).delimiter

        headers = topline.split(self.delimiter)
        self.headers = headers


    def check_template(self, snippet):
        for header in self.headers:
            if f"${{ {header} }}" in snippet.content:
                self.required = True
                break
        else:
            return False
        
        return True
    
    def is_required(self):
        return self.required