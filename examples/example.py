from time import perf_counter
import os

# Go to https://accounts.google.com/DisplayUnlockCaptcha and unblock you email, also enable less secure app access before using gmail

from mailtorpedo.reader import CSVReader
from mailtorpedo.template import Snippet, Template
from mailtorpedo.sender import Sender

this_dir = os.path.dirname(__file__) #absolute path of the current directory

reader = CSVReader(os.path.join(this_dir, 'test.csv'), email_field='email') # Initiate CSVReader with the CSV file path and email field title inside
template = Template('Test Email for You') # Initiate Template with email subject
snippet1 = Snippet("""
name,id,email,rank,username,password
Dear ${ name },

Hope you are well. Your rank has been updated to ${ rank }.

ID: ${ id }
Username: ${ username }

Thank you
""") # Initiate Snippet with the mail body
snippet2 = Snippet(os.path.join(this_dir, 'kexib.png')) # Initiate Snippet with the image file path
template.add_snippet(snippet1, snippet2) # Add snippets to 
sender = Sender(os.path.join(this_dir, 'credentials.json'), reader, template) # Initiate Sender with the json file containing credentials

sender.send()