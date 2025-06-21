# libvirt For Multiple VMs on Linux

## 🧾 Overview

**Libvirt** is an open-source API and management tool for virtualization platforms, mainly KVM/QEMU. It provides a consistent interface for managing multiple virtual machines across Linux systems.

This document provides a practical guide for setting up and managing **multiple VMs** using `libvirt`.

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

---

## 🛠️ CLI Management with `virsh`

### List all VMs:

```bash
virsh list --all
```

### Start/Shutdown VMs:

```bash
virsh start vm_name
virsh shutdown vm_name
```

### Define and Create a VM:

```bash
virt-install \
  --name debian-vm1 \
  --ram 2048 \
  --vcpus=2 \
  --os-type=linux \
  --os-variant=debian11 \
  --disk path=/var/lib/libvirt/images/debian-vm1.qcow2,size=10 \
  --graphics none \
  --console pty,target_type=serial \
  --location 'http://deb.debian.org/debian/dists/bookworm/main/installer-amd64/' \
  --extra-args 'console=ttyS0,115200n8 serial'
```

---

## ⚙️ Storage and Networking

### Create Storage Volumes:

```bash
virsh vol-create-as default debian-vm2.qcow2 10G --format qcow2
```

### Use Bridged Networking:

1. Create a bridge interface:

```bash
sudo nmcli connection add type bridge autoconnect yes con-name br0 ifname br0
sudo nmcli connection add type ethernet slave-type bridge con-name bridge-slave ifname enp1s0 master br0
```

2. Restart networking:

```bash
sudo nmcli connection up br0
```

3. Attach to VM:

```bash
virsh attach-interface vm_name network br0 --model virtio --config --live
```

---

## 🧰 Automating Multiple VMs

You can automate VM creation using shell scripts or Ansible.

### Example Shell Script:

```bash
#!/bin/bash
for i in {1..5}; do
  virt-install --name vm$i \
    --ram 1024 \
    --vcpus 1 \
    --disk path=/var/lib/libvirt/images/vm$i.qcow2,size=8 \
    --os-variant=generic \
    --network network=default \
    --graphics none \
    --location 'http://deb.debian.org/debian/dists/bookworm/main/installer-amd64/' \
    --extra-args 'console=ttyS0,115200n8 serial' \
    --noautoconsole
 done
```

---

## 🔄 Integrating libvirt with Vagrant and Ansible

### ✅ Vagrant with libvirt

To use `libvirt` as the provider for **Vagrant**:

1. Install required plugins:

```bash
vagrant plugin install vagrant-libvirt
```

2. Sample `Vagrantfile`:

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "vm1" do |vm1|
    vm1.vm.box = "debian/bookworm64"
    vm1.vm.provider :libvirt do |lv|
      lv.memory = 1024
      lv.cpus = 1
    end
  end
end
```

3. Launch VMs:

```bash
vagrant up --provider=libvirt
```

### ✅ Ansible with libvirt

Use the `community.libvirt.libvirt` collection:

```bash
ansible-galaxy collection install community.libvirt
```

Sample playbook to define a VM:

```yaml
- name: Create KVM VM using libvirt
  hosts: localhost
  connection: local
  tasks:
    - name: Define VM
      community.libvirt.libvirt_domain:
        name: vm1
        memory: 1024
        vcpu: 1
        disk:
          - name: vm1.qcow2
            size: 8
            pool: default
        network:
          - network: default
        state: running
```

---

## 🧪 Useful Tools

* `virt-manager`: GUI for VM creation
* `virt-viewer`: lightweight remote viewer
* `cockpit`: web UI that includes a `libvirt` module
* `ansible`: can control VMs with `community.libvirt.libvirt` collection
* `vagrant`: can use `vagrant-libvirt` plugin to manage VMs with provisioning support

---

## 📌 Best Practices

* Use `qcow2` format for snapshots and compression.
* Backup XML definitions: `virsh dumpxml vm_name > vm_name.xml`
* Use bridged networking for VM-to-LAN communication.
* Use LVM or ZFS for performance storage if hosting many VMs.
* Use Ansible for idempotent VM deployment and Vagrant for reproducible development environments.

---

## 📚 References

* [Libvirt Docs](https://libvirt.org/)
* [Virt-install](https://linux.die.net/man/1/virt-install)
* [Debian Cloud Images](https://cloud.debian.org/images/cloud/)
* [Cockpit Project](https://cockpit-project.org/)
* [Ansible Libvirt Collection](https://docs.ansible.com/ansible/latest/collections/community/libvirt/)
* [vagrant-libvirt plugin](https://github.com/vagrant-libvirt/vagrant-libvirt)
