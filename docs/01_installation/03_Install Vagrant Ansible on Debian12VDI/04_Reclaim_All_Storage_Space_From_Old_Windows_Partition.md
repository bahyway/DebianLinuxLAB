# 🧰 Install Vagrant & Ansible on Debian 12 to Deploy RHEL8/CentOS8 PostgreSQL OTAP Cluster

This guide walks you through installing **Vagrant** and **Ansible** on **Debian 12 (used as a VDI)** to provision multiple **RHEL8/CentOS8** VMs for a full OTAP-based PostgreSQL Streaming Replication lab.

---

## ✅ Prerequisites

* Debian 12 desktop or VDI instance
* VirtualBox or libvirt installed
* sudo/root access
* Internet connection

> ❗ **Note:** Some users have experienced system crashes when running Vagrant with VirtualBox on Windows 10 WSL boxes. In such cases, using Debian 12 directly with libvirt can provide improved stability and performance.

---

## 🖥️ System Specification Check

You can use the following command to generate a full report and verify whether your hardware can support a 12+ VM OTAP replication setup:

```bash
sudo apt install -y inxi
inxi -Fz > system_report.txt
```

You shared the following relevant system specs:

* **CPU**: Intel Core i7-6700HQ (4 cores / 8 threads, 2.6–3.5 GHz)
* **RAM**: 16 GB (currently 85% used)
* **Storage**: 1.36 TB (NVMe + HDD), 40 GB used
* **Virtualization**: Intel VT-x supported (KVM compatible)
* **GPU**: Intel HD 530 + NVIDIA GTX 960M (using nouveau)
* **Kernel**: 6.1.0-37-amd64
* **Display**: Wayland / GNOME 43.9

### 🧠 Capacity Assessment

* ✅ **CPU** is strong enough to handle 6–8 VMs concurrently
* ✅ **RAM** is sufficient for light to medium PostgreSQL instances (each VM \~1–1.5 GB)
* ✅ **Storage** (especially NVMe) can support fast I/O for WAL replication
* ⚠️ **Running 12+ VMs at once may require memory optimization or VM batching**

### 💡 Recommendation

To avoid system overload:

* Run OTAP Prim and Repl in separate sessions (staging in batches)
* Use libvirt with KVM for better performance and resource efficiency
* Avoid GUI-heavy VMs — stick with minimal RHEL/CentOS installs
* Consider increasing swap space or offloading heavy operations to a secondary node

---

## 📋 Generate Quick Hardware Summary (Optional)

```bash
lscpu && free -h && df -h
```

This displays:

* CPU cores and virtualization flags
* RAM usage
* Disk layout and free space

---

## 🧹 Reclaim Full Disk Space from Old Windows Partitions

If your laptop still contains partitions from a previous Windows installation, you can reclaim the storage and use it entirely for Debian 12. **Proceed with caution—this process is destructive.**

### 🔍 Step 1: Identify Partitions

```bash
lsblk
sudo fdisk -l
```

Look for partitions labeled as `ntfs` or clearly marked for Windows (e.g., `/dev/sda3` with label `Windows`).

### 💣 Step 2: Delete Old Windows Partitions

Use `gparted` (GUI) or `cfdisk` (CLI):

```bash
sudo apt install -y gparted
sudo gparted
```

* Select your disk (e.g., `/dev/sda`)
* Delete the Windows partitions (typically NTFS)
* Apply the changes

### 🧱 Step 3: Expand Existing Linux Partition

Still using `gparted`, right-click your main Linux (`ext4`) partition and choose **Resize/Move** to fill the unallocated space.

### 🆗 Step 4: Confirm Filesystem Integrity

```bash
sudo resize2fs /dev/sdXn   # Replace with actual partition
```

### 🧾 Final Check

```bash
df -h
```

You should now see increased space available under `/home` or `/`.

> 🛑 **Backup your system before modifying partitions!**

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

...

## ✅ Done

You now have a VDI-based setup using Vagrant + Ansible on Debian 12 to deploy a full OTAP PostgreSQL Streaming Replication environment with backups, certificate servers, and external services.

> 💡 Tip: If your system cannot support 12+ VMs concurrently, consider staging them in groups or running only a subset of OTAP nodes at a time for development and testing.
