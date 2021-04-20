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
- Update *inventory/hosts.inv* file with the LAN addresses of master and worker nodes. Example below:
```
[k3s_rpi:children]
k3s_rpi_master
k3s_rpi_worker

[k3s_rpi_master]
k3s-rpi1 ansible_host=192.168.0.58

[k3s_rpi_worker]
k3s-rpi2 ansible_host=192.168.50.201
k3s-rpi3 ansible_host=192.168.50.202
k3s-rpi4 ansible_host=192.168.50.203
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