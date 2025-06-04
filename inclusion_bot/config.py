import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID', '0'))

# Simple role mapping (user_id: role)
ROLE_MAP = {
    ADMIN_ID: 'coordinator'
}
