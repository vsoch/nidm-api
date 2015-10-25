#!/usr/bin/env python

'''
script.py: part of nidmapi package
Runtime executable

'''
from app import main
from glob import glob
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
    description="query and visualization api tool for nidm results, workflow, and experiments")
    parser.add_argument("ttl", help="List of comma separated ttl files to parse.", type=str)
    parser.add_argument("--port", help="PORT to use to serve nidm-api (default 8088).",default=8088,type=int)
   
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    
    #TODO: We will have logic here to serve API vs do some other functions, right now just serve API
    main(port=args.port)    

if __name__ == '__main__':
    main()
