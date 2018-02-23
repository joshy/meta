from os.path import join, exists
from os import makedirs


TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}

def _get_image_dir(download_task):
        return join(
            download_task.output_dir,
            download_task.dir_name,
            download_task.patient_id,
            download_task.accession_number,
            download_task.series_number
        )

def _get_base_command(download_task):
    return (
        '{} -v -S -k QueryRetrieveLevel=SERIES -aet {} -aec {} {} {} +P {}'
        .format(
            download_task.movescu,
            download_task.aet,
            download_task.aec,
            download_task.peer_address,
            download_task.peer_port,
            download_task.incoming_port
        )
    )

def create_download_command(download_task):
    base_command = _get_base_command(download_task)
    image_dir = _get_image_dir(download_task)

    if not exists(image_dir):
        makedirs(image_dir, exist_ok=True)

    return (
        base_command +
        ' --output-directory ' + image_dir +
        ' -k StudyInstanceUID=' + download_task.study_instance_uid +
        ' -k SeriesInstanceUID=' + download_task.series_instance_uid +
        ' ' + download_task.dcmin
    )


def create_transfer_command(move_task):
        node = TARGET_MAPPING[move_task.target]
        return (
            '{} -v -S '
            '-aem {} '
            '-aet {} '
            '-aec {} {} {} '
            '+P {} '
            '-k StudyInstanceUID={} {}'.format(
                move_task.movescu,
                node,
                move_task.aet,
                move_task.aec,
                move_task.peer_address,
                move_task.peer_port,
                move_task.incoming_port,
                move_task.series_instance_uid,
                move_task.dcmin
            )
        )