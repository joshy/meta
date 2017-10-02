""" Convert old json files to new json file with different structure """

import json
from os import walk
from meta.app import app

def convert_json(json_in):
    """ in: json file in old form
        out: json file in new form
    """
    my_dict = []
    flag = 0
    acc_num = []
    for entry in json_in:
        if entry['AccessionNumber'] not in acc_num:
            acc_num.append(entry['AccessionNumber'])
            if flag == 0:
                p_dict = {}
            else:
                my_dict.append(p_dict)
                p_dict = {}

            p_dict['cat'] = 'parent'
            p_dict["AccessionNumber"] = entry["AccessionNumber"]
            p_dict["InstanceAvailability"] = entry["InstanceAvailability"]
            p_dict["InstitutionName"] = entry["InstitutionName"]
            p_dict["Modality"] = entry["Modality"]
            p_dict["PatientBirthDate"] = entry["PatientBirthDate"]
            p_dict["PatientID"] = entry["PatientID"]
            p_dict["PatientName"] = entry["PatientName"]
            p_dict["PatientSex"] = entry["PatientSex"]
            p_dict["ReferringPhysicianName"] = entry["ReferringPhysicianName"]
            p_dict["SeriesDate"] = entry["SeriesDate"]
            p_dict["SpecificCharacterSet"] = entry["SpecificCharacterSet"]
            p_dict["StudyDate"] = entry["StudyDate"]
            p_dict["StudyDescription"] = entry["StudyDescription"]
            p_dict["StudyID"] = entry["StudyID"]
            p_dict["StudyInstanceUID"] = entry["StudyInstanceUID"]
            p_dict["id"] = entry["StudyInstanceUID"]
            p_dict['_childDocuments_'] = []
            p_dict = add_child(p_dict, entry)
            flag = 1
                    
        else:
            p_dict = add_child(p_dict, entry)

    return my_dict

def add_child(parent, entry):
    """ add child entry """
    child_dict = {}
    child_dict['cat'] = 'child'
    child_dict["BodyPartExamined"] = entry["BodyPartExamined"]
    child_dict["SeriesDescription"] = entry["SeriesDescription"]
    child_dict["SeriesInstanceUID"] = entry["SeriesInstanceUID"]
    child_dict["id"] = entry["SeriesInstanceUID"]
    child_dict["SeriesNumber"] = entry["SeriesNumber"]
    child_dict["SeriesTime"] = entry["SeriesTime"]
    parent['_childDocuments_'].append(child_dict)
    return parent

path_to_json_pacs = app.config['PATH_TO_JSON']
# process one month at a time
# First step: convert the original json to one with
# the needed parent-child relation
for (_, _, filenames) in walk(path_to_json_pacs):
    # one json pacs file per month
    for file in filenames:
        with open(path_to_json_pacs + file, 'r') as blu:
            print('loading ' + path_to_json_pacs + file)
            data = blu.read()
            json_in = json.loads(data)
            json_out = convert_json(json_in)
        
        name = 'new-' + file
        print('writing ', name)

        with open(name, 'w') as fp:
            json.dump(json_out, fp, indent=4)