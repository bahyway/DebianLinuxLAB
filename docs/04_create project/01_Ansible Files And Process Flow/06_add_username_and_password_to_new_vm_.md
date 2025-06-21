# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🗄️ PostgreSQL Primary & Replica Structure for All OTAP Environments

... *(existing content unchanged)* ...

### 🗂️ Sample `inventory/hosts.yml` for OTAP PostgreSQL Cluster

... *(existing content unchanged)* ...

### ✅ Updated Minimal Example (One VM at a Time)

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "centos/8"

  nodes = {
    "db_d_dbbds1_prim" => "192.168.56.11"
  }

  nodes.each do |name, ip|
    config.vm.define name do |node|
      node.vm.hostname = name.gsub('_', '-')
      node.vm.network "private_network", ip: ip
      node.vm.provider :libvirt do |v|
        v.memory = 1024
        v.cpus = 1
      end

      # Set default user and password
      node.vm.provision "shell", inline: <<-SHELL
        useradd -m vagrantuser
        echo "vagrantuser:vagrantpass" | chpasswd
        usermod -aG wheel vagrantuser
        echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel
      SHELL
    end
  end
end
```

### 🔄 Destroy and Recreate VM to Apply Username/Password Updates

To recreate a VM after updating its configuration (e.g. username or password), follow these steps:

1. **Destroy the current VM**:

   ```bash
   vagrant destroy db_d_dbbds1_prim --provider=libvirt -f
   ```

   > `-f` forces the destruction without asking for confirmation.

2. **Recreate the VM with updated provisioning**:

   ```bash
   vagrant up db_d_dbbds1_prim --provider=libvirt
   ```

   This will apply the latest changes in the Vagrantfile, including the updated username/password setup.

> 🔁 Repeat the process for any VM whose settings you’ve updated.

---

### 🔐 Setting Username & Password for VMs

To set a default **username and password** for new VMs created by Vagrant and Libvirt, you can use a shell provisioner block inside the VM definition:

```ruby
node.vm.provision "shell", inline: <<-SHELL
  useradd -m vagrantuser
  echo "vagrantuser:vagrantpass" | chpasswd
  usermod -aG wheel vagrantuser
  echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel
SHELL
```

This creates:

* A user `vagrantuser`
* With password `vagrantpass`
* Adds user to `wheel` group for sudo
* Enables passwordless sudo

> 💡 You can adjust this with variables from your Ansible `group_vars` or turn it into an Ansible task instead of shell provisioning.

Let me know if you'd like to fully migrate this logic to your Ansible role instead.
