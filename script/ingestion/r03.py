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

data = {}
for filename in glob('../../src/pages/r03/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		if "grant_num" in row:
			description = m[-1].strip()
			grant_num = row['grant_num']
			uid = str(uuid5(NAMESPACE_URL, grant_num))
			data[uid] = {**row, "description": description}
r03_df = pd.DataFrame.from_dict(data, orient="index").fillna('')
r03_df.index.name = "id"
r03_df.to_csv('r03.tsv', sep="\t")
# Update S3
backup_file(r03_df, "r03")

## ingest

cur = connection.cursor()

cur.execute('''
  create table r03_tmp
  as table r03
  with no data;
''')

s_buf = io.StringIO()
r03_df.to_csv(s_buf, header=True, sep="\t", quoting=csv.QUOTE_NONE)
s_buf.seek(0)
columns = next(s_buf).strip().split('\t')
cur.copy_from(s_buf, 'r03_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
    insert into r03 (%s)
      select %s
      from r03_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table r03_tmp;')

connection.commit()
print("ingested r03")