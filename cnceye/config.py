import os

# For github actions
CI_MYSQL_CONFIG = dict(
    host="localhost",
    port=3306,
    user="root",
    password="root",
)


MYSQL_CONFIG = dict(
    host="raspberrypi.local",
    port=3306,
    user="yuchi",
    password="raspberrypi",
)

if os.environ.get("CI"):
    MYSQL_CONFIG = CI_MYSQL_CONFIG