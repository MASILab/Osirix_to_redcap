#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys
import argparse
import logging as LOGGER

def redcap_project_access(API_KEY):
    """
    Access point to REDCap form
    :param API_KEY:string with REDCap database API_KEY
    :return: redcap Project Object
    """
    try:
        project = redcap.Project('https://redcap.vanderbilt.edu/api/', API_KEY)
    except:
        raise SystemExit('ERROR: Could not access redcap. Either wrong API_URL/API_KEY or redcap down.')
    return project

def get_form_names(project):
    """
    Fetches all form objects from the REDCap project and converts unicode values 
    to string
    :param project: redcap.Project object
    :return: list containing names of forms as string
    """
    forms_unicode = project.forms
    forms_str = []
    for form in forms_unicode:
        forms_str.append(form.encode('ascii','ignore'))
    return forms_str

def open_file(filepath):
    """
    """
    try:
        xl_file = open(filepath,"r")
        LOGGER.info("Opening xls file as txt")
        return xl_file
    except:
        raise SystemExit("ERROR: Check path and permissions of file you are trying to upload")

def add_to_parser():
    """
    Method to add arguments to default parser
    :return: parser object
    """
    parser = argparse.ArgumentParser(description='Crontabs manager')
    parser.add_argument("-k","--key",dest='API_KEY',default=None, \
                        help='API key to REDCap Database')
    parser.add_argument("-f","--file",dest='path',default=None, \
                        help = 'path of file that needs to be uploaded')
    return parser

def execute():
    """
    point of execution
    """
    LOGGER.basicConfig(level=LOGGER.DEBUG,\
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
                       datefmt='%Y-%m-%d %H:%M:%S')
    console = LOGGER.StreamHandler()
    console.setLevel(LOGGER.INFO)
    parser = add_to_parser()
    OPTIONS = parser.parse_args()
    project = redcap_project_access(OPTIONS.API_KEY)
    forms = get_form_names(project)
    doc = open_file(OPTIONS.path)

if __name__ == '__main__':
    execute()
