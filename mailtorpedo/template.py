from bs4 import BeautifulSoup
import pathlib

from .extras import audio_extensions, image_extensions


class SnippetParsingError(Exception):
    pass

class Template():
    def __init__(self, subject):
        self.snippets = []
        self.subject = subject
    
    def add_snippet(self, *args):
        for snippet in list(args):
            if snippet.type in ('plain', 'html'):
                if any(i.type == snippet.type for i in self.snippets):
                    raise SnippetParsingError(f"Another {snippet.type} MIMEType already present.")
            self.snippets.append(snippet)

class Snippet():
    def __init__(self, content: str):
        self.content = content
        
        if content.split('.')[-1] in image_extensions:
            self.type = 'image'
        elif content.split('.')[-1] in audio_extensions:
            self.type = 'audio'
        #elif isdir(content):
        #    self.type = 'dir'
        elif bool(BeautifulSoup(self.content, "html.parser").find()):
            self.type = 'html'
        else:
            self.type = 'plain'