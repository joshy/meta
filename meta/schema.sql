CREATE TABLE IF NOT EXISTS DOWNLOAD_TASKS
    (id INTEGER PRIMARY KEY,
     patient_id text,
     series_number text,
     dir_name text,
     creation_time text,
     execution_time text,
     running_time real,
     status text,
     exception text);


CREATE TABLE IF NOT EXISTS TRANSFER_TASKS
    (id INTEGER PRIMARY KEY,
     stuy_id text,
     creation_time text,
     executin_time text,
     running_time real,
     status text,
     exception text);