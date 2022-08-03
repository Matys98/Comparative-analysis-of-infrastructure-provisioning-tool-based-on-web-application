# Ansible
Ansible is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[Ansible Documentation](https://docs.ansible.com/)

## Instalation
### Linux pip
```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py --user
$ python -m pip install --user ansible
$ sudo python get-pip.py
$ sudo python -m pip install ansible
```

# Starting project

## How to run
Example how to run

```console
foo@bar:~$ ansible-playbook -i hosts playbook.yml
```

Example how to run with tags

```console
foo@bar:~$ ansible-playbook -i hosts playbook.yml --tags "foo"

# Deploy static web app to all 3 instnance
foo@bar:~$ ansible-playbook -i hosts static.yml --tags "StaticWebAppThreeInstance"
```

## Aplications
list of apps posible to deploy

### Static web app - My CV
Benchmark for Master degree project - Comparative analysis of infrastructure provisioning tool based on web application.

[My CV App](https://github.com/Matys98/my-cv)

### Tiquet
Tiquet is an open source project management tool focused on the kanban methodology.

[Tiquet App](https://github.com/FLiotta/Tiquet)

### Grafana - solar system
You can monitor the energy flow of the solar pv system.

[Solar System Dashboard](https://grafana.com/grafana/dashboards/13295)

[Grafana](https://grafana.com/)