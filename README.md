# radonpi
RADON based Serverless deployment on Raspberry Pi Edge Cluster. This repository demonstrates the use of the RADON framework to deploy a image thumbnail generation service leveraging MinIO (for data storage), k3s (light-weight kubernetes clustering for distributed processing) and OpenFaaS (for serverless function calls).

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

## Roles

There are 3 playbooks separated into folders. Their usage is explained in the table below:

| Role | Purpose
|:-------------|:-------------|
| **function-deploy** | deploys docker image to OpenFaaS as a function
| **bucket-create** | creates necessary buckets on MinIO server
| **bucket-notification** | creates notification on bucket and configures MinIO server configuration

## Deploying with xOpera

This part describes how to deploy function to OpenFaaS and how to setup simple MinIO object storage along with bucket
notification.

### Building docker images and preparing tar files

Docker images are used for deployment of OpenFaaS functions. Currently one can build one docker image which is a source for
function that gets deployed to OpenFaaS later on. It carries the main functionality of this repository and that is image-resize option 
that creates thumbnails from the source image. Source image must be uploaded into (minIO bucket) and then three thumbnails will be created and saved to another bucket.

To prepare tar file with docker image you should run Ansible playbook with:

```bash
cd docker-image-templates
ansible-playbook build.yml 
```

The playbook uses variables from `inputs.yml` so modify this file according to your system settings.

#### Editing the function

You can change the functionality on the function by editing `handler.py` located in `thumbnail-deploy-xopera\docker-image-templates\python-function-template\handler.py`.
This prepared function also uses MinIO class located in file `thumbnail-deploy-xopera\docker-image-templates\python-function-template\minio_handler.py`.
There is also an example of JSON message sent to function by MinIO notification trigger in `docker-image-templates/examples/minio_notification_message_example.rst` file.

### Setting variables

Deployment with xOpera uses inputs that are specified in key-value form in `inputs.yml` file. You can modify these values
according to yourself to set the appropriate params(IPs, bucket names etc.). The following values can be modified:

| Variable | Purpose | Example
|:-------------|:-------------|:-------------|
| `master_node_ip` | IP address of your RPi master node| 192.168.132.233 |
| `bucket_in_name` | The name of incoming the bucket | original |
| `bucket_out_name` | The name of the bucket with results | resized |
| `resize_image_name` | Name of already existing image for image-resize (Image name picked when saving the image has to be the same as actual name of image being saved) | localhost:5000/python-docker-test |
| `resize_function_name` | Name of the new OpenFaaS function with image-resize functionality | var-function-name |
| `minio_user` | Username of the minIO service (set in `playbooks/rpi_deploy.yml`) | admin |
| `minio_password` | Password of the minIO service (set in `playbooks/rpi_deploy.yml`) | password |

Note that we are using docker local registry to load OpenFaaS functions in the k3s environment hence the `localhost:5000` as a prefix of the `resize_image_name`.

### Running with xOpera

When running Ansible playbooks with xOpera you should specify the username that will be used to connect to
the virtual machine by ssh. This can be done by setting the environment variable `OPERA_SSH_USER`.

#### Deploy
You can initiate deployment by running:

`OPERA_SSH_USER=root opera deploy -i inputs.yml rpi_opera.yml`

You can also skip `OPERA_SSH_USER` when running xOpera by exporting this variable using: `export OPERA_SSH_USER=root`.

#### Undeploy
If you wish to undeploy your solution you can run:

`OPERA_SSH_USER=root opera undeploy`