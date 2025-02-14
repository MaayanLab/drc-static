import pandas as pd
import yaml
from glob import glob
from uuid import uuid5, NAMESPACE_URL
from uuid import uuid5, NAMESPACE_URL
from s3_update import backup_file
from ingest_common import connection
import io
import math
import csv

dccs = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_dccs.tsv', sep="\t", index_col=0, header=0)
# map dcc names to their respective ids
dcc_mapper = {}
for i, v in dccs.loc[:,'short_label'].items():
		dcc_mapper[v] = i
data = {}
dcc_partnership = []
partnership_publication = []

for filename in glob('../../src/pages/partnerships/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		if "title" in row:
			description = m[-1].strip()
			title = row['title']
			uid = str(uuid5(NAMESPACE_URL, title))
			data[uid] = {
				"title": row["title"],
				"description": description,
				"status": row.get("status"),
				"website": row.get("website"),
				"priority": int(row["priority"] if 'priority' in row and not math.isnan(row['priority']) else 0),
				"image": row.get("image"),
				"grant_num": row.get("grant_num"),
			}
			if "dccs" in row:
				lead_dccs = [dcc_mapper[i] for i in row["lead_dccs"]] if "lead_dccs" in row else []
				for dcc in set([dcc_mapper[i] for i in row["dccs"]]):
					dcc_partnership.append({"partnership_id": uid, "dcc_id": dcc, "lead": dcc in lead_dccs})
			if "publications" in row:
				partnership_publication.append({"partnership_id": uid, "publication_id": row["publications"]})

partnership_df = pd.DataFrame.from_dict(data, orient="index").fillna('')
partnership_df.index.name = "id"
dcc_partnership_df = pd.DataFrame.from_records(dcc_partnership)
partnership_publication_df = pd.DataFrame.from_records(partnership_publication)

## Update S3
backup_file(partnership_df, "partnership", quoting=False)
backup_file(dcc_partnership_df, "dcc_partnership", False)
backup_file(partnership_publication_df, "partnership_publications", False)

## ingest

cur = connection.cursor()

cur.execute('''
	DELETE FROM dcc_partnerships;
''')

cur.execute('''
	DELETE FROM partnership_publications;
''')

cur.execute('''
	DELETE FROM partnerships;
''') 

cur.execute('''
	create table partnerships_tmp
	as table partnerships
	with no data;
''')

s_buf = io.StringIO()
partnership_df.to_csv(s_buf, header=True, sep="\t", quoting=csv.QUOTE_NONE)
s_buf.seek(0)
columns = next(s_buf).strip().split('\t')
cur.copy_from(s_buf, 'partnerships_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
		insert into partnerships (%s)
			select %s
			from partnerships_tmp
			on conflict (id)
				do update
				set %s
		;
	'''%(column_string, column_string, set_string))
cur.execute('drop table partnerships_tmp;')

cur = connection.cursor()
cur.execute('''
	create table dcc_partnerships_tmp
	as table dcc_partnerships
	with no data;
''')

d_buf = io.StringIO()
dcc_partnership_df.to_csv(d_buf, header=True, sep="\t", index=None)
d_buf.seek(0)

columns = next(d_buf).strip().split('\t')
cur.copy_from(d_buf, 'dcc_partnerships_tmp',
			columns=columns,
			null='',
			sep='\t',
		)

column_string = ", ".join(columns)

cur.execute('''
		insert into dcc_partnerships (%s)
			select %s
			from dcc_partnerships_tmp
			on conflict 
				do nothing
		;
	'''%(column_string, column_string))
cur.execute('drop table dcc_partnerships_tmp;')
connection.commit()

cur = connection.cursor()
cur.execute('''
	create table partnership_publications_tmp
	as table partnership_publications
	with no data;
''')

p_buf = io.StringIO()
partnership_publication_df.to_csv(p_buf, header=True, sep="\t", index=None)
p_buf.seek(0)
columns = next(p_buf).strip().split('\t')
cur.copy_from(p_buf, 'partnership_publications_tmp',
	columns=columns,
	null='',
	sep='\t',
)

column_string = ", ".join(columns)

cur.execute('''
		insert into partnership_publications (%s)
			select %s
			from partnership_publications_tmp
			on conflict 
				do nothing
		;
	'''%(column_string, column_string))
cur.execute('drop table partnership_publications_tmp;')
connection.commit()

print("Ingested partnerships")

