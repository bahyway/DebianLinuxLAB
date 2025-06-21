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

## ⚙️ VM Base Image and Creation Strategy

All VMs will be **minimal servers** (no GUI) based on **RHEL 8**. However, due to subscription limitations, **CentOS 8** will be used as a substitute.

> 🧠 **Performance Tip**: It is safer to create and provision VMs **one-by-one** instead of all at once to prevent system crashes, especially on lower-spec Debian 12 VDIs.

---

## 📊 Performance Benchmark Checklist

Use this checklist to evaluate your Debian12 VDI before adding more VMs:

* [ ] Check available RAM: `free -h`
* [ ] Check CPU load: `uptime` or `top`
* [ ] Check disk I/O: `iostat` or `iotop`
* [ ] Ensure virtualization support: `egrep -c '(vmx|svm)' /proc/cpuinfo`
* [ ] Monitor current libvirt usage: `virsh list --all`
* [ ] Use `vagrant status` before adding more VMs

> ✅ Recommendation: For systems with ≤ 8GB RAM, keep total active VMs ≤ 3.

---

## 📁 GitHub Repository Scaffold

To publish this project as a GitHub repository:

1. Initialize Git:

```bash
cd project-root/
git init
git add .
git commit -m "Initial commit: Ansible + Vagrant + Libvirt VM setup"
```

2. Push to GitHub:

```bash
git remote add origin https://github.com/your-username/ansible-libvirt-vms.git
git push -u origin main
```

3. Optionally add a `.gitignore`:

```
.vagrant/
*.retry
*.log
*.swp
```

4. Include a `README.md`:

```markdown
# Ansible + Vagrant + Libvirt Minimal VM Infrastructure
This project automates the creation of CentOS 8 minimal VMs using libvirt, managed via Vagrant, and configured using Ansible.
```

> 🧠 Consider adding GitHub Actions later to run `ansible-lint` or `vagrant validate`.

---

## 📦 Step-by-Step Setup

### 1️⃣ `Vagrantfile` - Create First VM (Scalable to More)

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "vm1" do |vm1|
    vm1.vm.box = "centos/8"
    vm1.vm.hostname = "vm1"
    vm1.vm.provider :libvirt do |lv|
      lv.memory = 1024
      lv.cpus = 1
    end
  end
end
```

> ✅ You can extend this to multiple VMs, but for stability, test one at a time on modest hardware.

...

\[remaining sections unchanged]
