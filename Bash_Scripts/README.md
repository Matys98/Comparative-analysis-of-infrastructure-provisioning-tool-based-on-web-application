# Bash scripts

## How to run
```shell
touch test.sh
chmod u+x test.sh
./test.sh
```
## Aplications
list of apps posible to deploy

### Static web app - My CV
Benchmark for Master degree project - Comparative analysis of infrastructure provisioning tool based on web application.

scp ./staticwebapp.sh  vagrant@192.168.56.22:/home/vagrant/staticwebapp.sh
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 'chmod u+x staticwebapp.sh | ./staticwebapp.sh'

[My CV App](https://github.com/Matys98/my-cv)

### Tiquet
Tiquet is an open source project management tool focused on the kanban methodology.

[Tiquet App](https://github.com/FLiotta/Tiquet)

### Grafana - solar system
You can monitor the energy flow of the solar pv system.

[Solar System Dashboard](https://grafana.com/grafana/dashboards/13295)

[Grafana](https://grafana.com/) 
