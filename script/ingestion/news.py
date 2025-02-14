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

old_df = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_dccs.tsv', sep="\t")
old_df = old_df.set_index('label')
data = {}
for filename in glob('../../src/pages/news/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		if "title" in row:
			description = m[-1].strip()
			title = str(row["date"]) + row["title"]
			uid = str(uuid5(NAMESPACE_URL, title))
			vals = {**row, "description": description}
			if row.get("tags"):
				vals["tags"] = json.dumps(row["tags"])
			if row.get("supp_description"):
				vals["supp_description"] = json.dumps(row["supp_description"])
			
			data[uid] = vals
news_df = pd.DataFrame.from_dict(data, orient="index").fillna('')
news_df.index.name = "id"
## Update S3
backup_file(news_df, "news")

## ingest

cur = connection.cursor()

cur.execute('''
  create table news_tmp
  as table news
  with no data;
''')

s_buf = io.StringIO()
news_df.to_csv(s_buf, header=True, sep="\t", quoting=csv.QUOTE_NONE)
s_buf.seek(0)
columns = next(s_buf).strip().split('\t')
cur.copy_from(s_buf, 'news_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
    insert into news (%s)
      select %s
      from news_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table news_tmp;')

connection.commit()
print("ingested news")