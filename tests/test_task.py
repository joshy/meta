import unittest
import json

from unittest.mock import MagicMock, patch

from meta.models import TaskInfo, db
from meta.queue_manager import submit_task, _store_task_info, _bash_task

from meta.views import DOWNLOAD, TRANSFER
from meta.app_creator import create_app
from meta.views import _transfer_series

from datetime import datetime
from flask import current_app

temp_db_name = 'meta_unittest_db'


def _get_test_series(series_type):
    return [
        {
            'patient_id': 'pai1',
            'accession_number': 'acn1',
            'series_number': 'sen1',
            'study_id': 'sti1',
            'series_id': 'sei1',
            'task_type': series_type
        },
        {
            'patient_id': 'pai2',
            'accession_number': 'acn2',
            'series_number': 'sen2',
            'study_id': 'sti2',
            'series_id': 'sei2',
            'task_type': series_type
        }
    ]


def _get_test_task_info():
    return TaskInfo(
        dir_name='DIRNAME',
        study_id='STUDID',
        patient_id='PATID',
        accession_number='ACCNUM',
        series_number='SERNUM',
        command='UNITTESTCMD',
        running_time=None,
        status='UNITTESTING',
        exception=None,
        started=datetime.now(),
        finished=None,
        flag_finished=False,
        task_type='UNITTEST',
    )


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            config_object_path='tests.test_config',
            server_name='0.0.0.0:5558'
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        with self.app.app_context():
            TaskInfo  # This somehow sets the right context

        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        db.session.commit()


class CommonTests(Tests):
    def test_create_task_info_in_db(self):
        with self.app.app_context():
            series_dicts = _get_test_series(DOWNLOAD)

            _store_task_info('fake_dir', entry=series_dicts[0], command='fake_command')

            db_task = TaskInfo.query.get(1).__dict__
            test_task = series_dicts[0]
            del test_task['series_id']

            assert set(test_task.keys()).issubset(set(db_task.keys()))
            for key in test_task:
                assert test_task[key] == db_task[key]

    def test_submit_task(self):
        with self.app.app_context():
            with patch('meta.queue_manager._executor.submit') as mock_submit:
                mock_future = MagicMock()
                mock_future.add_done_callback = lambda x: None
                mock_submit.return_value = mock_future
                task_id = submit_task('some_dir', _get_test_series('fake_type')[0], 'fake command')
                assert task_id == 1
            assert mock_submit.called

    # noinspection PyMethodMayBeStatic
    def test_bash(self):
        with patch('meta.queue_manager.run') as mock_run, patch('meta.queue_manager.TaskInfo') as mock_TaskInfo:
            magic_mock = MagicMock()
            magic_mock.query.get = _get_test_task_info()
            mock_TaskInfo = magic_mock

            _bash_task(None, current_app.config, None)

        assert mock_run.called


class FlaskNavigationTests(Tests):
    def test_get_root(self):
        with self.app.app_context():
            rv = self.client.get('/')
            assert rv.status == '200 OK'

    def test_get_tasks(self):
        with self.app.app_context():
            rv = self.client.get('/tasks')
            assert rv.status == '200 OK'

    def test_get_transfers(self):
        with self.app.app_context():
            rv = self.client.get('/transfers')
            assert rv.status == '200 OK'


class TransferTests(Tests):
    def test_transfer(self):
        with self.app.app_context():
            with patch('meta.views.submit_task') as mock_transfer_series:
                mock_transfer_series.return_value = 42

                target = 'syngo'
                series_dicts = _get_test_series(TRANSFER)
                data = {'data': series_dicts, 'target': target}
                json_data = json.dumps(data)

                rv = self.client.post(
                    '/transfer',
                    data=json_data,
                    follow_redirects=True
                )

                assert '200 OK' == rv.status
        assert mock_transfer_series.called

    def test_transfer_series(self):
        with self.app.app_context():
            with patch('meta.views.submit_task') as mock_submit_task, patch('meta.views.construct_transfer_command') as mock_construct_transfer_command:
                mock_submit_task.return_value = 42
                mock_construct_transfer_command.return_value = 'some lame test command'
                series_dicts = _get_test_series(TRANSFER)
                assert _transfer_series(series_dicts, None) == 2
        assert mock_submit_task.called
        assert mock_construct_transfer_command.called

    def test_integration_submit_transfer(self):
        with self.app.app_context():
            with patch('meta.queue_manager._executor.submit') as mock_submit:
                mock_future = MagicMock()
                mock_future.add_done_callback = lambda x: None
                mock_submit.return_value = mock_future

                target = 'syngo'
                series_dicts = _get_test_series(TRANSFER)
                data = {'data': series_dicts, 'target': target}
                json_data = json.dumps(data)

                rv = self.client.post(
                    '/transfer',
                    data=json_data,
                    follow_redirects=True
                )

                assert '200 OK' == rv.status

        assert mock_submit.called


class DownloadTests(Tests):
    def test_integration_submit_download_task(self):
        with self.app.app_context():
            with patch('meta.queue_manager._executor.submit') as mock_submit:
                mock_future = MagicMock()
                mock_future.add_done_callback = lambda x: None
                mock_submit.return_value = mock_future

                test_response = {"status": "OK", "series_length": 2}

                dir_name = 'fake_path_to_dir'
                series_dicts = _get_test_series(DOWNLOAD)
                data = {'data': series_dicts, 'dir': dir_name}
                json_data = json.dumps(data)
                rv = self.client.post(
                    '/download',
                    data=json_data,
                    follow_redirects=True
                )

                rv_data_str = rv.get_data().decode('utf-8')
                rv_data_dict = json.loads(rv_data_str)

                assert '200 OK' == rv.status
                for key in test_response:
                    assert rv_data_dict[key] == test_response[key]
                assert len(rv_data_dict) == len(test_response)

        assert mock_submit.called

    if __name__ == '__main__':
        unittest.main()
