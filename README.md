# radonpi
RADON based Serverless deployment on Raspberry Pi Edge Cluster

## Pre-requisites
- Install opera
```
sudo apt install python3-pip
pip3 install opera
export PATH=$PATH:~/.local/bin
```
- Install packages
```
sudo apt install -y sshpass
```


## Deploy RPi Cluster
In each node:
```
# Disable swap and enable cgroup:
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove
sudo systemctl disable dphys-swapfile.service

sudo sed -i -e 's/$/ cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory/' /boot/cmdline.txt
sudo reboot now
```