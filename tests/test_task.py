import unittest
from concurrent.futures import Future

from meta.task import download_task, finish_task


class TestTask(unittest.TestCase):
    def test_creation(self):
        entry = {'patient_id': 'a',
                 'accession_number': 1,
                 'series_number': 2}
        task = download_task(entry, 'foo')
        self.assertEqual(task.patient_id, 'a')
        self.assertEqual(task.accession_number, 1)
        self.assertEqual(task.series_number, 2)

    def test_done(self):
        entry = {'patient_id': 'a',
                 'accession_number': 1,
                 'series_number': 2}
        task = download_task(entry, 'foo')
        future = Future()
        future.set_result(1)
        future.task = task

        new_task = finish_task(future)
        self.assertNotEqual(new_task.creation_time, new_task.execution_time)


