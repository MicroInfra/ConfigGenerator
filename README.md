# Config Generator
It's a service to generate configuration files for your microinfra.

## Configure

Easiest way to start using microinfra is to specify services in request to create config.
So let us describe service available fields to configure.


*name* - just a name should use only alphabet numbers and _ ("A-Za-z0-9_")


*url* - url where it could be accessed *FROM proxy-manager CONTAINER*!
So, for example if you are running it on port 8000 on your host machine you should use `http://host.docker.internal:8000/`.
If you don't want service to be available from internet you can run in the same docker network. To do so you should:
1. Enable `use_docker_network` in request.
2. Create docker network in server `docker network create microinfra_net`
3. Add container that you want to send requests to network by `docker network connect microinfra_net *container_id*`
4. In `url` specify container name. For example http://dummy_server:80/
!There could be errors with this method. TBA solution.


*listen_port* - port on server that should listen to requests.
For example if I specify 10000, then by accessing http://server_ip:10000 I will be addressed to `url` from previous point.

## Development
### To configure pre-commit hook:
```bash
pip3 install pre-commit && pre-commit install
```

### Dependencies
```bash
pip3 install poetry && poetry install
```
