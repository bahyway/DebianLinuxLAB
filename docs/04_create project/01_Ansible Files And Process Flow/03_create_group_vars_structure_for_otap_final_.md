# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🗄️ PostgreSQL Primary & Replica Structure for All OTAP Environments

You can replicate the structure used for the `development` environment across all OTAP environments to represent both Primary and Replica PostgreSQL nodes. Here's a unified structure example:

```
group_vars/
├── development/
│   ├── db_d_dbbds1/
│   │   ├── db_d_dbbds1_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_d_dbbds1_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   ├── db_d_dbbds2/
│   │   ├── db_d_dbbds2_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_d_dbbds2_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
├── test/
│   ├── db_t_dbbds1/
│   │   ├── db_t_dbbds1_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_t_dbbds1_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   ├── db_t_dbbds2/
│   │   ├── db_t_dbbds2_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_t_dbbds2_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
├── acceptance/
│   ├── db_a_dbbds1/
│   │   ├── db_a_dbbds1_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_a_dbbds1_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   ├── db_a_dbbds2/
│   │   ├── db_a_dbbds2_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_a_dbbds2_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
├── production/
│   ├── db_p_dbbds1/
│   │   ├── db_p_dbbds1_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_p_dbbds1_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   ├── db_p_dbbds2/
│   │   ├── db_p_dbbds2_prim/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
│   │   ├── db_p_dbbds2_repl/
│   │   │   ├── vars/main.yml
│   │   │   └── vault/secrets.yml
```

This structure gives you full control and isolation over PostgreSQL Primary/Replica behavior in every OTAP environment. You can define separate replication roles, parameters, or secrets for each host instance.

Let me know if you'd like a complete JSON + Python script generator for this extended version.

✅ Yes: Below is a complete JSON + Python script generator to automate creation of this entire structure for all four OTAP environments including all primary/replica folders and placeholder variable files.

### 📁 JSON Structure

```json
{
  "group_vars": {
    "development": {
      "db_d_dbbds1": {
        "db_d_dbbds1_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_d_dbbds1_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      },
      "db_d_dbbds2": {
        "db_d_dbbds2_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_d_dbbds2_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      }
    },
    "test": {
      "db_t_dbbds1": {
        "db_t_dbbds1_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_t_dbbds1_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      },
      "db_t_dbbds2": {
        "db_t_dbbds2_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_t_dbbds2_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      }
    },
    "acceptance": {
      "db_a_dbbds1": {
        "db_a_dbbds1_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_a_dbbds1_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      },
      "db_a_dbbds2": {
        "db_a_dbbds2_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_a_dbbds2_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      }
    },
    "production": {
      "db_p_dbbds1": {
        "db_p_dbbds1_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_p_dbbds1_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      },
      "db_p_dbbds2": {
        "db_p_dbbds2_prim": { "vars": ["main.yml"], "vault": ["secrets.yml"] },
        "db_p_dbbds2_repl": { "vars": ["main.yml"], "vault": ["secrets.yml"] }
      }
    }
  }
}
```

### 🐍 Python Generator Script

````python
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
``` for all four OTAP environments including all primary/replica folders and placeholder variable files.

````
