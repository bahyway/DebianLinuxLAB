# 🔐 Ansible and SSH: Logging into Vagrant+Libvirt VMs from Debian12 VDI

This document explains how to securely login from your **Debian12 VDI host** into newly created Vagrant-managed virtual machines using SSH, and how it relates to Ansible automation.

---

## 🧩 Prerequisites

Ensure:

* VMs are created with SSH enabled
* User has valid credentials (username/password or SSH key)
* VMs have private IP addresses assigned (e.g. `192.168.56.x`)

---

## 📂 Example Vagrant Setup Recap

If your VM was created with the following provisioner:

```ruby
node.vm.provision "shell", inline: <<-SHELL
  useradd -m vagrantuser
  echo "vagrantuser:vagrantpass" | chpasswd
  usermod -aG wheel vagrantuser
  echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel
SHELL
```

Then the username is `vagrantuser`, password is `vagrantpass`.

---

## 🔐 Login via SSH (Manual)

From your Debian12 VDI:

```bash
ssh vagrantuser@192.168.56.11
```

Enter password: `vagrantpass`

If you prefer using SSH key authentication:

### 🔑 Generate an SSH Key

```bash
ssh-keygen -t rsa -b 4096 -C "vagrantuser@debian12"
```

* Save to: `~/.ssh/id_rsa`

### 🚀 Copy Public Key to VM (Manually or via Vagrant provisioner)

```bash
ssh-copy-id vagrantuser@192.168.56.11
```

---

## 🧪 Test SSH Connectivity

To confirm Ansible can connect:

```bash
ansible all -i inventory/hosts.yml -m ping
```

> Ensure your Ansible inventory points to the correct IP and uses `ansible_user: vagrantuser`

---

## ✅ Ansible Inventory Example

```yaml
all:
  hosts:
    db_d_dbbds1_prim:
      ansible_host: 192.168.56.11
      ansible_user: vagrantuser
      ansible_ssh_pass: vagrantpass  # Or use ansible_ssh_private_key_file
```

---

## 🎯 Best Practices

* ✅ Use SSH keys instead of plain passwords
* ✅ Use Ansible Vault to store secrets
* ✅ Set up SSH config in `~/.ssh/config` for easier host aliasing

---

Let me know if you'd like:

* A script to auto-copy SSH keys to all VMs
* An SSH config template
* Ansible Vault integration
