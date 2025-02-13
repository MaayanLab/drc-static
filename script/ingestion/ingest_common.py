import pandas as pd
import os
import psycopg2
import pathlib
import csv
import contextlib
import tempfile
import urllib.request
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
from uuid import UUID, uuid5

uuid0 = UUID('00000000-0000-0000-0000-000000000000')
def quote(col): return f'"{col}"'

#%%
class TableHelper:
  def __init__(self, tablename, columns, pk_columns, add_columns=tuple()):
    self.tablename = tablename
    self.pk_columns = pk_columns
    self.columns = columns
    self.add_columns = add_columns
  @contextlib.contextmanager
  def writer(self):
    with tempfile.TemporaryDirectory() as tmpdir:
      path = pathlib.Path(tmpdir)/(self.tablename+'.tsv')
      with path.open('w') as fw:
        yield csv.DictWriter(fw, self.columns, delimiter='\t', escapechar='\\', doublequote=False)
      print(f"inserting {self.tablename}...")
      with connection.cursor() as cur:
        cur.execute('set statement_timeout = 0')
        cur.execute(f'''
          create temporary table {quote(self.tablename+'_tmp')}
          as table {quote(self.tablename)}
          with no data;
        ''')
        with path.open('r') as fr:
          cur.copy_from(fr, f"{self.tablename}_tmp",
            columns=self.columns,
            null='',
            sep='\t',
          )
        update_set = ','.join([
          *[f"{quote(col)} = excluded.{quote(col)}" for col in self.columns if col not in self.pk_columns and col not in self.add_columns],
          *[f"{quote(col)} = {quote(self.tablename)}.{quote(col)} + excluded.{quote(col)}" for col in self.add_columns],
        ])
        do_update_set = f"do update set {update_set}" if update_set else "do nothing"
        cur.execute(f'''
            insert into {quote(self.tablename)} ({', '.join(map(quote, self.columns))})
              select {', '.join(map(quote, self.columns))}
              from {quote(self.tablename+'_tmp')}
              on conflict ({', '.join(map(quote, self.pk_columns))})
              {do_update_set};
        ''')
        cur.execute(f"drop table {quote(self.tablename+'_tmp')};")
        connection.commit()

#%%
# Establish connection to database

load_dotenv(pathlib.Path(__file__).parent.parent / 'drc-portals' / '.env')
load_dotenv()
########## DB ADMIN INFO: BEGIN ############
# Comment the line below with .env.dbadmin if not ingesting, almost always ingesting if running these scripts
#load_dotenv(pathlib.Path(__file__).parent.parent.parent/'DB_ADMIN_INFO'/'.env.dbadmin')
########## DB ADMIN INFO: END   ############

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL == None:
  load_dotenv('../../drc-portals/.env') # for fair assessment 
  load_dotenv()
  DATABASE_URL = os.getenv("DATABASE_URL")
result = urlparse(DATABASE_URL)
username = result.username
password = unquote(result.password)
database = result.path[1:]
hostname = result.hostname
port = result.port

##### Line below is for debug only, always keep commented otherwise
#####print(f"username: {username}, password: {password}, database: {database}, hostname: {hostname}")

connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)
