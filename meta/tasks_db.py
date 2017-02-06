
def select_download(c):
    result = []
    for row in c.execute('SELECT * FROM TASKS_DB'):
        result.append(row)
    return result


def insert_download(c, download):
    print(download)
    # Cursor, Task -> None
    c.execute('INSERT INTO TASKS_DB VALUES (NULL, ?,?,?,?,?,?,?,?)', download)
    return None

def insert_transfer(transfer):
  return None


def update_download(download):
  return None

def update_transfer(transfer):
  return None
