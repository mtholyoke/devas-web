# superman-web

A web interface to the [Superman](https://github.com/all-umass/superman) tools.

## Quick start - current server

Starting from a fresh download of the source files,
a few steps are required before starting the server for the first time.

### 1: Install dependencies

While it’s theoretically possible to install dependencies using `pip install -r requirements.txt`, we had problems with this on an Ubuntu 24.04 server with Python 3.12 and found this sequence, executed as the `www-data` user, to work well.

Clone this repo into `/opt/devas-web` as the `www-data` user

Clone the [Superman repo](https://github.com/all-umass/superman) into `/opt/superman`

```bash
sudo apt install -y cython3 libomp-dev python3-dev python3-h5py python3-matplotlib python3-pandas python3-pywt python3-yaml python3-sklearn python3-setuptools python3-tornado python3-venv

python3 -m venv --system-site-packages /opt/devas-venv

source /opt/devas-venv/bin/activate

cd /opt/superman

pip install .
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


### 4: Run

To start (or restart) the server in the background for typical use, run:

    ./restart_server.sh

Use the option `--dry-run` to check what would happen without interfering
with any currently running server.

Or simply run the server directly, and handle the details yourself:

    python superman_server.py

To stop the server without restarting it, use:

    ./restart_server.sh --kill



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
