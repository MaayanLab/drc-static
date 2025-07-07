import pandas as pd
import yaml
from glob import glob
from uuid import uuid5, NAMESPACE_URL
from uuid import uuid5, NAMESPACE_URL
from s3_update import backup_file
from ingest_common import connection
import io

old_df = pd.read_csv('https://cfde-drc.s3.amazonaws.com/database/files/current_dccs.tsv', sep="\t")
old_df = old_df.set_index('label')
df = None
init = False
for filename in glob('../../src/pages/dccs/*.md'):
	with open(filename) as o:
		markdown = o.read()
		m = markdown.split("---")
		yml = yaml.safe_load(m[1])
		if "label" in yml:
			description = m[-1].strip()
			label = yml['label']
			if label in old_df.index:
				uid = old_df.loc[label, 'id']
			else:
				print(label)
				uid = str(uuid5(NAMESPACE_URL, label))
			if not init:
				init = True
				df = pd.DataFrame(index=[], columns=["label"] + [i for i in old_df.columns if not i =="id"])
				df.index.name = "id"
			values = {}
			if description:
				values["description"] = description
			for k,v in yml.items():
				if not k=='layout':
					values[k] = v
			df.loc[uid] = values

# test if the old values are in there

for i,row in old_df[old_df.active == True].reset_index().set_index("id").iterrows():
	if i not in df.index:
		raise(Exception("%s not in previous dcc"%i))
	new_row = df.loc[i]
	for k,v in row.items():
		if not new_row[k] == v:
			if type(new_row[k]) == str and not (new_row[k].replace("https://cfde-drc.s3.amazonaws.com/assets/img/", "/img/") == v):
				raise(Exception("key %s not the same, expected %s got %s"%(k, v, new_row[k])))

## Update S3
backup_file(df, "dccs")

## ingest

cur = connection.cursor()
cur.execute('''
  create table dcc_tmp
  as table dccs
  with no data;
''')

s_buf = io.StringIO()
df.to_csv(s_buf, header=True, sep="\t")
s_buf.seek(0)
columns = next(s_buf).strip().split('\t')
cur.copy_from(s_buf, 'dcc_tmp',
	columns=columns,
	null='',
	sep='\t',
)

cur.execute('''
    insert into dccs (id, label, short_label, description, homepage, icon, cfde_partner, active, cf_site)
      select id, label, short_label, description, homepage, icon, cfde_partner, active, cf_site
      from dcc_tmp
      on conflict (id)
        do update
        set label = excluded.label,
            short_label = excluded.short_label,
            description = excluded.description,
            homepage = excluded.homepage,
            icon = excluded.icon,
            cfde_partner = excluded.cfde_partner,
            active = excluded.active,
            cf_site = excluded.cf_site
    ;
  ''')
cur.execute('drop table dcc_tmp;')
connection.commit()

print("Ingested DCCs")