# superman-web

A web interface to the [Superman](https://github.com/all-umass/superman) tools.

## Quick Start - current server

Starting from a fresh download of the source files,
a few steps are required before starting the server for the first time.

### 1: Install Dependencies

Python (2.7 or 3.4+) is the main requirement for running the server.
Several Python packages are needed, available from PyPI via `pip`:

    pip install --only-binary :all: superman matplotlib tornado pyyaml h5py pandas

If you're not running Linux, `superman` may require special care to install.
See [the superman docs](https://github.com/all-umass/superman#installation) for instructions.

For running tests, you'll want:

    pip install pytest mock coverage

### 2: Configure

An example config file is provided at `config-template.yml`.
Copy this to `config.yml` and edit as needed.
Any values left commented-out or not included will use reasonable defaults.

In the same way, copy `datasets-template.yml` to `datasets.yml`
and update the listings to match your local datasets.


### 3: Add Datasets

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

If you want to verify that everything is working as intended,
try running the test suite (located in the `test/` directory):

    python -m pytest

To generate a nice code coverage report:

    coverage run --source backend -m pytest
    coverage html



## Quick Start - Ubuntu 20.04 test server


### 1. Install dependencies

1. Python 3.8+ and `pip` installed via `apt`
1. `apt install --yes libomp-dev python3-dev cython3` 
1. `apt install --yes python3-h5py python3-matplotlib python3-yaml python3-tornado` 
1. `pip install PyWavelets==1.1.1`
1. `pip install pandas==1.1.5`
1. Clone this repo. `/opt/devas-web` is a good choice.
1. Install the [Superman](https://github.com/all-umass/superman) library:
   1. clone its repo into `/opt/superman` because v0.1.2 might not be packaged right for `pip`
   1. `cd /opt/superman`
   1. `pip install -e .`


### 2. Configure

1. Make a copy of `config-template.yml` named `config.yml`. For dev/test work, the defaults are all sufficient.
1. Add at least one dataset to the `data/` directory, and create a file `datasets.yml` that has appropriate entries for the datasets.


### 3. Run

**TODO:** This should probably be set up as a service but for now there’s a script on the test server, `start-dev-server.sh`. Run that. 



## Developing in Lando

You will need a reasonably current version of [Lando](https://lando.dev/) (this was developed in version 3.6.4) and whichever version of Docker it prefers.


### Preparation

1. Make a copy of `config-template.yml` named `config.yml`. For dev work, the defaults are all sufficient (if you change the port, also change it in `.lando.yml`).
1. Add a dataset to the `data/` directory, and create a file `datasets.yml` that has an entry for it.

**TODO:** Include a sample dataset?


### First run

The first time you run `lando start` it will download a Python container, install the relevant packages, and start the DEVAS service at http://devas.lndo.site. Subsequent `start`s will go much faster.

**TODO:** Update versions of dependencies to be consistent with what’s available via `apt` for the dev container (Debian 11) and next production server (Ubuntu 20.04 or Ubuntu 22.04):
| package    | current | Debian 11    | Ubuntu 20           | Ubuntu 22      |
|------------|---------|--------------|---------------------|----------------|
| h5py       | 2.10.0  | 2.10.0-9     | 2.10.0-2build2      | 3.6.0-2build1  |
| matplotlib | 3.1.3   | 3.3.4-1      | 3.1.2-1ubuntu4      | 3.5.1-2build1  |
| pandas     | 1.0.0   | 1.1.5+dfsg-2 | n/a – use `pip`     | 1.3.5+dfsg-3   |
| pywavelets | 1.1.1   | 1.1.1-1+b2   | n/a – use `pip`     | 1.1.1-1ubuntu2 |
| pyyaml     | 5.3     | 5.3.1-5      | 5.3.1-1             | 5.4.1-1ubuntu1 |
| tornado    | 4.4.2   | 6.1.0-1+b1   | 6.0.3+really5.1.1-3 | 6.1.0-3build1  |


### Working in the dev environment

Once the container is running, `lando python` will execute Python inside the container. 

