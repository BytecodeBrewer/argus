from argus.gui.app import app
from argus.storage.database import initialize_database


def main(db) -> None:
    """
    The main function that starts the application.
    """
    initialize_database(db)
    app()


db = ""
main(db)
