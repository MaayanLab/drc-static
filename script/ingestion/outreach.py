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
for k,v in dccs.iterrows():
	dcc_mapper[v["short_label"]] = k

centers = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_centers.tsv', sep="\t", index_col=0, header=0)
# map dcc names to their respective ids
center_mapper = {}
for k,v in centers.iterrows():
	center_mapper[v["short_label"]] = k


outreach_columns = ["title", "short_description", "description", "tags", "agenda", "featured", "active", "start_date", "end_date", "application_start", "application_end", "link", "image", "carousel", "carousel_description", "cfde_specific", "flyer", "recurring", "ical", "schedule"]
dcc_outreach_columns = ["outreach_id", "dcc_id"]
center_outreach_columns = ["outreach_id", "center_id"]

outreach_df = pd.DataFrame("-", index=[], columns=outreach_columns)
outreach_df.index.name = 'id'
dcc_outreach_df = pd.DataFrame("-", index=[], columns=dcc_outreach_columns)
ind = 0

center_outreach_df = pd.DataFrame("-", index=[], columns=center_outreach_columns)
cind = 0
outreach_df = outreach_df.fillna('')

for filename in glob('../../src/pages/outreach/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		val = yaml.safe_load(m[1])
		description = m[-1].strip()
		if "title" in val:
			title = val["title"]
		
			start_date = val.get("start_date", "")
			end_date = val.get("end_date", "")
			string_id = title + str(start_date) + str(end_date)
			uid = str(uuid5(NAMESPACE_URL, string_id))
			if uid =='830ddbac-bf21-5612-af1a-75c713045299':
				print(val)
			vdict = {}
			for c in outreach_columns:
				if c == "description":
					vdict[c] = description
				elif val.get(c):
					vdict[c] = val[c]
			outreach_df.loc[uid] = vdict
			if val.get('dcc'):
				for dcc in val["dcc"]:
					dcc_id = dcc_mapper[dcc]
					dcc_outreach_df.loc[ind] = [uid, dcc_mapper[dcc]]
					ind += 1
			if val.get('center'):
				for center in val["center"]:
					center_id = center_mapper[center]
					center_outreach_df.loc[cind] = [uid, center_mapper[center]]
					cind += 1


# webinars
webinars = {}
outreach_df['agenda'] = ''
for filename in glob('../../src/pages/webinars/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		val = yaml.safe_load(m[1])
		description = m[-1].strip()
		if "agenda" in val:
			title = 'CFDE Webinar Series'
			start_date = val["start_date"]
			end_date = val.get('end_date')
			string_id = title + str(start_date) + str(end_date)
			uid = str(uuid5(NAMESPACE_URL, string_id))
			if uid not in outreach_df.index:
				print(uid)
			else:
				if not type(val["agenda"]) == list:
					print(val['agenda'])
				outreach_df.at[uid,'agenda'] = json.dumps(val["agenda"])



outreach_df['active'] = outreach_df['active'].fillna(0).astype(bool)
outreach_df['featured'] = outreach_df['featured'].fillna(0).astype(bool)
outreach_df['carousel'] = outreach_df['carousel'].fillna(0).astype(bool)
outreach_df['recurring'] = outreach_df['recurring'].fillna(0).astype(bool)
outreach_df['cfde_specific'] = outreach_df['cfde_specific'].fillna(0).astype(bool)
backup_file(outreach_df, "outreach", quoting=False)
backup_file(dcc_outreach_df, "dcc_outreach", False)
backup_file(center_outreach_df, "center_outreach", False)

cur = connection.cursor()

cur.execute('''
  DELETE FROM dcc_outreach;
''')

cur.execute('''
  DELETE FROM center_outreach;
''')

cur.execute('''
  DELETE FROM outreach;
''') 
cur.execute('''
  create table outreach_tmp
  as table outreach
  with no data;
''')

o_buf = io.StringIO()
outreach_df.to_csv(o_buf, header=True, quoting=csv.QUOTE_NONE, sep="\t")
o_buf.seek(0)
columns = next(o_buf).strip().split('\t')
cur.copy_from(o_buf, 'outreach_tmp',
	columns=columns,
	null='',
	sep='\t',
)
column_string = ", ".join(columns)
set_string = ",\n".join(["%s = excluded.%s"%(i,i) for i in columns])

cur.execute('''
    insert into outreach (%s)
      select %s
      from outreach_tmp
      on conflict (id)
        do update
        set %s
    ;
  '''%(column_string, column_string, set_string))
cur.execute('drop table outreach_tmp;')

cur = connection.cursor()
cur.execute('''
  create table dcc_outreach_tmp
  as table dcc_outreach
  with no data;
''')
d_buf = io.StringIO()
dcc_outreach_df.to_csv(d_buf, header=True, sep="\t", index=None)
d_buf.seek(0)
columns = next(d_buf).strip().split('\t')
cur.copy_from(d_buf, 'dcc_outreach_tmp',
	columns=dcc_outreach_columns,
	null='',
	sep='\t',
)

cur.execute('''
    insert into dcc_outreach (outreach_id, dcc_id)
      select outreach_id, dcc_id
      from dcc_outreach_tmp
      on conflict 
        do nothing
    ;
  ''')
cur.execute('drop table dcc_outreach_tmp;')

# centers

cur = connection.cursor()
cur.execute('''
  create table center_outreach_tmp
  as table center_outreach
  with no data;
''')
c_buf = io.StringIO()
center_outreach_df.to_csv(c_buf, header=True, sep="\t", index=None)
c_buf.seek(0)
columns = next(c_buf).strip().split('\t')
cur.copy_from(c_buf, 'center_outreach_tmp',
	columns=center_outreach_columns,
	null='',
	sep='\t',
)

cur.execute('''
    insert into center_outreach (outreach_id, center_id)
      select outreach_id, center_id
      from center_outreach_tmp
      on conflict 
        do nothing
    ;
  ''')
cur.execute('drop table center_outreach_tmp;')
connection.commit()

print("Ingested outreach and webinars")