import pandas as pd
import yaml
from glob import glob
from uuid import uuid5, NAMESPACE_URL
from uuid import uuid5, NAMESPACE_URL
from s3_update import backup_file
from ingest_common import connection
import io
import csv
import json

dccs = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_dccs.tsv', sep="\t", index_col=0, header=0)
# map dcc names to their respective ids
dcc_mapper = {}
for i, v in dccs.loc[:,'short_label'].items():
    dcc_mapper[v] = i

data = {}
dcc_usecase = []
for filename in glob('../../src/pages/usecase/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		title = row['title']
		uid = str(uuid5(NAMESPACE_URL, title))
		data[uid] = {
			"title": row.get("title"),
			"short_description": row.get("short_description"),
			"description": m[-1].strip(),
			"tool_icon": row.get("tool_icon"),
			"tool_name": row.get("tool_name"),
			"inputs": json.dumps(list(set(row["inputs"].strip().split("; ")))) if row.get('inputs') else '',
			"sources": json.dumps(list(set(row["sources"].strip().split("; ")))) if row.get('sources') else '',
			"link": row.get("link"),
			"image": row.get("image"),
			"tutorial": row.get("tutorial"),
			"featured": row.get("featured"),
			"creator_dcc_id": dcc_mapper[row["creator_dcc"][0]],
		}
		if row.get("source_dcc"): 
			for dcc in set([dcc_mapper[i] for i in row["source_dcc"]]):
				dcc_usecase.append({"usecase_id": uid, "dcc_id": dcc})

usecase_df = pd.DataFrame.from_dict(data, orient="index").fillna('')
usecase_df.index.name = "id"
dcc_usecase_df = pd.DataFrame.from_records(dcc_usecase)

backup_file(usecase_df, "usecase", quoting=False)
backup_file(dcc_usecase_df, "dcc_usecase", False)

cur = connection.cursor()

cur.execute('''
  DELETE FROM dcc_usecase;
''')

cur.execute('''
  DELETE FROM usecase;
''') 
cur.execute('''
  create table usecase_tmp
  as table usecase
  with no data;
''')

u_buf = io.StringIO()
usecase_df.to_csv(u_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t")
u_buf.seek(0)
columns = next(u_buf).strip().split('\t')
cur.copy_from(u_buf, 'usecase_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
    insert into usecase (%s)
      select %s
      from usecase_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table usecase_tmp;')
connection.commit()

cur = connection.cursor()
cur.execute('''
  create table dcc_usecase_tmp
  as table dcc_usecase
  with no data;
''')



d_buf = io.StringIO()
dcc_usecase_df.to_csv(d_buf, header=True, index=None, sep="\t")
d_buf.seek(0)
columns = next(d_buf).strip().split('\t')
cur.copy_from(d_buf, 'dcc_usecase_tmp',
	columns=columns,
	null='',
	sep='\t',
)

column_string = ", ".join(columns)

cur.execute('''
    insert into dcc_usecase (%s)
      select %s
      from dcc_usecase_tmp
      on conflict 
        do nothing
    ;
  '''%(column_string, column_string))
cur.execute('drop table dcc_usecase_tmp;')
connection.commit()

