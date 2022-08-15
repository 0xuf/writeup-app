# writeup-app

## information
Writeup-app is a simple program for sending notifications of new bug bounty write-ups in Discord.

### built with
* [![Python][Python]][Python-Url]
* [![SqlAlchemy][SqlAlchemy]][SqlAlchemy-Url]
* [![Alembic][Alembic]][Alembic]
* [![Toml][Toml]][Toml-Url]


# installation
Edit config.toml file and put your discord webhooks in it.
```commandline
pip install -r requirements.txt
alembic revision --autogenerate -m "Create Writeup models"
alembic upgrade head
python main.py
```

## You can set the script to run once every time by adding crontab
## example for run every 1 hour
```commandline
crontab -e
0 * * * * /usr/bin/python3 /path/to/main.py
```

## You can also

# License
```
This project is licensed under MIT License.
```

# Author
Discord: NotAvailable#7600

[Instagram](https://instagram.com/n0t.4vailable)

[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=blue
[Python-Url]: https://python.org
[Toml]: https://img.shields.io/badge/toml-35495E?style=for-the-badge
[Toml-Url]: https://toml.io
[SqlAlchemy]: https://img.shields.io/badge/SqlALchemy-0769AD?style=for-the-badge
[SqlAlchemy-Url]: https://www.sqlalchemy.org/
[Alembic]: https://img.shields.io/badge/alembic-20232A?style=for-the-badge
[Alembic-Url]: https://pypi.org/project/alembic/