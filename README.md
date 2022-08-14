# writeup-app 

## information
Writeup-app is a simple program for sending notifications of new bug bounty write-ups in Discord.

# Docker installation
Edit config.toml file and put your discord webhook in it.
```commandline
docker-compose up
```

# Manual installation
Edit config.toml file and put your discord webhook in it.
```commandline
pip install -r requirements.txt
alembic revision --autogenerate -m "Create log model"
alembic upgrade head
python main.py
```

# License
```
This project is licensed under MIT License.
```

# Author
[@NotAvailable](https://instagram/n0t.4vailable)
