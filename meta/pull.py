""" 
    PULL Series from PACS
    Takes parameters: StudyInstanceUID SeriesInstanceUID OutPath
    StudyInstanceUID, SeriesInstanceUID = unique identifiers
       for series stored in PACS
    OutPath= full path to directory where result should be stored.
"""
import sys
import os
import subprocess

from meta.settings import *


def download(study_instance_uid, series_instance_uid):
    cmd = BASE_COMMAND + " --output-directory " + OUTPUT_DIR + " -k StudyInstanceUID=" + study_instance_uid + " -k SeriesInstanceUID=" + series_instance_uid
    print(cmd)
    subprocess.call(cmd, shell=True)


if len(sys.argv) < 4:
    print("usage: pullFromPACS StudyInstanceUID SeriesInstanceUID OutPath")
    print("  StudyInstanceUID,SeriesInstanceUID = unique identifier of series to PULL")
    print("  OutPath = directory in which to send output")
else:
    if not os.path.exists(DCMIN):
        print(DCMIN + " does not exist!")
        exit(-1)
    StudyInstanceUID = sys.argv[1]
    SeriesInstanceUID = sys.argv[2]
    outPath = sys.argv[3]
    print(StudyInstanceUID)
    print(SeriesInstanceUID)
    if os.path.isfile(outPath):
        outPath = os.path.dirname(outPath)
    elif not os.path.exists(outPath):
        os.makedirs(outPath)
    cmd = BASE_COMMAND + " --output-directory " + outPath + " -k StudyInstanceUID=" + StudyInstanceUID + " -k SeriesInstanceUID=" + SeriesInstanceUID
    print(cmd)
    subprocess.call(cmd, shell=True)
