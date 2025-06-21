# 📦 Install Oracle VirtualBox on Debian 12

This guide provides step-by-step instructions for installing Oracle VirtualBox on **Debian 12 (Bookworm)**.

---

## ✅ Prerequisites

* A user with `sudo` privileges
* Internet access
* Debian 12 up-to-date

Run:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🔧 Step 1: Install Required Dependencies

```bash
sudo apt install -y wget curl gnupg2 lsb-release software-properties-common
```

---

## 🔑 Step 2: Add Oracle VirtualBox GPG Key

```bash
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/oracle_vbox_2016.gpg
```

---

## 📦 Step 3: Add VirtualBox Repository

```bash
echo "deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
```

Update the repository:

```bash
sudo apt update
```

---

## 🖥️ Step 4: Install VirtualBox (Latest Version)

To install the latest version (e.g., 7.0):

```bash
sudo apt install -y virtualbox-7.0
```

> 🔍 You can verify available versions using:
>
> ```bash
> apt-cache search virtualbox
> ```

---

## 🧪 Step 5: Verify Installation

```bash
vboxmanage --version
```

Or launch VirtualBox GUI:

```bash
virtualbox
```

---

## 🛠️ Optional: Install Extension Pack

Download from: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

Then install:

```bash
sudo vboxmanage extpack install Oracle_VM_VirtualBox_Extension_Pack-7.x.x.vbox-extpack
```

---

## 🧼 Optional: Remove VirtualBox

```bash
sudo apt remove --purge virtualbox-7.0
sudo rm /etc/apt/sources.list.d/virtualbox.list
sudo apt update
```

---

## 📚 References

* [Official VirtualBox Downloads](https://www.virtualbox.org/wiki/Linux_Downloads)
* [Debian Wiki VirtualBox](https://wiki.debian.org/VirtualBox)

---

## ✅ Done

You have now successfully installed Oracle VirtualBox on Debian 12!

---

# 📁 Create a DebianLinuxLab Collection on GitHub

To manage and organize multiple Debian Linux Labs as a GitHub collection, follow this recommended structure:

## 🏗️ Architecture Overview

```
debian-linux-lab/
├── README.md
├── lab-template/
│   ├── project1/
│   ├── project2/
│   └── ...
├── networking-lab/
│   ├── project1/
│   └── ...
├── automation-lab/
│   ├── project-ansible/
│   └── project-vagrant/
└── security-lab/
    ├── hardening/
    └── firewall/
```

Each folder is either:

* A **topic lab** (e.g., networking, automation, security)
* A **project** with its own documentation and code

## 🔧 Step-by-Step Setup

1. **Create a new GitHub repository**:

   * Name it `debian-linux-lab`
   * Initialize with a `README.md`

2. **Create subdirectories for labs**:

```bash
mkdir -p debian-linux-lab/{lab-template,networking-lab,automation-lab,security-lab}
```

3. **Add individual projects** under each lab topic:

```bash
mkdir -p debian-linux-lab/automation-lab/{project-ansible,project-vagrant}
```

4. **Add README.md to each project**:

Each project should have:

```markdown
# 🧪 Project Title

## 📌 Objective

## 🛠️ Tools Used

## 🚀 Setup Instructions

## ✅ Output Verification
```

5. **Use Git submodules** if each lab project is in a separate Git repo:

```bash
git submodule add https://github.com/your-org/project-ansible automation-lab/project-ansible
```

6. **Push to GitHub**:

```bash
cd debian-linux-lab
git init
git add .
git commit -m "Initial Debian Linux Lab Structure"
git remote add origin https://github.com/your-user/debian-linux-lab.git
git push -u origin main
```

## 📘 Tips

* Use GitHub Pages + MkDocs to create interactive documentation.
* Use GitHub Actions for CI (e.g., test lab setup scripts).
* Label each lab clearly: `[Beginner]`, `[Intermediate]`, `[Advanced]`
* Add `.gitlab-ci.yml` or `ansible-lint` configs as needed.

## 🧾 JSON Project Structure

### `debian_linux_lab_structure.json`

```json
{
  "debian-linux-lab": {
    "README.md": "",
    "lab-template": {
      "project1": {"README.md": ""},
      "project2": {"README.md": ""}
    },
    "networking-lab": {
      "project1": {"README.md": ""}
    },
    "automation-lab": {
      "project-ansible": {"README.md": ""},
      "project-vagrant": {"README.md": ""}
    },
    "security-lab": {
      "hardening": {"README.md": ""},
      "firewall": {"README.md": ""}
    }
  }
}
```

---

## 🐍 Python Script to Generate Structure

### `create_lab_structure.py`

```python
import os
import json

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    with open("debian_linux_lab_structure.json") as f:
        lab_structure = json.load(f)

    create_structure(".", lab_structure)
    print("✅ Debian Linux Lab structure created.")
```

---

## 🧱 Linux Permissions Tip: `chmod 777` for Project Directories

To ensure that Visual Studio Code (or any editor) can create directories and files within your project structure, you can use:

```bash
chmod -R 777 ./debian-linux-lab
```

### Explanation:

* `-R`: Applies the change recursively to all subdirectories and files
* `777`: Grants **read**, **write**, and **execute** permissions to **owner**, **group**, and **others**

### 🔐 Warning:

This setting is insecure for production environments. It’s fine for local development, but consider more secure permission models for shared systems.

For better practice:

```bash
sudo chown -R $USER:$USER ./debian-linux-lab
chmod -R 755 ./debian-linux-lab
```

---

## ✅ Done

You now have a clean, modular DebianLinuxLab structure to scale across projects and teams, and tools to generate it automatically.
