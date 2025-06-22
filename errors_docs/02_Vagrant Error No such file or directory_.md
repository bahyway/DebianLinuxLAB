# Ansible and SSH

This document explains how to log in via SSH from Debian 12 VDI into newly created VMs and how to manage SSH keys for secure authentication.

---

## 🔐 SSH Login from Debian12 VDI to VMs

If you've created a VM with username `vagrantuser` and password `vagrantpass` (or your own custom user):

### Option 1: Password-based Login

```bash
ssh vagrantuser@192.168.56.11
```

When prompted, enter the password:

```
vagrantpass
```

### Option 2: SSH Key-based Login

1. Generate SSH Key:

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   # or better:
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Accept default location `~/.ssh/id_ed25519` or `~/.ssh/id_rsa`.
3. Copy your public key to the VM:

   ```bash
   ssh-copy-id vagrantuser@192.168.56.11
   ```

> 🔑 After this, you can SSH without password prompts.

---

## 🔐 Ed25519 Token Prefix

When generating an SSH key using the **Ed25519** algorithm, the public key starts with:

```
ssh-ed25519
```

### Example:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJN2f+1UcVfGHfJHTl8UgxFx9LtTwUVdf... your_email@example.com
```

* The `ssh-ed25519` prefix confirms it's using the Ed25519 elliptic-curve signature algorithm.
* It's secure, fast, and widely supported by modern SSH servers and Git platforms.

---

## 🛠️ Troubleshooting: Permission Denied (publickey,...)

If you get this error:

```
Permission denied (publickey,gssapi-keyex,gssapi-with-mic)
```

Make sure the VM has your public key added and the SSH daemon allows login.

### ✅ Fix in Vagrantfile Provisioning Block:

Add the following in the VM definition block in `Vagrantfile`:

```ruby
node.vm.provision "shell", inline: <<-SHELL
  useradd -m vagrantuser || true
  echo "vagrantuser:vagrantpass" | chpasswd
  mkdir -p /home/vagrantuser/.ssh
  cp /vagrant/.ssh/id_ed25519.pub /home/vagrantuser/.ssh/authorized_keys
  chown -R vagrantuser:vagrantuser /home/vagrantuser/.ssh
  chmod 700 /home/vagrantuser/.ssh
  chmod 600 /home/vagrantuser/.ssh/authorized_keys
  echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/wheel
  usermod -aG wheel vagrantuser
SHELL
```

Ensure the public key exists in the shared folder (like `/vagrant/.ssh/id_ed25519.pub`).

---

## ❌ Error: No such file or directory during provisioning

If you encounter:

```
cp: cannot stat '/vagrant/.ssh/id_ed25519.pub': No such file or directory
chmod: cannot access '/home/vagrantuser/.ssh/authorized_keys': No such file or directory
```

### ✅ Resolution:

Make sure to copy your SSH public key to the project path:

```bash
mkdir -p .vagrant/.ssh
cp ~/.ssh/id_ed25519.pub .vagrant/.ssh/
```

Then reference that path in the provision script or adjust it accordingly:

```ruby
cp /vagrant/.vagrant/.ssh/id_ed25519.pub /home/vagrantuser/.ssh/authorized_keys
```

Let me know if you'd like to automatically distribute your SSH keys to all VMs using Ansible or shell provisioning.

---

## 🛑 Additional Error: `chmod` or `cp` Fails in Provisioner

If you receive errors such as:

```
cp: cannot stat '/vagrant/.ssh/id_ed25519.pub': No such file or directory
chmod: cannot access '/home/vagrantuser/.ssh/authorized_keys': No such file or directory
```

### ✅ Additional Fix:

Make sure:

* `.ssh/id_ed25519.pub` exists under your project folder and is synced correctly to `/vagrant` in the guest VM.
* Use an absolute path or create fallback logic in provisioning:

```ruby
if [ -f /vagrant/.ssh/id_ed25519.pub ]; then
  cp /vagrant/.ssh/id_ed25519.pub /home/vagrantuser/.ssh/authorized_keys
else
  echo "SSH public key not found. Skipping..."
fi
```

Let me know if you'd like this fallback logic automated for every VM setup.

---

## 📂 Common Errors Observed

### Error: `cp` or `chmod` failed during inline provisioning

```
cp: cannot stat 'vagrant/.vagrant/.ssh/id_ed25519.pub': No such file or directory
cp: cannot create regular file '/home/vagrantuser/.ssh/authorized_keys': No such file or directory
```

These errors mean either:

* Your local file doesn’t exist.
* The remote user’s `.ssh/` folder was never created before the `cp` command.

✅ Always use `mkdir -p` before copying and test your file presence with `ls -l`.

Let me know if you’d like a pre-check shell snippet added for this as well.
