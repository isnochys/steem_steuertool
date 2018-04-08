# SST: STEEM SteuerTool
## STEEM Steuertool / Tax tool for STEEM
Mit diesem Tool kann eine Auflistung aller Eimkünfte aus der STEEM Blockchain erstellt werden, Ausgabe ist das csv Format zur weiteren Verarbeitung in einer Steuersoftware oder Tabellenkalulationsprogramm.

This tool helps for the german tax law, mostly interesting for German STEEM users

## Requirements
Python 3.6 mit steem-python installiert oder Python 2.x, bzw. 3.x mit beem installiert

Python 3.6 with steem-python installed or Python 2.x/3.x with beem intalled

## Installation
Verzeichnis für SST und virtuelle Pythonumgebung erstellen 

Create create a directory for gtw and a virtual environment for Python

``mkdir sst&&cd sst``

``python -m venv env``

Source it

``source env/bin/activate``
### Option 1 beem
Install steem-python

``pip install beem``

Clone the repository

``git clone https://github.com/isnochys/steem_steuertool.git``

### Option 2 steem-python
Install steem-python

``pip install steem-python``

Clone the repository

``git clone https://github.com/isnochys/steem_steuertool.git``

## Usage
Before first use, you have to edit the following line in steuertool.py or beem_steuertool.py:

``username = 'isnochys'``

Change it to our steem username, save it and run it with

``(env)$ python beem_steuertool.py``

or with steem-python:

``(env)$ python steuertool.py``

The output will be a CVS file ``steuer.cvs`` in the current directory, with STEEM transaction id, timestamp, type and amount in the selected currency as values per line
