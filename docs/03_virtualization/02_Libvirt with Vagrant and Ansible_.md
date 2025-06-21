# libvirt For Multiple VMs on Linux

## 🧾 Overview

**Libvirt** is an open-source API and management tool for virtualization platforms, mainly KVM/QEMU. It provides a consistent interface for managing multiple virtual machines across Linux systems.

This document provides a practical guide for setting up and managing **multiple VMs** using `libvirt`, with integration of **Vagrant** and **Ansible**.

---

## 🚀 Full Setup Workflow: Libvirt + Vagrant + Ansible

### 1️⃣ Install Vagrant

```bash
sudo apt install -y vagrant
```

Install the libvirt plugin:

```bash
vagrant plugin install vagrant-libvirt
```

---

### 2️⃣ Install Ansible

```bash
sudo apt install -y ansible
```

Install the libvirt collection:

```bash
ansible-galaxy collection install community.libvirt
```

---

### 3️⃣ Install libvirt and KVM

```bash
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients virt-manager bridge-utils
```

Add your user to the appropriate groups:

```bash
sudo usermod -aG libvirt $(whoami)
sudo usermod -aG kvm $(whoami)
newgrp libvirt
```

---

### 4️⃣ Run libvirt GUI (virt-manager)

```bash
virt-manager
```

This opens a graphical interface for managing VMs with drag-and-drop ISO creation, network management, and VM monitoring.

---

### 5️⃣ Use Ansible + Vagrant + libvirt to Create Multiple VMs

#### A. Define your `Vagrantfile` to bootstrap multiple VMs:

```ruby
Vagrant.configure("2") do |config|
  (1..3).each do |i|
    config.vm.define "vm#{i}" do |vm|
      vm.vm.box = "debian/bookworm64"
      vm.vm.hostname = "vm#{i}"
      vm.vm.provider :libvirt do |lv|
        lv.memory = 1024
        lv.cpus = 1
      end
    end
  end
end
```

Run:

```bash
vagrant up --provider=libvirt
```

#### B. Use Ansible to provision those VMs

1. Create an Ansible inventory:

```ini
[vms]
vm1 ansible_host=192.168.122.101
vm2 ansible_host=192.168.122.102
vm3 ansible_host=192.168.122.103
```

2. Example playbook:

```yaml
- name: Provision all Vagrant-libvirt VMs
  hosts: vms
  become: true
  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
```

3. Run the playbook:

```bash
ansible-playbook -i inventory.ini provision.yml
```

---

## 📦 Installation on Debian/Ubuntu

```bash
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients virt-manager bridge-utils
```

Ensure your user is in the `libvirt` and `kvm` groups:

```bash
sudo usermod -aG libvirt $(whoami)
sudo usermod -aG kvm $(whoami)
newgrp libvirt
```

---

## 🖥️ Launch GUI Manager (Optional)

```bash
virt-manager
```

This launches the Virtual Machine Manager GUI for easier VM creation and control.

...

\[rest of the document continues unchanged]
