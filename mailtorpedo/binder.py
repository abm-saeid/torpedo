from .reader import CSVReader
from .template import Template, SnippetParsingError

from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
#from email.mime.application import MIMEApplication

from csv import DictReader
import re

class Binder():
    def __init__(self, reader: CSVReader, template: Template):
        self.reader = reader
        self.template = template
        self.set_type()

    def set_type(self):
        for snippet in self.template.snippets:
            if snippet.type in ('plain', 'html'):
                self.reader.check_template(snippet)
        
        if self.reader.is_required():
            self.type = 'solo' #for individually modified
        else:
            self.type = 'bulk' #for unmodified

    def parse(self):
        with open(self.reader.filename, 'r', encoding = self.reader.encoding) as csvfile:
            reader = DictReader(csvfile, delimiter = self.reader.delimiter)
            for row in reader:
                for snippet in self.template.snippets:
                    if snippet.type in ('plain', 'html'):
                        for header in self.reader.headers:
                            snippet.content = re.sub(f'\${{ {header} }}', row[header], snippet.content)
            
                mime = MIMEMultipart()
                for snippet in self.template.snippets:
                    if snippet.type == 'plain':
                        content = MIMEText(snippet.content, 'plain')
                    elif snippet.type == 'html':
                        content = MIMEText(snippet.content, 'html')
                    elif snippet.type == 'image':
                        with open(snippet.content, 'rb') as img:
                            content = MIMEImage(img.read())
                            content.add_header('Content-Disposition', 'attachment', filename = snippet.content.split('/')[-1])
                    elif snippet.type == 'audio':
                        with open(snippet.content, 'rb') as audio:
                            content = MIMEAudio(audio.read())
                            content.add_header('Content-Disposition', 'attachment', filename = snippet.content.split('/')[-1])
                    else:
                        raise SnippetParsingError("Snippet unidentified")

                    mime.attach(content)
                    mime['Subject'] = self.template.subject
                    mime['To'] = row[self.reader.email_field]
                
                yield (row[self.reader.email_field], mime)