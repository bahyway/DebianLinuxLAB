# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🗄️ PostgreSQL Primary & Replica Structure for All OTAP Environments

... *(existing content unchanged)* ...

### 🗂️ Sample `inventory/hosts.yml` for OTAP PostgreSQL Cluster

Below is an example of a valid Ansible inventory layout with static IPv4 assignments for all PostgreSQL nodes across OTAP environments:

````yaml
all:
  children:
    development:
      children:
        db_d_dbbds1:
          hosts:
            db_d_dbbds1_prim:
              ansible_host: 192.168.56.11
            db_d_dbbds1_repl:
              ansible_host: 192.168.56.12
        db_d_dbbds2:
          hosts:
            db_d_dbbds2_prim:
              ansible_host: 192.168.56.13
            db_d_dbbds2_repl:
              ansible_host: 192.168.56.14

    test:
      children:
        db_t_dbbds1:
          hosts:
            db_t_dbbds1_prim:
              ansible_host: 192.168.56.21
            db_t_dbbds1_repl:
              ansible_host: 192.168.56.22
        db_t_dbbds2:
          hosts:
            db_t_dbbds2_prim:
              ansible_host: 192.168.56.23
            db_t_dbbds2_repl:
              ansible_host: 192.168.56.24

    acceptance:
      children:
        db_a_dbbds1:
          hosts:
            db_a_dbbds1_prim:
              ansible_host: 192.168.56.31
            db_a_dbbds1_repl:
              ansible_host: 192.168.56.32
        db_a_dbbds2:
          hosts:
            db_a_dbbds2_prim:
              ansible_host: 192.168.56.33
            db_a_dbbds2_repl:
              ansible_host: 192.168.56.34

    production:
      children:
        db_p_dbbds1:
          hosts:
            db_p_dbbds1_prim:
              ansible_host: 192.168.56.41
            db_p_dbbds1_repl:
              ansible_host: 192.168.56.42
        db_p_dbbds2:
          hosts:
            db_p_dbbds2_prim:
              ansible_host: 192.168.56.43
            db_p_dbbds2_repl:
              ansible_host: 192.168.56.44
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
````

Each `host:` entry must resolve either by DNS or be mapped via `/etc/hosts` or Vagrant private IP provisioning.

### 💡 Where and How to Specify Each VM's IPv4 Address

To bind hostnames like `db_d_dbbds1_prim` to real IPs, you can:

1. **Static Inventory IP Declaration**:
   Extend each host in `inventory/hosts.yml` like so:

   ```yaml
   db_d_dbbds1_prim:
     ansible_host: 192.168.56.11
   db_d_dbbds1_repl:
     ansible_host: 192.168.56.12
   ```

2. **Set in Vagrantfile**:
   If VMs are created via Vagrant, define static private networks per VM:

   ```ruby
   config.vm.define "db_d_dbbds1_prim" do |node|
     node.vm.hostname = "db_d_dbbds1_prim"
     node.vm.network "private_network", ip: "192.168.56.11"
   end
   ```

3. **DNS or /etc/hosts Resolution**:
   Manually bind names to IPs on the Ansible control node (Debian12 VDI):

   ```
   192.168.56.11 db_d_dbbds1_prim
   192.168.56.12 db_d_dbbds1_repl
   ```

> ✅ Best Practice: Define `ansible_host` under each host entry in `hosts.yml` for portability, even if using Vagrant. It gives full control regardless of provisioning method.

Let me know if you'd like a sample full `hosts.yml` with embedded IPs.

Let me know if you want to generate a dynamic script to build the `inventory/hosts.yml` file from the JSON structure as well.

### 📦 Sample `Vagrantfile` for All OTAP PostgreSQL VMs

Below is a sample `Vagrantfile` that provisions all OTAP nodes defined in the inventory, matching each hostname to its corresponding IPv4 address:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "centos/8"

  nodes = {
    "db_d_dbbds1_prim" => "192.168.56.11",
    "db_d_dbbds1_repl" => "192.168.56.12",
    "db_d_dbbds2_prim" => "192.168.56.13",
    "db_d_dbbds2_repl" => "192.168.56.14",

    "db_t_dbbds1_prim" => "192.168.56.21",
    "db_t_dbbds1_repl" => "192.168.56.22",
    "db_t_dbbds2_prim" => "192.168.56.23",
    "db_t_dbbds2_repl" => "192.168.56.24",

    "db_a_dbbds1_prim" => "192.168.56.31",
    "db_a_dbbds1_repl" => "192.168.56.32",
    "db_a_dbbds2_prim" => "192.168.56.33",
    "db_a_dbbds2_repl" => "192.168.56.34",

    "db_p_dbbds1_prim" => "192.168.56.41",
    "db_p_dbbds1_repl" => "192.168.56.42",
    "db_p_dbbds2_prim" => "192.168.56.43",
    "db_p_dbbds2_repl" => "192.168.56.44"
  }

  nodes.each do |name, ip|
    config.vm.define name do |node|
      node.vm.hostname = name
      node.vm.network "private_network", ip: ip
      node.vm.provider :libvirt do |v|
        v.memory = 1024
        v.cpus = 1
      end
    end
  end
end
```

> 💡 This Vagrantfile assumes you're using CentOS 8 minimal. Adjust box name and resources (memory, CPUs) as needed.

Let me know if you'd like a shell script to auto-generate this `Vagrantfile` from JSON.
