# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🗄️ PostgreSQL Primary & Replica Structure for All OTAP Environments

... *(existing content unchanged)* ...

### 🗂️ Sample `inventory/hosts.yml` for OTAP PostgreSQL Cluster

Below is an example of a valid Ansible inventory layout for all environments, aligning with the `group_vars/` structure:

```yaml
all:
  children:
    development:
      children:
        db_d_dbbds1:
          hosts:
            db_d_dbbds1_prim:
            db_d_dbbds1_repl:
        db_d_dbbds2:
          hosts:
            db_d_dbbds2_prim:
            db_d_dbbds2_repl:

    test:
      children:
        db_t_dbbds1:
          hosts:
            db_t_dbbds1_prim:
            db_t_dbbds1_repl:
        db_t_dbbds2:
          hosts:
            db_t_dbbds2_prim:
            db_t_dbbds2_repl:

    acceptance:
      children:
        db_a_dbbds1:
          hosts:
            db_a_dbbds1_prim:
            db_a_dbbds1_repl:
        db_a_dbbds2:
          hosts:
            db_a_dbbds2_prim:
            db_a_dbbds2_repl:

    production:
      children:
        db_p_dbbds1:
          hosts:
            db_p_dbbds1_prim:
            db_p_dbbds1_repl:
        db_p_dbbds2:
          hosts:
            db_p_dbbds2_prim:
            db_p_dbbds2_repl:
```

Each `host:` entry must resolve either by DNS or be mapped via `/etc/hosts` or Vagrant private IP provisioning.

Let me know if you want to generate a dynamic script to build the `inventory/hosts.yml` file from the JSON structure as well.
