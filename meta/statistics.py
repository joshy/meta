import pandas as pd

Main = ['UNISPITAL BASEL, HNO', 'Universitaetsspital Basel', 'Universitaetsspital',
        'RADIOLOGIE UNI BASEL', 'BILDDIAGNOSTIK BASEL', 'Universitätsspital Basel',
        'Universitätsspial Basel', 'Universitätsspital, Radiologie, Basel', 'Universitätsspital']
Pediatric = ['UKBB', 'Kinderspital UKBB', 'Kinderspital Basel']
Geriatric = ['Felix Platter Spital', 'Felixplatter Spital']


def calculate(df):
    df = df.dropna()
    df['year'] = df.apply(lambda x: str(x['StudyDate'])[0:4], axis=1)
    df['institution_type'] = df.apply(lambda x : mapping(x['InstitutionName']), axis=1)
    return df.groupby(['year','institution_type']).agg('count').reset_index()


def mapping(input):
    test_string = input.strip()
    if test_string in Main:
        return 'Main'
    elif 'USB' in test_string:
        return 'Main'
    elif 'UKBB' in test_string:
        return 'Pediatric'
    elif 'Universitaetsspital' and 'Basel' in test_string:
        return 'Main'
    elif test_string in Pediatric:
        return 'Pediatric'
    elif test_string in Geriatric:
        return 'Geriatric'
    else:
        return 'Extern'