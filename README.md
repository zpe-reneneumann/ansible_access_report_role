# Project Title
The project provides a Ansible role which allows users to export Device Details from a Nodegrid appliance based on the Access view

## Features
The role uses Nodegrids RESTFul APIs to export the data and then writes the data to a cvs file.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
ansible
or 
Nodegrid OS version 6.0

### Installing
- Copy the role zip folder to the ansible host or Nodegrid host
- unzip the zip file
- copy the folder as is to the ansible playbook folder
- in the ansible playbook folder create a new playbook with the following content

Example for Nodegrid OS:
- File was copied via File Manager /var/local/file_manager/admin_group
- as ansible user
```
mv /var/local/file_manager/admin_group/roles.zip /etc/ansible/playbooks
cd /etc/ansible/playbooks
unzip roles.zip
rm roles.zip
```


```access_device_export.yml
- hosts: all
  gather_facts: false
  connection: local
  roles:
   - nodegrid_access_data_export
```
## Usage
The role requires the following variable:
- ansible_host
- username
- password
- path (default: /var/local/file_manager/admin_group)

execute from as ansible user from the commandline
```shell
cd /etc/ansible/playbooks
ansible-playbook access_device_export.yml -e 'username=admin password=admin'
```

Example
```shell
ansible@iegsr01:/etc/ansible/playbooks$ ansible-playbook access_device_export.yml -e 'username=admin password=admin' --limit localhost
PLAY [all] *************************************************************************************************************************************************************************************************************************************

TASK [nodegrid_access_data_export : Get Access Details] ****************************************************************************************************************************************************************************************
skipping: [localhost]

TASK [nodegrid_access_data_export : Get Access Details] ****************************************************************************************************************************************************************************************
changed: [localhost]

PLAY RECAP *************************************************************************************************************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

## Authors
Rene Neumann (zpe-rneumann)
