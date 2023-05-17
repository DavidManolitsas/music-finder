# Music Finder

A python application that finds the latest search releases from a range of search artists

https://davidmanolitsas.github.io/music-finder/

## Setup Project

Start virtual environment (venv) with:

```bash
python3 -m virtualenv venv
```

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip3 install -U -r requirements.txt
```

## Quick Start

Run the project with:

```bash
make run
```

or

```bash
python3 -m music --days 31
```

To run the project with custom artists, update the `music/resources/artists.yaml` file


## Clean Up

Deactivate `venv` with:

```bash
deactivate
```
