# 🧰 Install Vagrant & Ansible on Debian 12 to Deploy RHEL8/CentOS8 PostgreSQL OTAP Cluster

This guide walks you through installing **Vagrant** and **Ansible** on **Debian 12 (used as a VDI)** to provision multiple **RHEL8/CentOS8** VMs for a full OTAP-based PostgreSQL Streaming Replication lab.

---

## ✅ Prerequisites

* Debian 12 desktop or VDI instance
* VirtualBox or libvirt installed
* sudo/root access
* Internet connection

---

## 🛠️ Step 1: Install Required Tools

### 🔧 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 📦 Install Vagrant

```bash
sudo apt install -y vagrant
```

### 📦 Install Ansible

```bash
sudo apt install -y ansible
```

---

## 📁 Vagrant Project Layout

### Recommended Directory Structure:

```
~/PostgreSQL-OTAP-Lab/
├── Vagrantfile
├── ansible/
│   ├── playbooks/
│   └── inventory/
│       ├── hosts.yaml
│       └── group_vars/
├── templates/
│   └── postgresql.conf.j2
├── scripts/
│   └── bootstrap.sh
└── roles/
    └── postgresql/
```

---

## 📜 YAML Inventory File: `inventory/hosts.yaml`

```yaml
all:
  children:
    A_Prim:
      hosts:
        A-Prim:
          ansible_host: 192.168.56.11
    A_Repl:
      hosts:
        A-Repl:
          ansible_host: 192.168.56.21
    O_Prim:
      hosts:
        O-Prim:
          ansible_host: 192.168.56.12
    O_Repl:
      hosts:
        O-Repl:
          ansible_host: 192.168.56.22
    T_Prim:
      hosts:
        T-Prim:
          ansible_host: 192.168.56.13
    T_Repl:
      hosts:
        T-Repl:
          ansible_host: 192.168.56.23
    P_Prim:
      hosts:
        P-Prim:
          ansible_host: 192.168.56.14
    P_Repl:
      hosts:
        P-Repl:
          ansible_host: 192.168.56.24
    Barman_Prim:
      hosts:
        Barman-Prim:
          ansible_host: 192.168.56.31
    Barman_Repl:
      hosts:
        Barman-Repl:
          ansible_host: 192.168.56.32
    RepoCertServer:
      hosts:
        RepoCertServer:
          ansible_host: 192.168.56.40
```

---

## 📄 Example Jinja2 Template: `templates/postgresql.conf.j2`

```jinja
# PostgreSQL Configuration Template
listen_addresses = '*'
port = {{ postgres_port | default(5432) }}
max_connections = {{ max_connections | default(100) }}
wal_level = replica
archive_mode = on
archive_command = 'rsync -a %p barman@{{ barman_host }}:{{ barman_archive_path }}/%f'
```

---

## 🖧 Using Libvirt Instead of VirtualBox

If you prefer **libvirt** over VirtualBox for improved performance and native KVM support, follow these steps:

### 🔧 Install Libvirt with Vagrant Support

```bash
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo apt install -y vagrant-libvirt
```

### 🔥 Enable & Start Libvirt

```bash
sudo systemctl enable --now libvirtd
sudo usermod -aG libvirt $USER
newgrp libvirt
```

### 📝 Example `Vagrantfile` for Libvirt

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "generic/centos8"
  nodes = ["A-Prim", "A-Repl"]

  nodes.each do |node|
    config.vm.define node do |node_config|
      node_config.vm.hostname = node
      node_config.vm.network "private_network", type: "dhcp"
      node_config.vm.provider "libvirt" do |lv|
        lv.memory = 2048
        lv.cpus = 2
      end
    end
  end
end
```

### ✅ Advantages of Libvirt

* Native KVM/QEMU virtualization
* Better performance for many VMs
* Efficient resource usage
* Can run headless without GUI

> 📝 Recommended for large-scale PostgreSQL OTAP replication environments.

---

## 🆚 VirtualBox vs Libvirt: Which Is Better for This Setup?

**VirtualBox** is more user-friendly and widely supported across platforms, making it a good choice for quick testing and basic Vagrant setups.

**Libvirt** is a better option for production-like environments or when running many VMs efficiently. It offers:

* Better performance and resource usage
* Native KVM/QEMU virtualization support
* Faster provisioning
* Advanced networking and storage options

### ✅ Recommendation:

If your Debian 12 VDI supports KVM, **libvirt** is better suited for running a large number of PostgreSQL replication nodes and services. However, VirtualBox remains easier to configure if you're just getting started.

---

## 🔁 Next Steps

* Create Ansible roles for:

  * PostgreSQL installation & replication setup
  * Barman configuration
  * Firewall, FreeIPA, Nginx, etc.
* Run Vagrant with:

```bash
vagrant up
```

* Connect to a specific node:

```bash
vagrant ssh A-Prim
```

* Run Ansible playbook:

```bash
ansible-playbook -i inventory/hosts.yaml playbooks/setup_postgresql.yml
```

---

## ✅ Done

You now have a VDI-based setup using Vagrant + Ansible on Debian 12 to deploy a full OTAP PostgreSQL Streaming Replication environment with backups, certificate servers, and external services.
