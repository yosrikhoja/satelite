# Satellite Visibility Solver

Automated Python solver for the Hack The Box **First Contact** challenge.

The program connects to the HTB challenge server, receives satellite TLE data and a ground-station location, calculates the satellite visibility windows using Skyfield, sends the answer back, and repeats until the final flag is received.

## How it works

```text
HTB Server
    ↓
Receive TLE + station coordinates
    ↓
Parse challenge data
    ↓
Calculate satellite orbit with Skyfield
    ↓
Find visibility windows above 30°
    ↓
Send answer to HTB
    ↓
Repeat until flag is received
```

The solver searches for satellite passes during a 24-hour period.

A visibility window starts when the satellite rises above the configured minimum elevation and ends when it falls below it.

Default configuration:

```text
Minimum elevation: 30°
Search window: 24 hours
```

## Project Structure

```text
first_contact/
├── client.py      # TCP communication
├── parser.py      # TLE and coordinate parsing
├── orbital.py     # Satellite visibility calculations
├── models.py      # Challenge data model
└── __init__.py

main.py            # Application entry point
requirements.txt   # Python dependencies
README.md
```

## Main Components

`client.py`

Handles the TCP connection with the HTB server.

`parser.py`

Extracts:

* Satellite name
* TLE line 1
* TLE line 2
* Latitude
* Longitude

`orbital.py`

Uses Skyfield to:

* Create the satellite orbit
* Create the ground station
* Search for passes above 30°
* Extract rise and set timestamps

`main.py`

Controls the complete workflow:

```text
Connect → Receive → Parse → Calculate → Send → Repeat
```

The program also detects the final flag using:

```text
HTB{...}
```

## Requirements

Python 3.10+ is recommended.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Current external dependency:

```text
skyfield
```

## Usage

Clone the repository:

```bash
git clone https://github.com/yosrikhoja/satelite.git
cd satelite
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the solver using the host and port provided by Hack The Box:

```bash
python main.py HOST PORT
```

Example:

```bash
python main.py 94.237.x.x 12345
```

The solver will automatically process each challenge until the flag is returned.

## Technologies

* Python
* TCP sockets
* Regular expressions
* Skyfield
* TLE orbital data
* Satellite visibility calculations

## Disclaimer

This project was created for educational purposes and for solving the authorized Hack The Box **First Contact** challenge.
