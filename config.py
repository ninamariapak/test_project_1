import os
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

BOT_TOKEN = os.getenv(
    'BOT_TOKEN',
    config.get('bot', 'token', fallback=None)
)
if not BOT_TOKEN:
    exit('Please provide BOT_TOKEN env variable')


def get_admin_ids():
    admin_ids = config.get("admin", "admin_ids", fallback=" ")
    admin_ids=[admin_id.strip() for admin_id in admin_ids.split(",")]
    admin_ids=[int(admin_id) for admin_id in admin_ids if admin_ids]
    return admin_ids
