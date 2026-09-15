# DEVAS Web

A web interface to the [Superman](https://github.com/all-umass/superman) tools.



## Quick start


### 1: Install dependencies

While it’s theoretically possible to install dependencies using `pip install -r requirements.txt`, we had problems with this on an Ubuntu 24.04 server with Python 3.12.

You will need root privileges to install an older version of Python and some support libraries. We also elected to install a few modules this way so they could automatically be kept up to date.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9-full python3.9-dev
sudo apt install cython3 libfreetype-dev libomp-dev pkg-config
sudo apt install python3-dask python3-yaml python3-setuptools
sudo chown www-data:www-data /opt
```

The remainder of the instructions below should be executed as the `www-data` user:

```bash
python3.9 -m venv --system-site-packages /opt/devas-venv
source /opt/devas-venv/bin/activate
pip install h5py pandas PyWavelets scikit-learn
```

Clone the [Superman repo](https://github.com/all-umass/superman) into `/opt/superman`.

```bash
cd /opt/superman
pip install .
```

Clone this repo into `/opt/devas-web` and it should be ready to configure and run after picking up the last few dependencies.

```bash
cd /opt/devas-web
pip install -r requirements.txt
```


### 2: Configure

An example config file is provided at `config-template.yml`.
Copy this to `config.yml` and edit as needed.
Any values left commented-out or not included will use reasonable defaults.

In the same way, copy `datasets-template.yml` to `datasets.yml`
and update the listings to match your local datasets.


### 3: Add datasets

Datasets are the basic unit of data in the superman server.
Add one by modifying the `datasets.yml` configuration file,
optionally adding a loader function to the `custom_datasets.py` module.
Relative paths are evaluated starting from the current working directory
of the process running `superman_server.py`,
typically the root of this repository.



## Running the service


### Using `systemctl`

We have provided a Systemd service definition for automatically starting and stopping the service. It can be symlinked to make using it easy:

```bash
sudo ln -s /opt/devas-web/devas.service /etc/systemd/system/
sudo systemctl daemon-reload
```

It provides the usual `start`/`stop`/`restart` functionality; don’t forget to
```bash
sudo systemctl enable devas.service
```
to have start on server reboot.


### Manual control

To start (or restart) the server in the background for typical use, run:
```bash
./restart_server.sh
```

Use the option `--dry-run` to check what would happen without interfering
with any currently running server.

Or simply run the server directly, and handle the details yourself:
```bash
python superman_server.py
```

To stop the server without restarting it, use:
```bash
./restart_server.sh --kill
```


## Running behind a secure proxy

The application does not currently support SSL, but it can run behind a proxy server to provide a secure layer.

Set `secure_proxy: True` in `config.yml` and configure the proxy to pass all `https://` and `wss://` requests through to the application using `http://` and `ws://` on whatever port it uses (default `54321` if not also set in `config.yml`).


### Apache 2.4

Be sure `mod_headers`, `mod_proxy`, `mod_proxy_http`, and `mod_rewrite` are enabled. If your Apache is _older_ than 2.4.47, also enable `mod_proxy_wstunnel`.

This configuration tests for whether the `Upgrade` header is present and contains the word `websocket`, then changes the schema appropriately before passing the request to the application running on the same server.

```ApacheConf
  RequestHeader set X-Forwarded-Proto "https"
  RequestHeader set X-Forwarded-Port  "443"

  RewriteEngine On
  RewriteCond %{HTTP:Upgrade} !=websocket [NC]
  RewriteRule ^/?(.*)$ http://localhost:54321/$1 [P,L]
  RewriteCond %{HTTP:Upgrade} =websocket [NC]
  RewriteRule ^/?(.*)$ ws://localhost:54321/$1 [P,L]

  ProxyPreserveHost On
  ProxyPassReverse / http://localhost:54321/
  ProxyPassReverse / ws://localhost:54321/
```



## Other notes

Original documentation claimed that we could set up to run tests:

```bash
pip install pytest mock coverage
```

If you want to verify that everything is working as intended, try running the test suite (located in the `test/` directory):

```bash
python -m pytest
```

To generate a nice code coverage report:

```bash
coverage run --source backend -m pytest
coverage html
```
