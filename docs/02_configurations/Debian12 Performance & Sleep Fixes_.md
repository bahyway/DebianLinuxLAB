# 🛡️ How to Prevent Debian 12 from Freezing or Sleeping Automatically

If your **Debian 12 system freezes or stops responding** after a few minutes of inactivity (such as auto-sleep after 5 minutes), this guide provides a set of **best practices**, configuration fixes, and theming recommendations to improve performance, stability, and desktop experience.

---

## 🔧 Disable Auto Suspend, Sleep & Screen Lock

### GNOME Settings (GUI Way)

1. Open **Settings > Power**

2. Set:

   * **Blank screen**: *Never*
   * **Automatic suspend**: *Off*

3. Go to **Settings > Privacy > Screen Lock**

   * Disable **Screen Lock**

### CLI Way (System-Wide)

Run:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

This disables all suspend actions at the system level.

If using GNOME Power Manager:

```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.desktop.session idle-delay 0
```

---

## 🧱 Prevent Laptop Lid from Causing Suspend

Edit:

```bash
sudo nano /etc/systemd/logind.conf
```

Uncomment and set:

```ini
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
HandleLidSwitchExternalPower=ignore
```

Then restart:

```bash
sudo systemctl restart systemd-logind.service
```

---

## 🧊 Fix Random Freezes on GNOME/Wayland

If you're using **Wayland** and experience freezes:

### Option 1: Switch to X11

1. On login screen, click the gear icon
2. Choose **GNOME on Xorg**

### Option 2: Disable Wayland

Edit:

```bash
sudo nano /etc/gdm3/daemon.conf
```

Uncomment and set:

```ini
WaylandEnable=false
```

Then reboot:

```bash
sudo systemctl restart gdm3
```

---

## 🎨 Recommended Theme & Extensions

### Install GNOME Tweaks

```bash
sudo apt install gnome-tweaks gnome-shell-extensions
```

### Enable Best Theme for Productivity

Install **Yaru** or **WhiteSur** theme:

```bash
sudo apt install yaru-theme-gnome
```

Use **GNOME Tweaks > Appearance** to apply:

* Yaru-Dark (Theme)
* Papirus-Dark (Icons)
* Monospace Font: `JetBrains Mono` or `Fira Code`

Optional: Add extensions from [https://extensions.gnome.org](https://extensions.gnome.org)

---

## 🧠 System Monitor Recommendation

Install `gnome-system-monitor` or `bpytop` to keep track of performance:

```bash
sudo apt install gnome-system-monitor
sudo apt install bpytop
```

---

## ✅ Summary Checklist

*

---

## 🎉 Done!

Your Debian 12 system is now optimized to **stay responsive and avoid freezing**, with **auto-suspend fully disabled** and theming optimized for usability and performance.
