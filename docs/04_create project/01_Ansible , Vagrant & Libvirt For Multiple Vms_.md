# Ansible, Vagrant & Libvirt for Multiple VMs

## 🗂️ Project Structure (Best Practice)

This is a recommended layout for using **Ansible**, **Vagrant**, and **libvirt** together to manage multiple virtual machines:

```
project-root/
├── Vagrantfile
├── inventory/
│   └── hosts.yml
├── group_vars/
│   ├── all.yml
│   └── nginx.yml
├── roles/
│   ├── common/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── templates/
│   │       └── motd.j2
│   └── nginx/
│       ├── tasks/
│       │   └── main.yml
│       └── templates/
│           └── nginx.conf.j2
├── site.yml
└── README.md
```

---

## 📦 Step-by-Step Setup

### 1️⃣ `Vagrantfile` - Create First VM (Scalable to More)

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "vm1" do |vm1|
    vm1.vm.box = "debian/bookworm64"
    vm1.vm.hostname = "vm1"
    vm1.vm.provider :libvirt do |lv|
      lv.memory = 1024
      lv.cpus = 1
    end
  end
end
```

> 🧠 **Scalability Note**: You can safely extend to more VMs later by adding blocks like `vm2`, `vm3`, etc., without recreating `vm1`.

---

### 2️⃣ `inventory/hosts.yml`

```yaml
all:
  children:
    vms:
      hosts:
        vm1:
          ansible_host: 192.168.122.101
```

---

### 3️⃣ `group_vars/all.yml`

```yaml
ansible_user: vagrant
ansible_ssh_private_key_file: .vagrant/machines/vm1/libvirt/private_key
```

---

### 4️⃣ `roles/common/tasks/main.yml`

```yaml
- name: Set a custom Message of the Day
  template:
    src: motd.j2
    dest: /etc/motd
```

---

### 5️⃣ `roles/common/templates/motd.j2`

```jinja
Welcome to {{ inventory_hostname }} provisioned by Ansible!
```

---

### 6️⃣ `roles/nginx/tasks/main.yml`

```yaml
- name: Install Nginx
  apt:
    name: nginx
    state: present

- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

- name: Ensure Nginx is running
  service:
    name: nginx
    state: started
    enabled: true
```

---

### 7️⃣ `roles/nginx/templates/nginx.conf.j2`

```jinja
user www-data;
worker_processes auto;
pid /run/nginx.pid;
events { worker_connections 1024; }
http {
    server {
        listen 80;
        server_name {{ inventory_hostname }};
        location / {
            return 200 'Hello from {{ inventory_hostname }}';
        }
    }
}
```

---

### 8️⃣ `site.yml` - Main Playbook

```yaml
- name: Configure all VMs
  hosts: vms
  become: true
  roles:
    - common
    - nginx
```

---

## ✅ Running the Setup

1. Start the first VM:

```bash
vagrant up --provider=libvirt
```

2. Run the Ansible playbook:

```bash
ansible-playbook -i inventory/hosts.yml site.yml
```

---

## 🔁 Adding More VMs Later

Just edit the `Vagrantfile`:

```ruby
config.vm.define "vm2" do |vm2|
  vm2.vm.box = "debian/bookworm64"
  vm2.vm.hostname = "vm2"
  vm2.vm.provider :libvirt do |lv|
    lv.memory = 1024
    lv.cpus = 1
  end
end
```

Update the inventory as well, then run:

```bash
vagrant up vm2
ansible-playbook -i inventory/hosts.yml site.yml
```

---

## 📚 References

* [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
* [vagrant-libvirt Plugin](https://github.com/vagrant-libvirt/vagrant-libvirt)
* [libvirt.org](https://libvirt.org)
