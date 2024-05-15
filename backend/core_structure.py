import asyncio
from collections import UserDict

from comradewolf.utils.olap_data_types import OlapFrontend
from comradewolf.utils.utils import singleton


class OlapDbSettings(UserDict):
    """
    Class with database settings for Olap frontend
    """

    def __init__(self, host: str, port: str, database: str, username: str, password: str, database_type: str,
                 max_connections: int, olap_frontend: OlapFrontend) -> None:
        """

        :param host:
        :param port:
        :param database:
        :param username:
        :param password:
        :param database_type:
        :param max_connections:
        """
        settings = {
            "host": host,
            "port": port,
            "database": database,
            "username": username,
            "password": password,
            "database_type": database_type,
            "max_connections": asyncio.Semaphore(max_connections),
            "olap_frontend": olap_frontend,
        }
        super().__init__(settings)

    async def acquire_semaphore(self):
        return self.data["max_connections"].acquire()

    async def release_semaphore(self):
        return self.data["max_connections"].release()


@singleton
class CoreContainer(UserDict):
    """
    Contains frontend info about OLAP
    """

    def create_olap_structure(self, olap_name: str, olap_settings: OlapDbSettings) -> None:
        self.data = {olap_name: olap_settings}

    def get_front_fields(self, olap_name: str) -> OlapFrontend:
        return self.data[olap_name]["olap_frontend"]
