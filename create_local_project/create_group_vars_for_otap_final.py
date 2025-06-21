import os

structure = {
  "development": {
    "db_d_dbbds1": {
      "db_d_dbbds1_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_d_dbbds1_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    },
    "db_d_dbbds2": {
      "db_d_dbbds2_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_d_dbbds2_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    }
  },
  "test": {
    "db_t_dbbds1": {
      "db_t_dbbds1_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_t_dbbds1_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    },
    "db_t_dbbds2": {
      "db_t_dbbds2_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_t_dbbds2_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    }
  },
  "acceptance": {
    "db_a_dbbds1": {
      "db_a_dbbds1_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_a_dbbds1_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    },
    "db_a_dbbds2": {
      "db_a_dbbds2_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_a_dbbds2_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    }
  },
  "production": {
    "db_p_dbbds1": {
      "db_p_dbbds1_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_p_dbbds1_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    },
    "db_p_dbbds2": {
      "db_p_dbbds2_prim": {"vars": ["main.yml"], "vault": ["secrets.yml"]},
      "db_p_dbbds2_repl": {"vars": ["main.yml"], "vault": ["secrets.yml"]}
    }
  }
}

def create_structure(base, structure):
    for env, hosts in structure.items():
        for host, roles in hosts.items():
            for role, folders in roles.items():
                for folder, files in folders.items():
                    path = os.path.join(base, env, host, role, folder)
                    os.makedirs(path, exist_ok=True)
                    for file in files:
                        with open(os.path.join(path, file), 'w') as f:
                            f.write(f"# {file}
")

create_structure("group_vars", structure)