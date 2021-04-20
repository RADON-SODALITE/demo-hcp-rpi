# radonpi
RADON based Serverless deployment on Raspberry Pi Edge Cluster

## Pre-requisites
In the master RPi node follow the below steps.

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
- Enable passwordless ssh
```
ssh-keygen -b 2048 -t rsa -f /tmp/sshkey -q -N ""
ssh-copy-id pi@localhost
```
- Clone this repo
```
git clone https://github.com/shreshthtuli/radonpi.git
cd radonpi
```


## Deploy RPi Cluster
- In each node:
```
# Disable swap and enable cgroup:
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove
sudo systemctl disable dphys-swapfile.service

sudo sed -i -e 's/$/ cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory/' /boot/cmdline.txt
sudo reboot now
```
- In master node deploy Kubernetes based OpenFAAS setup using ansible.
```
ansible-playbook playbooks/rpi_deploy.yml
```