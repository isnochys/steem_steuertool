# SST: STEEM SteuerTool
## STEEM Steuertool / Tax tool for STEEM
Mit diesem Tool kann eine Auflistung aller Eimkünfte aus der STEEM Blockchain erstellt werden, Ausgabe ist das csv Format zur weiteren Verarbeitung in einer Steuersoftware oder Tabellenkalulationsprogramm.

This tool helps for the german tax law, mostly interesting for German STEEM users

## Requirements
Python 3.6 mit steem-python installiert

Python 3.6 with steem-python installed

## Installation
Verzeichnis für SST und virtuelle Pythonumgebung erstellen 

Create create a directory for gtw and a virtual environment for Python

``mkdir sst&&cd sst``

``python -m venv env``

Source it

``source env/bin/activate``

Install steem-python

``pip install steem-python``

Clone the repository

``git clone https://github.com/isnochys/steem_steuertool.git``

## Usage
Before first use, you have to edit the following line in steuertool.py:

``username = 'isnochys'``

Change it to our steem username, save it and run it with

``(env)$ python steuertool.py``
