# radonpi-todo

- none

# Problems fixed

- Traditional libseccomp library (for kernel syscall filtering) works for amd64 architecture. The deployment ansible playbook circumvents this by updating the syscall configurations.
- Traditional kubectl deployments can access docker images locally, however for the light-weight k3s deployment we had to setup and integrate local docker registry (and kubectl secret keys) for image sharing across all Rpi nodes.
- Traditional minio deployments on kubernetes require huge amounts of ram and lead to several errors when setting up bucket notifications, but for a standalone deployment the extended tosca definitions allow easy setup. 
- 