# Install

Installation from pypi:

```bash
pip install pydantify
```

*pydantify* needs Python 3.10 or above. 

## Installing from git

```bash
pip install git+https://github.com/pydantify/pydantify.git
```

*pydantify* can also be installed in editable mode.

```bash
git clone https://github.com/pydantify/pydantify.git
pip install -e pydantify
```

## Create docker image

```bash
git clone https://github.com/pydantify/pydantify.git
cd pydantify
docker build -t pydantify .
docker run --rm -it pydantify
```