# 🧰 Install Vagrant & Ansible on Debian 12 to Deploy RHEL8/CentOS8 PostgreSQL OTAP Cluster

This guide walks you through installing **Vagrant** and **Ansible** on **Debian 12 (used as a VDI)** to provision multiple **RHEL8/CentOS8** VMs for a full OTAP-based PostgreSQL Streaming Replication lab.

...

### 📌 Optional: Make It Permanent

Get UUID:

```bash
sudo blkid
```

From the output in your terminal, the correct UUID for the new formatted partition `/dev/nvme0n1p3` is:

```bash
UUID="ed1d28e3-739e-44be-b71e-275dedf21827"
```

Add this line to your `/etc/fstab` to ensure the partition auto-mounts at boot:

```ini
UUID=ed1d28e3-739e-44be-b71e-275dedf21827 /mnt/data ext4 defaults 0 2
```

To verify it's mounted correctly without rebooting:

```bash
sudo mount -a
ls /mnt/data
```

If the folder already exists (`mkdir: cannot create directory '/mnt/data': File exists`), that’s fine — it means the path is ready to be used.

> ✅ **You’ve successfully formatted and mounted a previously NTFS partition from your old Windows install, and it's ready to use in your PostgreSQL lab!**

...

## ✅ Done

You now have a VDI-based setup using Vagrant + Ansible on Debian 12 to deploy a full OTAP PostgreSQL Streaming Replication environment with backups, certificate servers, and external services.

> 💡 Tip: If your system cannot support 12+ VMs concurrently, consider staging them in groups or running only a subset of OTAP nodes at a time for development and testing.
