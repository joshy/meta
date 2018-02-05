"""
DCMTK command generation.
"""
import os

TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def _get_base_command(dcmtk_config, pacs_config):
    """ Constructs the first part of a dcmtk command_creator. """
    return (
        dcmtk_config.dcmtk_bin +
        'movescu -v -S -k QueryRetrieveLevel=SERIES ' +
        '-aet {} -aec {} {} {} +P {}'.format(
            pacs_config.ae_title,
            pacs_config.ae_called,
            pacs_config.peer_address,
            pacs_config.peer_port,
            pacs_config.incoming_port
        )
    )


def _create_image_dir(entry, path_to_dir, dir_name):
    """ The folder structure is as follows:
        MAIN_DOWNLOAD_DIR/USER_DEFINED/PATIENTID/ACCESSION_NUMBER/SERIES_NUMBER
    """
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']
    image_folder = os.path.join(path_to_dir, dir_name, patient_id,
                                accession_number, series_number)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
    return image_folder


def construct_download_command(dcmtk_config, pacs_config, entry, path_to_dir, dir_name):
    base_command = _get_base_command(dcmtk_config, pacs_config)
    image_dir = _create_image_dir(entry, path_to_dir, dir_name)
    study_instance_uid = entry['study_id']
    series_instance_uid = entry['series_id']

    return (base_command +
        ' --output-directory ' + image_dir +
        ' -k StudyInstanceUID=' + study_instance_uid +
        ' -k SeriesInstanceUID=' + series_instance_uid + ' ' + dcmtk_config.dcmin)


def construct_transfer_command(dcmkt_config, pacs_config, target, study_id):
    """ Constructs the first part of the transfer command_creator to a PACS node. """
    node = TARGET_MAPPING[target]

    return (
        dcmkt_config.dcmtk_bin +
        'movescu -v -S '
        '-aem {} '
        '-aet {} '
        '-aec {} {} {} '
        '+P {} '
        '-k StudyInstanceUID={} {}'.format(
            node,
            pacs_config.ae_title,
            pacs_config.ae_called,
            pacs_config.peer_address,
            pacs_config.peer_port,
            pacs_config.incoming_port,
            study_id,
            dcmkt_config.dcmin
        )
    )

