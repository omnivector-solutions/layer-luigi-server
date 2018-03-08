# luigi-server

This charm provides luigi-server as described in the luigi docs [here](http://luigi.readthedocs.io/en/stable/central_scheduler.html#the-luigid-server).


## Usage
Use Juju to deploy this charm.
```bash
juju deploy luigi-server
```

## Access
Following deployment you must expose luigi-server before you can access its web front end.
```bash
juju expose luigi-server
```
Luigi server web and api available at `http://<luigi-server-ip-address>:8082`


## Extended Usage
You may optionally 'relate' this charm to a reverse proxy using the 'http' interface.
The workflow would resemble the following.
```bash
juju deploy luigi-server
juju deploy haproxy

juju relate haproxy:reverseproxy luigi-server:http
juju expose haproxy
```
luigi-server will now be available at `http://<haproxy-ip>`


#### License
* AGPLv3 (see `LICENSE` file)

#### Copyright
* James Beedy (c) 2018 <jamesbeedy@gmail.com>
