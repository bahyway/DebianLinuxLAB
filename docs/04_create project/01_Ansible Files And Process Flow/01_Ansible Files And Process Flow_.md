# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

---

## 🔍 1. `inventory/hosts.yml`

### 📌 What it does:

This file defines the list of target machines (inventory) that Ansible will manage.

### 🧠 Why it's important:

Ansible needs to know *which hosts* to connect to and *how*. This file organizes VMs into logical groups like `vms`, `nginx`, `db`, etc.

### 🧾 Example:

```yaml
all:
  children:
    vms:
      hosts:
        vm1:
          ansible_host: 192.168.122.101
        vm2:
          ansible_host: 192.168.122.102
```

### ❓Alternative Group-Only Structure:

You can define groups and their children **without IP addresses**. For example:

```yaml
all:
  children:
    postgres_cluster:
      children:
        master:
        replica:
```

Then under each child group (like `master/` or `replica/`), you can create folders for additional variables:

```
group_vars/
├── postgres_cluster/
│   ├── vars/
│   │   └── main.yml
│   └── vault/
│       └── secrets.yml
```

### ✅ Is This Valid?

Yes — this is valid. Ansible will look for `group_vars/<groupname>/vars/main.yml` and `group_vars/<groupname>/vault/secrets.yml` automatically when processing the inventory. This structure is beneficial when:

* You want clear separation between public config (vars) and encrypted secrets (vault)
* You want to group logic for infrastructure tiers (e.g., frontend/backend)

### 🔁 How It Works

1. Ansible loads `inventory/hosts.yml` and parses group relationships.
2. If `group_vars/postgres_cluster/vars/main.yml` exists, it loads those variables for any host in `postgres_cluster`.
3. If `vault/secrets.yml` is encrypted using `ansible-vault`, it will also be loaded (if decryption key is available).

> 🧠 This approach increases modularity, especially in large infrastructure projects.

### 🧪 Validating Complex Group Hierarchies

A user-provided example attempted to use this structure:

```ini
[dbservers developing primary]
db_d_dbbds1_prim
db_d_dbbds2_prim
...
```

This is **not valid syntax**. You cannot define nested groups in a single INI-style header. Instead, use YAML-style nested group declarations for proper hierarchy:

```yaml
all:
  children:
    dbservers:
      children:
        developing:
          children:
            primary:
              hosts:
                db_d_dbbds1_prim:
                db_d_dbbds2_prim:
                db_d_dbbds3_prim:
            replica:
              hosts:
                db_d_dbbds1_repl:
                db_d_dbbds2_repl:
                db_d_dbbds3_repl:
```

This can be extended to `acceptance`, `test`, and `production` environments similarly.

Ansible will respect this hierarchy and load variable files accordingly from:

```
group_vars/
├── dbservers/
│   └── vars/main.yml
├── developing/
│   └── vars/main.yml
├── primary/
│   ├── vars/main.yml
│   └── vault/secrets.yml
```

This is modular, readable, and supports scoped configuration per environment and role.

### 📦 Using One `group_vars` Root for All OTAP Environments

You can place all OTAP (Development, Test, Acceptance, Production) environments into a single `group_vars/` directory and represent each one as a **subfolder**. Inside each environment's folder, you can keep both `vars/` and `vault/` for clean separation of settings:

```
group_vars/
├── development/
│   ├── vars/main.yml
│   └── vault/secrets.yml
├── test/
│   ├── vars/main.yml
│   └── vault/secrets.yml
├── acceptance/
│   ├── vars/main.yml
│   └── vault/secrets.yml
├── production/
│   ├── vars/main.yml
│   └── vault/secrets.yml
```

This is **fully valid and recommended**. Ansible will load variables for hosts based on the group they belong to in the inventory. The folder name must match the group name used in your `inventory/hosts.yml`.

### 🔄 Can I go deeper — one folder per host under each OTAP environment?

Yes, a more granular structure is also **valid** where each environment contains folders named after its hosts:

```
group_vars/
├── development/
│   ├── db_d_dbbds1/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
│   ├── db_d_dbbds2/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
├── test/
│   ├── db_t_dbbds1/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
│   ├── db_t_dbbds2/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
├── acceptance/
│   ├── db_a_dbbds1/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
│   ├── db_a_dbbds2/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
├── production/
│   ├── db_p_dbbds1/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
│   ├── db_p_dbbds2/
│   │   ├── vars/main.yml
│   │   └── vault/secrets.yml
```

To make this work, you must match this folder structure with `inventory/hosts.yml`:

```yaml
all:
  children:
    development:
      hosts:
        db_d_dbbds1:
        db_d_dbbds2:
    test:
      hosts:
        db_t_dbbds1:
        db_t_dbbds2:
    acceptance:
      hosts:
        db_a_dbbds1:
        db_a_dbbds2:
    production:
      hosts:
        db_p_dbbds1:
        db_p_dbbds2:
```

This lets you customize secrets and config at the **host level** inside each OTAP environment.

---

## 🧩 2. `group_vars/all.yml`

### 📌 What it does:

Defines common variables applied to all hosts in the inventory.

### 🧠 Why it's important:

It centralizes values like `ansible_user`, SSH keys, or default packages.

### 🧾 Example:

```yaml
ansible_user: vagrant
ansible_ssh_private_key_file: .vagrant/machines/vm1/libvirt/private_key
```

...

\[remaining sections unchanged]
