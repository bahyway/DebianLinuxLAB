# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🛠️ Generate the OTAP `group_vars` Structure with JSON and Python

To automate the creation of the full OTAP `group_vars` folder structure, use the following two files:

#### 📁 1. JSON Representation: `group_vars_structure.json`

This JSON file defines the full directory layout:

```json
{
  "group_vars": {
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
}
```

#### 🐍 2. Python Script: `create_group_vars_structure.py`

This script reads the JSON and creates all folders and placeholder files:

```python
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
```

Run it with:

```bash
python3 create_group_vars_structure.py
```

This creates a complete OTAP-compliant directory tree with placeholder YAML files ready for your Ansible configuration.

---

\[Remaining sections unchanged]
