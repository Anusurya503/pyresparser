import os
import argparse
from pprint import pprint
import io
import multiprocessing as mp
import urllib
from urllib.request import Request, urlopen
from pyresparser import ResumeParser
import json
from json2html import *


def get_remote_data():
    try:
        remote_file = 'https://www.omkarpathak.in/downloads/OmkarResume.pdf'
        print('Extracting data from: {}'.format(remote_file))
        req = Request(remote_file, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        _file = io.BytesIO(webpage)
        _file.name = remote_file.split('/')[-1]
        resume_parser = ResumeParser(_file)
        return [resume_parser.get_extracted_data()]
    except urllib.error.HTTPError:
        return 'File not found. Please provide correct URL for resume file.'

def get_local_data():
    data = ResumeParser('./CEG_CVs/CVs/AjayKundu-ResidentEngineerAhmedabad.pdf').get_extracted_data()
    return data
        
def test_remote_name():
    data = get_remote_data()
    return  data

def test_remote_phone_number():
    data = get_remote_data()
    assert data[0]['mobile_number']

def test_local_name():
    data = get_local_data()
    # assert 'Ajay kumar kundu' == data['name']
    return data

def test_local_phone_number():
    data = get_local_data()
    assert data['mobile_number']


outputData = test_local_name()
json_object = json.dumps(outputData)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
with open('sample.json') as f:
    d = json.load(f)
    scanOutput = json2html.convert(json=d)
    htmlReportFile = 'output.html'
    with open(htmlReportFile, 'w') as htmlfile:
        htmlfile.write(str(scanOutput))
        