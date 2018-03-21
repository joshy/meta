import unittest
from unittest.mock import MagicMock
from concurrent.futures import Future

from meta.task import download_task, finish_task

class TestTask(unittest.TestCase):
    def test_creation(self):
        entry = {'patient_id': 'a',
                 'accession_number': 1,
                 'series_number': 2,
                 'study_id': 4,
                 'series_id': 3}
        conn = MagicMock()
        task = download_task(conn, entry, 'foo', '/tmp')
        self.assertEqual(task.patient_id, 'a')
        self.assertEqual(task.accession_number, 1)
        self.assertEqual(task.series_number, 2)

    def test_done(self):
        entry = {'patient_id': 'a',
                 'accession_number': 1,
                 'series_number': 2,
                 'study_id': 4,
                 'series_id': 3}
        conn = MagicMock()
        task = download_task(conn, entry, 'foo', '/tmp')
        future = Future()
        future.set_result(1)
        future.task = task
        finish_task(conn, future)
        self.assertNotEqual(future.task.creation_time, future.task.execution_time)
