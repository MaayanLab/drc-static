import pandas as pd
import yaml
from glob import glob
from uuid import uuid5, NAMESPACE_URL
from uuid import uuid5, NAMESPACE_URL
from s3_update import backup_file
from ingest_common import connection
import io
import csv

dccs = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_dccs.tsv', sep="\t", index_col=0, header=0)
# map dcc names to their respective ids
dcc_mapper = {}
for k,v in dccs.iterrows():
	dcc_mapper[v["short_label"]] = k

partnerships = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_partnerships.tsv', sep="\t", index_col=0)
partnership_mapper = {}
for k,v in partnerships.iterrows():
	partnership_mapper[v["title"]] = k

r03 = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_r03s.tsv', sep="\t", index_col=0)
r03_mapper = {}
for k,v in r03.iterrows():
	r03_mapper[v["grant_num"]] = k

publication_columns = ["title", "journal", "authors", "year", "page", "volume", "issue", "pmid", "pmcid", "doi", "landmark", "tool_id", "carousel", "carousel_title", "carousel_link", "carousel_description", "image", "featured", "keywords" ]
dcc_publication_columns = ["publication_id", "dcc_id"]
partnership_publication_columns = ["publication_id", "partnership_id"]
r03_publication_columns = ["publication_id", "r03_id"]

publication_df = pd.DataFrame("-", index=[], columns=publication_columns)
publication_df.index.name = "id"
dcc_publication_df = pd.DataFrame("-", index=[], columns=dcc_publication_columns)
partnership_publication_df = pd.DataFrame("-", index=[], columns=partnership_publication_columns)
r03_publication_df = pd.DataFrame("-", index=[], columns=r03_publication_columns)
ind = 0
pind = 0
rind = 0

for filename in glob('../../src/pages/publications/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		yml = yaml.safe_load(m[1])
		if "title" in yml:
			title = yml['title']
			uid = str(uuid5(NAMESPACE_URL, title))
			v = {c: yml[c] for c in publication_columns if c in yml}
			publication_df.loc[uid] = v
			if "dccs" in yml:
				for dcc in yml["dccs"]:
					dcc = dcc.strip()
					dcc_id = dcc_mapper[dcc]
					dcc_publication_df.loc[ind] = [uid, dcc_mapper[dcc]]
					ind += 1
			if "partnerships" in yml:
				partnership = yml["partnerships"]
				partnership = partnership.strip()
				partnership_id = partnership_mapper[partnership]
				partnership_publication_df.loc[pind] = [uid, partnership_mapper[partnership]]
				pind += 1
			
			if "r03" in yml:
				r03 = yml["r03"]
				r03 = r03.strip()
				r03_id = r03_mapper[r03]
				r03_publication_df.loc[rind] = [uid, r03_mapper[r03]]
				rind += 1

## Update S3
backup_file(publication_df, "publications", quoting=False)
backup_file(dcc_publication_df, "dcc_publications", False)
backup_file(partnership_publication_df, "partnership_publications", False)
backup_file(r03_publication_df, "r03_publications", False)

## ingest

cur = connection.cursor()
cur.execute('''
  DELETE FROM dcc_publications;
''')

cur.execute('''
  DELETE FROM partnership_publications;
''')

cur.execute('''
  DELETE FROM r03_publications;
''')

cur.execute('''
  DELETE FROM publications;
''')

cur.execute('''
  create table publication_tmp
  as table publications
  with no data;
''')

p_buf = io.StringIO()
publication_df.to_csv(p_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t")
p_buf.seek(0)
columns = next(p_buf).strip().split('\t')
cur.copy_from(p_buf, 'publication_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])

cur.execute('''
    insert into publications (%s)
      select %s
      from publication_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table publication_tmp;')



cur = connection.cursor()
cur.execute('''
  create table dcc_publication_tmp
  as table dcc_publications
  with no data;
''')


d_buf = io.StringIO()
dcc_publication_df.to_csv(d_buf, header=True, sep="\t", index=None)
d_buf.seek(0)
columns = next(d_buf).strip().split('\t')
cur.copy_from(d_buf, 'dcc_publication_tmp',
	columns=dcc_publication_columns,
	null='',
	sep='\t',
)
cur.execute('''
    insert into dcc_publications (publication_id, dcc_id)
      select publication_id, dcc_id
      from dcc_publication_tmp
      on conflict 
        do nothing
    ;
  ''')
cur.execute('drop table dcc_publication_tmp;')


cur = connection.cursor()
cur.execute('''
  create table partnership_publication_tmp
  as table partnership_publications
  with no data;
''')

part_buf = io.StringIO()
partnership_publication_df.to_csv(part_buf, header=True, sep="\t", index=None)
part_buf.seek(0)
columns = next(part_buf).strip().split('\t')
cur.copy_from(part_buf, 'partnership_publication_tmp',
	columns=partnership_publication_columns,
	null='',
	sep='\t',
)
cur.execute('''
    insert into partnership_publications (publication_id, partnership_id)
      select publication_id, partnership_id
      from partnership_publication_tmp
      on conflict 
        do nothing
    ;
  ''')
cur.execute('drop table partnership_publication_tmp;')

cur = connection.cursor()
cur.execute('''
  create table r03_publication_tmp
  as table r03_publications
  with no data;
''')

r_buf = io.StringIO()
r03_publication_df.to_csv(r_buf, header=True, sep="\t", index=None)
r_buf.seek(0)
columns = next(r_buf).strip().split('\t')
cur.copy_from(r_buf, 'r03_publication_tmp',
	columns=r03_publication_columns,
	null='',
	sep='\t',
)

cur.execute('''
    insert into r03_publications (publication_id, r03_id)
      select publication_id, r03_id
      from r03_publication_tmp
      on conflict 
        do nothing
    ;
  ''')
cur.execute('drop table r03_publication_tmp;')


connection.commit()

print("ingested publications")