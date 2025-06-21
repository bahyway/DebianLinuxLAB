# Understanding Ansible Project Files and Execution Flow

This document explains each core file used in an Ansible + Vagrant + Libvirt multi-VM setup and outlines the **execution flow** starting from Ansible all the way to provisioning VMs.

...

### 🗄️ PostgreSQL Primary & Replica Structure for All OTAP Environments

... *(existing content unchanged)* ...

### 🗂️ Sample `inventory/hosts.yml` for OTAP PostgreSQL Cluster

Below is an example of a valid Ansible inventory layout with static IPv4 assignments for all PostgreSQL nodes across OTAP environments:

```yaml
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
```

> ❗ **Vagrant Hostname Rules:**
>
> The error message:
>
> ```
> The hostname set for the VM 'db_d_dbbds1_prim' should only contain letters, numbers, hyphens or dots. It cannot start with a hyphen or dot.
> ```
>
> ✅ The name `db_d_dbbds1_prim` is valid because it follows these rules:
>
> * Begins with a letter
> * Contains only lowercase letters, underscores, and numbers
> * **BUT**, `libvirt` might reject underscores `_` in the `hostname` field
>
> ✅ **Fix:** Use hyphens (`-`) instead of underscores in hostnames for compatibility:
>
> ```ruby
> node.vm.hostname = name.gsub('_', '-')
> ```
>
> This will convert `db_d_dbbds1_prim` → `db-d-dbbds1-prim`, making it fully compliant.

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
    end
  end
end
```

> ✅ This structure now avoids the `libvirt` hostname error and works correctly.

Let me know if you'd like to refactor your JSON structure too to follow the hyphenated hostname pattern for full libvirt compatibility.
