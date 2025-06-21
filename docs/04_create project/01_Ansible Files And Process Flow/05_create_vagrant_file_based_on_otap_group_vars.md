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

1. **Static Inventory IP Declaration**: Extend each host in `inventory/hosts.yml` like so:

   ```yaml
   db_d_dbbds1_prim:
     ansible_host: 192.168.56.11
   db_d_dbbds1_repl:
     ansible_host: 192.168.56.12
   ```

2. **Set in Vagrantfile**: If VMs are created via Vagrant, define static private networks per VM:

   ```ruby
   config.vm.define "db_d_dbbds1_prim" do |node|
     node.vm.hostname = "db_d_dbbds1_prim"
     node.vm.network "private_network", ip: "192.168.56.11"
   end
   ```

3. **DNS or /etc/hosts Resolution**: Manually bind names to IPs on the Ansible control node (Debian12 VDI):

   ```
   192.168.56.11 db_d_dbbds1_prim
   192.168.56.12 db_d_dbbds1_repl
   ```

> ✅ Best Practice: Define `ansible_host` under each host entry in `hosts.yml` for portability, even if using Vagrant. It gives full control regardless of provisioning method.

Let me know if you'd like a sample full `hosts.yml` with embedded IPs.

Let me know if you want to generate a dynamic script to build the `inventory/hosts.yml` file from the JSON structure as well.

### 📦 Sample `Vagrantfile` for All OTAP PostgreSQL VMs

#### ✅ Running One VM at a Time (Valid Minimal Example)

Yes, it's valid to comment out most VMs and run just one for development or testing. Here's an example:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "centos/8"

  nodes = {
    "db_d_dbbds1_prim" => "192.168.56.11"
    # "db_d_dbbds1_repl" => "192.168.56.12",
    # "db_d_dbbds2_prim" => "192.168.56.13",
    # "db_d_dbbds2_repl" => "192.168.56.14",
    # ... (other nodes)
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

> ⚠️ This method is helpful to conserve resources or test provisioning. Just uncomment more nodes as needed.

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

### 🛠️ Shell Script to Generate `Vagrantfile` from JSON

Save the JSON structure into a file like `vm_config.json` (keys = node names, values = IPs), then use this script:

```bash
#!/bin/bash

JSON_FILE="vm_config.json"
VAGRANTFILE="Vagrantfile"
BOX="centos/8"

cat <<EOF > $VAGRANTFILE
Vagrant.configure("2") do |config|
  config.vm.box = "$BOX"
EOF

jq -r 'to_entries[] | "  config.vm.define \"\(.key)\" do |node|
    node.vm.hostname = \"\(.key)\"
    node.vm.network \"private_network\", ip: \"\(.value)\"
    node.vm.provider :libvirt do |v|
      v.memory = 1024
      v.cpus = 1
    end
  end"' $JSON_FILE >> $VAGRANTFILE

echo "end" >> $VAGRANTFILE
```

> ✅ Requires `jq`. Install with: `sudo apt install jq`

You can generate `vm_config.json` from the same source as `hosts.yml`.

Let me know if you'd like to add this script and JSON file to your project automatically.

### ▶️ How to Run the Vagrantfile

Given your current project structure:

```
project-root/
├── ansible/
│   └── inventory/hosts.yml
├── create_local_project/
│   └── create_group_vars_for_otap_final.json (and other scripts)
├── docs/ (documentation)
├── vagrant/
│   └── vagrantfile
```

To run the `Vagrantfile` and provision your VMs:

1. **Navigate to the Vagrant directory:**

   ```bash
   cd vagrant
   ```

2. **Ensure your system has the required tools installed:**

   * `vagrant` → Installed from official website
   * `vagrant-libvirt` plugin → Install via `vagrant plugin install vagrant-libvirt`
   * `libvirt` with QEMU/KVM → Installed via `sudo apt install libvirt-daemon-system libvirt-clients virtinst`
   * User is in `libvirt` group → Add with `sudo usermod -aG libvirt $(whoami)` and restart session

3. **Run the provisioning:**

   ```bash
   vagrant up --provider=libvirt
   ```

4. **Verify VMs:**

   ```bash
   vagrant status
   virsh list --all
   ```

> ⚠️ Your current path to the Vagrantfile is `vagrant/vagrantfile`, so make sure to `cd vagrant/` before running `vagrant up`.

---

### 🧾 Example `vm_config.json`

Here is the JSON file used to generate the `Vagrantfile` automatically:

```json
{
  "db_d_dbbds1_prim": "192.168.56.11",
  "db_d_dbbds1_repl": "192.168.56.12",
  "db_d_dbbds2_prim": "192.168.56.13",
  "db_d_dbbds2_repl": "192.168.56.14",

  "db_t_dbbds1_prim": "192.168.56.21",
  "db_t_dbbds1_repl": "192.168.56.22",
  "db_t_dbbds2_prim": "192.168.56.23",
  "db_t_dbbds2_repl": "192.168.56.24",

  "db_a_dbbds1_prim": "192.168.56.31",
  "db_a_dbbds1_repl": "192.168.56.32",
  "db_a_dbbds2_prim": "192.168.56.33",
  "db_a_dbbds2_repl": "192.168.56.34",

  "db_p_dbbds1_prim": "192.168.56.41",
  "db_p_dbbds1_repl": "192.168.56.42",
  "db_p_dbbds2_prim": "192.168.56.43",
  "db_p_dbbds2_repl": "192.168.56.44"
}
```

> 💡 This file can be versioned, reused, or transformed into `hosts.yml` or `group_vars` as needed.
