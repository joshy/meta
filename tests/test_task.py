import unittest
import os
import json

from unittest.mock import MagicMock

from concurrent.futures import Future
from meta.queue_manager import submit_task  # download_task, finish_task

import meta
from meta.app import app
import tempfile
from sqlalchemy import create_engine

from meta.queue_manager_models import db
from meta.queue_manager_models import TaskInfo

temp_db_name = 'meta_unittest_db'
admin_db_name = 'postgres'

ADMIN_DB_URI = (
    'postgresql+psycopg2://postgres:postgres@localhost/' +
    admin_db_name

)
TEST_DB_URI = (
    'postgresql+psycopg2://postgres:postgres@localhost/' +
    temp_db_name
)


class MetaTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        #app.app_context().push()
        db.init_app(app)
        db.create_all()
        db.session.commit()

        #
        # engine = create_engine(ADMIN_DB_URI)
        # conn = engine.connect()
        # conn.execute("commit")  # bypassing always run in transaction
        # try:
        #     conn.execute(
        #         '''SELECT pg_terminate_backend(pg_stat_activity.pid)
        #         FROM pg_stat_activity
        #         WHERE pg_stat_activity.datname = {}
        #         AND pid <> pg_backend_pid();
        #         '''.format(temp_db_name))
        # except:
        #     conn.execute('ROLLBACK')
        #
        # conn.execute("DROP DATABASE IF EXISTS " + temp_db_name)
        # conn.execute("commit")
        #
        # conn.execute("CREATE DATABASE " + temp_db_name)
        # conn.close()
        # engine.dispose()
        #
        # app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI #tempfile.mkstemp()



    def tearDown(self):
        db.session.remove()
        db.drop_all()

        # no need to destroy, it will droped on setUp every time
        #engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        #conn = engine.connect()
        #conn.execute("commit")  # bypassing always run in transaction
        #conn.execute("DROP DATABASE " + temp_db_name)

        # app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        #conn.close()

        #os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])
        #pass

    def test_store_task_info(self):
        print(db)
        pass


    def test_empty_tasks(self):
        rv = self.app.get('/tasks')
        assert (b'<!DOCTYPE html>\n<html lang="en">\n<title>Tasks status'
                b'</title>\n<meta name="viewport" content="width=device-width, '
                b'initial-scale=1">\n<link rel="stylesheet" '
                b'href="/static/css/tachyons.min.css">\n\n'
                b'<body class="w-100">\n  '
                b'<nav class="dt w-100 border-box pa3 ph5-ns">\n  '
                b'<a class="dtc v-btm link w-75 link f6 f5-ns dib '
                b'mr3 mr4-ns" href="/" title="Home">\n    '
                b'Pacs Crawler\n    '
                b'<div class="dib">\n        '
                b'<small class="nowrap f6 mt2 mt3-ns pr2 '
                b'black-70 fw2">1.5.2</small>\n'
                b'    </div>\n  </a>\n  <div class="dtc v-btm w-50 tr">\n    '
                b'<a class="link f6 f5-ns dib" '
                b'href="http://www.unispital-basel.ch/'
                b'index.php?id=1899" title="Klinik f\xc3\xbcr '
                b'Radiologie und Nuklearmedizin">\n    '
                b'Universit\xc3\xa4tsspital Basel<br>\n    '
                b'Klinik f\xc3\xbcr Radiologie und Nuklearmedizin\n    '
                b'</a>\n  </div>\n</nav>\n  <div id="container" '
                b'class="bt b--black-10">\n'
                b'</body>\n<script type=text/javascript '
                b'src="/static/js/jquery-3.1.0.min.js"></script>\n'
                b'<script type=text/javascript>\n  $(function() {\n    '
                b'startRefresh();\n    var sec = 30;\n    '
                b'console.log(sec);\n    setInterval(function() {\n      '
                b'sec = sec - 1;\n      if (sec === 0) sec = 30;\n      '
                b'$(\'#timer\').html(sec);\n    }, 1000);\n  });\n  '
                b'function startRefresh() {\n    '
                b'setTimeout(startRefresh, 30000);\n    '
                b'$.get(\'/tasks/data\',\n      function(data) {\n        '
                b'$(\'#container\').html(data);\n    });\n  }'
                b'\n</script>\n</html>') == rv.get_data()
        #print(rv, rv.get_data(), rv.status, sep=' :: ')

    def test_empty_transfers(self):
        rv = self.app.get('/transfers')
        assert (b'<!DOCTYPE html>\n<html lang="en">\n'
                b'<title>Transfer status</title>\n'
                b'<meta name="viewport" content="width=device-width, '
                b'initial-scale=1">\n<link rel="stylesheet" '
                b'href="/static/css/tachyons.min.css">\n\n'
                b'<body class="w-100">\n  '
                b'<nav class="dt w-100 border-box pa3 ph5-ns">\n  '
                b'<a class="dtc v-btm link w-75 link f6 f5-ns '
                b'dib mr3 mr4-ns" href="/" title="Home">\n    '
                b'Pacs Crawler\n    <div class="dib">\n        '
                b'<small class="nowrap f6 mt2 mt3-ns pr2 black-70 '
                b'fw2">1.5.2</small>\n    </div>\n  </a>\n  '
                b'<div class="dtc v-btm w-50 tr">\n    '
                b'<a class="link f6 f5-ns dib" href='
                b'"http://www.unispital-basel.ch/index.php?id=1899" '
                b'title="Klinik f\xc3\xbcr '
                b'Radiologie und Nuklearmedizin">\n    '
                b'Universit\xc3\xa4tsspital Basel<br>\n    '
                b'Klinik f\xc3\xbcr Radiologie und Nuklearmedizin\n    '
                b'</a>\n  </div>\n</nav>\n  <div id="container" '
                b'class="bt b--black-10">\n</body>\n<script '
                b'type=text/javascript '
                b'src="/static/js/jquery-3.1.0.min.js"></script>\n'
                b'<script type=text/javascript>\n  $(function() {\n    '
                b'startRefresh();\n    var sec = 30;\n    '
                b'console.log(sec);\n    setInterval(function() {\n      '
                b'sec = sec - 1;\n      if (sec === 0) sec = 30;\n      '
                b'$(\'#timer\').html(sec);\n    }, 1000);\n  });\n  '
                b'function startRefresh() {\n    setTimeout(startRefresh, '
                b'30000);\n    $.get(\'/transfers/data\',\n      '
                b'function(data) {\n        '
                b'$(\'#container\').html(data);\n    });\n  }\n'
                b'</script>\n</html>') == rv.get_data()

    def submit_task(self):
        series_dicts = [
            {
                'patient_id': 'pai1',
                'accession_number': 'acn1',
                'series_number': 'sen1',
                'study_id': 'sti1',
                'series_id': 'sei1',
                'type': 'DOWNLOAD'
            },
            {
                'patient_id': 'pai2',
                'accession_number': 'acn2',
                'series_number': 'sen2',
                'study_id': 'sti2',
                'series_id': 'sei2',
                'type': 'DOWNLOAD'
            }
        ]
        dir_name = 'fake_path_to_dir'

        data = {'data': series_dicts, 'dir': dir_name}
        json_data = json.dumps(data)

        return self.app.post(
            '/download',
            data=json_data,
            follow_redirects=True
        )

    def test_submit_task(self):
        expected = {"status": "OK", "series_length": 2}

        rv = self.submit_task()

        rv_data_str = rv.get_data().decode('utf-8')
        rv_data_dict = json.loads(rv_data_str)

        assert '200 OK' == rv.status
        for key in expected:
            assert rv_data_dict[key] == expected[key]
        assert len(rv_data_dict) == len(expected)

    def test_submit_transfer(self):
        def submit_transfers(self):
            series_dicts = [
                {
                    'patient_id': 'pai1',
                    'accession_number': 'acn1',
                    'series_number': 'sen1',
                    'study_id': 'sti1',
                    'series_id': 'sei1',
                    'type': 'DOWNLOAD'
                },
                {
                    'patient_id': 'pai2',
                    'accession_number': 'acn2',
                    'series_number': 'sen2',
                    'study_id': 'sti2',
                    'series_id': 'sei2',
                    'type': 'DOWNLOAD'
                }
            ]
            dir_name = 'fake_path_to_dir'

            data = {'data': series_dicts, 'dir': dir_name}
            json_data = json.dumps(data)

            return self.app.post(
                '/download',
                data=json_data,
                follow_redirects=True
            )

    if __name__ == '__main__':
        unittest.main()

#
# class TestTask(unittest.TestCase):
#     def test_creation(self):
#         entry = {'patient_id': 'a',
#                  'accession_number': 1,
#                  'series_number': 2,
#                  'series_id': 3}
#         conn = MagicMock()
#         future = submit_task(conn, 'dir', entry, 'fakse_command')
#         future.
#         #task = download_task(conn, entry, 'foo', '/tmp')
#
#         self.assertEqual(task.patient_id, 'a')
#         self.assertEqual(task.accession_number, 1)
#         self.assertEqual(task.series_number, 2)
#
#     def test_done(self):
#         entry = {'patient_id': 'a',
#                  'accession_number': 1,
#                  'series_number': 2,
#                  'series_id': 3}
#         conn = MagicMock()
#         task = download_task(conn, entry, 'foo', '/tmp')
#         future = Future()
#         future.set_result(1)
#         future.task = task
#         finish_task(conn, future)
#         self.assertNotEqual(future.task.creation_time, future.task.execution_time)
