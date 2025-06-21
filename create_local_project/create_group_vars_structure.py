import os

structure = {
  "development": {
    "db_d_dbbds1": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
    "db_d_dbbds2": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
  },
  "test": {
    "db_t_dbbds1": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
    "db_t_dbbds2": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
  },
  "acceptance": {
    "db_a_dbbds1": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
    "db_a_dbbds2": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
  },
  "production": {
    "db_p_dbbds1": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
    "db_p_dbbds2": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
  }
}


def create_structure(base, structure):
    for group, hosts in structure.items():
        for host, subdirs in hosts.items():
            for subdir, files in subdirs.items():
                path = os.path.join(base, group, host, subdir)
                os.makedirs(path, exist_ok=True)
                for file in files:
                    with open(os.path.join(path, file), 'w') as f:
                        f.write(f"# {file}\n")

create_structure("group_vars", structure)