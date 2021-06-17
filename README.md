# check-ram-and-notify
Python script that check available ram and notify if it goes below a defined amount (Useful for low memory computers)

## Requirements
- Python
- Re (Python module)
- PyGObject (Python module)

## Usage
### As normal process
- Execute in a terminal:
```
python check_mem.py
```

### As detached process
- Execute in a terminal:
```
nohup python check_mem.py > /dev/null &
```

### As service
- Choose a place to put the script and write down the full path
- Execute in a terminal: 
```
systemctl --user edit check-ram-and-notify.service --full --force
```
- Write this by replacing \<path\> by the path you wrote down earlier and save:
```
[Unit]
Description=Check ram and notify
[Service]
ExecStart=bash <path>

[Install]
WantedBy=default.target
```
- Enable the service so it starts each time you start your computer
```
systemct --user enable check-ram-and-notify.service
```
