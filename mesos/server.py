import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../../opteryx"))

from mysql_mimic import MysqlServer  # isort: skip
from mysql_mimic import Session  # isort: skip
from orso import logging  # isort: skip
import opteryx  # isort: skip


logging.set_log_name("MESOS")
logger = logging.get_logger()
logger.setLevel(5)


class MySession(Session):
    async def query(self, sql, attrs):
        print(f"Original SQL string: {sql}")
        print(f"Query attributes: {attrs}")
        print(f"Currently authenticated user: {self.username}")
        print(f"Currently selected database: {self.database}")

        curr = opteryx.query(sql)
        return curr.fetchall(), curr.column_names


if __name__ == "__main__":
    server = MysqlServer(session_factory=MySession, port=3306)
    asyncio.run(server.serve_forever())
