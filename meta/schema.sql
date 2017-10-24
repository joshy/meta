CREATE TABLE IF NOT EXISTS DOWNLOAD_TASKS
    (id INTEGER PRIMARY KEY,
     patient_id text,
     accession_number text,
     series_number text,
     series_instance_uid text,
     dir_name text,
     path text,
     creation_time text,
     execution_time text,
     running_time real,
     status text,
     exception text);


CREATE TABLE IF NOT EXISTS TRANSFER_TASKS
    (id INTEGER PRIMARY KEY,
     study_id text,
     creation_time text,
     execution_time text,
     running_time real,
     status text,
     exception text);