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
publication_df = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_publications.tsv', sep="\t", index_col=0)
publication_mapper = {}
for i, row in publication_df.iterrows():
	doi = row['doi']
	if type(doi) == str:
		publication_mapper[doi] = i

tools = {}
for filename in glob('../../src/pages/tools/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		row = yaml.safe_load(m[1])
		if "label" in row:
			uid = str(uuid5(NAMESPACE_URL, row['label']))
			description = m[-1].strip()
			
			val = {"description": description}
			for k, v in row.items():
				if k == "doi":
					if type(v) == str:
						doi = v.replace("https://doi.org/", "")
						pub_id = publication_mapper[doi]
						publication_df.at[pub_id, 'tool_id'] = uid
				elif k not in ["layout", "id", "tutorial"]:
					val[k] = v
				elif k == "tutorial":
					val[k] = json.dumps(v)
					print(val[k], type(v))
					
			tools[uid] = val

tools_df = pd.DataFrame.from_dict(tools, orient="index").fillna('')
tools_df.index.name = "id"
backup_file(tools_df, "tools", quoting=False)
backup_file(publication_df, "publications", quoting=False)

cur = connection.cursor()
# Remove tool_ids on publication
cur.execute('''
  UPDATE publications
  SET tool_id=NULL;
''')

# delete tool table
cur.execute('''
  DELETE FROM tools;
''') 
# Create tools
cur.execute('''
  create table tools_tmp
  as table tools
  with no data;
''')

t_buf = io.StringIO()
tools_df.to_csv(t_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t")
t_buf.seek(0)

columns = next(t_buf).strip().split('\t')
cur.copy_from(t_buf, 'tools_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
    insert into tools (%s)
      select %s
      from tools_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table tools_tmp;')

# Create publications
cur.execute('''
  create table publications_tmp
  as table publications
  with no data;
''')

p_buf = io.StringIO()
publication_df.to_csv(p_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t")
p_buf.seek(0)

columns = next(p_buf).strip().split('\t')
cur.copy_from(p_buf, 'publications_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])
cur.execute('''
    insert into publications (%s)
      select %s
      from publications_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table publications_tmp;')



connection.commit()

print("Ingested Tools")