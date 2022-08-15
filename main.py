import logging
from requests.exceptions import MissingSchema
from platforms import (
    PentesterlandScrapper, MediumScrapper
)
from utils import (
    cleanup, ascii_art, notify_script_launch, notify_writeup
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Log, App
)
from rich.logging import RichHandler
from tomli import load

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


class WriteupApp:
    """
    Main class of Writeup App
    """
    first_launch = None

    def __init__(self) -> None:
        """
        Constructor method
        """

        # Read config.toml file
        with open("config.toml", mode="rb") as _config_file:
            self.config = load(_config_file)
            _config_file.close()

        # Session of the sqlite database
        self.Session = sessionmaker(
            bind=create_engine(
                self.config['database']['uri']
            )
        )

        log.info("Sent launch log in discord.")
        notify_script_launch(notify_webhook=self.config["discord"]["script_working_alert_webhook"])

        # Check that the program is running for the first time or not
        with self.Session() as session:
            app_table = session.query(App).all()

            if len(app_table) < 1:
                self.first_launch = True
                session.add(
                    App(
                        id=1,
                        first_launch=False
                    )
                )
                session.commit()

            else:
                self.first_launch = False

    def medium_writeup(self) -> list:
        """
        This method will receive the dictionary of medium write-ups
        :return: medium write-ups
        :rtype: list
        """
        output = []
        # Read tags from config.toml file
        tags = self.config['medium']['tags']

        log.info("Requesting to medium to get new writeups.")

        for tag in tags:
            _instance = MediumScrapper(tag=tag)
            output.append(_instance.get_response())

        return output

    @staticmethod
    def pentesterland_writeup() -> list:
        """
        This method will receive the dictionary of pentesterlab write-ups
        :return: pentesterlab write-ups
        :type: list
        """
        log.info("Requesting to pentesterland to get new writeups.")
        _instance = PentesterlandScrapper()
        return _instance.get_response()

    def insert_log(self, data) -> None:
        """
        This method will insert data to database
        :param data: write-up data
        :return: Nothing
        :type: None
        """
        with self.Session() as session:
            session.add(
                Log(
                    url=data.get("post")["link"],
                    title=data.get("post")["title"],
                    author=data.get("author")["name"],
                    author_url=data.get("author")["username"]
                )
            )
            session.commit()
            session.close()

    def main(self) -> None:
        """
        This is the main method of the class and when it is called, it checks whether a new write-up has been added
        or not, if it has been added, it adds it to the database and announces it in Discord.

        :return: Nothing
        :type: None
        """

        # Get all write-ups from database
        with self.Session() as session:
            database_writeups = session.query(Log).all()
            session.close()

        medium_writeups = self.medium_writeup()
        pentesterland_writeups = self.pentesterland_writeup()

        titles = [output.title for output in database_writeups]
        log.info("Checking medium writeups with the database")

        # Loop into medium write-ups
        for writeups in medium_writeups:
            for writeup in writeups:
                if writeup.get("post")["title"] not in titles:
                    if not self.first_launch:
                        log.info("Sent new writeup in discord.")
                        # Notify the write-up in discord
                        notify_writeup(notify_webhook=self.config["discord"]["writeup_notif_webhook"], data=writeup)
                    self.insert_log(writeup)

        log.info("Checking pentesterland writeups with the database")
        for writeup in pentesterland_writeups:
            if writeup.get("post")["title"] not in titles:
                if not self.first_launch:
                    log.info("Sent new writeup in discord.")
                    # Notify the write-up in discord
                    notify_writeup(notify_webhook=self.config["discord"]["writeup_notif_webhook"], data=writeup)
                self.insert_log(writeup)


if __name__ == "__main__":
    cleanup()
    ascii_art()
    try:
        instance = WriteupApp()
        instance.main()
    except MissingSchema:
        log.error("Add Discord webhooks into config.toml file.")
