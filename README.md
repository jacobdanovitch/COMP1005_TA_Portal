# COMP1005 TA Portal

(help wanted!)

## Description

A small marking portal for TAs. Upload a zipped file with the student's name and number, containing the student's `.py` files.
The files will be run with pre-defined test-cases, and you can enter your marks to produce an HTML table that can be pasted directly into CULearn.

## Setup

To build:
```bash
git clone https://github.com/jacobdanovitch/COMP1005_TA_Portal.git
cd COMP1005_TA_Portal
pip install -r requirements.txt
```

To run in development mode on Windows:
```bash
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```
Use "export" in place of "set" on Linux.
