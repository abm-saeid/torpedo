# Torpedo

This is a python package that helps you to send campaign mails easily using your preferred SMTP Server.

## Setup and Other Information

* This project currently works properly and can deliver approximately 40 emails (with an 80KB image attachment) a minute and 70 emails (without attachment) a minute. Tested on a remote AWS Server and Google SMTP has been used for it.
* The package is not yet on PyPi and setup files are not prepared. You have to download the `mailtorpedo` folder and place it with the python files you will be using to send. Putting the `mailtorpedo` folder inside the `<pythonpath/venv>\Lib\site-packages` also works.
* Check `examples\example.py` for an example. It's pretty much self-explanatory.