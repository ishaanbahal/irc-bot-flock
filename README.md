# IRC relay bot for Flock

### Requirements:
- Internet! Duh!
- Python (2.7.x)
- Requests package, install using `pip install requests`

### Setup:
1. Copy config-template.json to config.json `cp config-template.json config.json`
2. Fill in details, it already has a structure, to add a channel, copy the same structure, change the key name, and add config for the channel.

> Note: The keys you create in config.json, will be auto joined on server startup and verification. Authentication also takes place from the same config file. Be sure to fill that out.

### Run dat bot
- If you've filled in the data correctly in the config.json, run using `python start_clients.py`

> To avoid python 3 and 2 issue, just do a `chmod 755 start_clients.py` and run using `./start_clients.py`, it will choose the correct python.