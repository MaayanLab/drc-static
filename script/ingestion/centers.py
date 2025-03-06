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
# center_publication = []
for filename in glob('../../src/pages/centers/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		if "label" in row:
			label = row['label']
			description = m[-1].strip()
			uid = str(uuid5(NAMESPACE_URL, label))
			data[uid] = {"description": description}
			for k,v in row.items():
				if not k == "layout":
					if type(v) == dict or type(v) == list:
						data[uid][k] = json.dumps(v)
					else:	
						data[uid][k] = v
			# if row.get("publications"):
			# 	for pub in set(row["publications"]):
			# 		center_publication.append({"center_id": uid, "publication_id": pub})

center_df = pd.DataFrame.from_dict(data, orient="index").fillna('')
center_df.index.name = "id"
# center_publication_df = pd.DataFrame.from_records(center_publication, columns=['center_id', 'publication_id'])

## Update S3
backup_file(center_df, "centers", quoting=False)
# backup_file(center_publication_df, "center_publication", False)

## ingest

print("ingesting...")

cur = connection.cursor()

cur.execute('''
	DELETE FROM center_publications;
''')

cur.execute('''
	DELETE FROM centers;
''') 

cur.execute('''
	create table centers_tmp
	as table centers
	with no data;
''')

p_buf = io.StringIO()
center_df.to_csv(p_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t", escapechar='\\')
p_buf.seek(0)
columns = next(p_buf).strip().split('\t')
cur.copy_from(p_buf, 'centers_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
		insert into centers (%s)
			select %s
			from centers_tmp
			on conflict (id)
				do update
				set %s
		;
	'''%(column_string, column_string, set_string))
cur.execute('drop table centers_tmp;')


# cur = connection.cursor()
# cur.execute('''
# 	create table center_publications_tmp
# 	as table center_publications
# 	with no data;
# ''')


# cp_buf = io.StringIO()
# center_publication_df.to_csv(cp_buf, header=True, sep="\t", index=None)
# cp_buf.seek(0)
# columns = next(cp_buf).strip().split('\t')
# cur.copy_from(cp_buf, 'center_publications_tmp',
# 	columns=columns,
# 	null='',
# 	sep='\t',
# )

# column_string = ", ".join(columns)

# cur.execute('''
# 		insert into center_publications (%s)
# 			select %s
# 			from center_publications_tmp
# 			on conflict 
# 				do nothing
# 		;
# 	'''%(column_string, column_string))
# cur.execute('drop table center_publications_tmp;')
connection.commit()

print("Ingested centers")

