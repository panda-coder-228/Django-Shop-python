import logging
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from utils.emoij import EMOJI


class EmojiFormatter(logging.Formatter):
    def format(self, record):
        if not getattr(record, "emoji", None):
            record.emoji = EMOJI.get(record.levelname, "🔥")

        return super().format(record)


class SimpleTelegramHandler(logging.Handler):
    MAX_MESSAGE = 4000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise ValueError("Telegram env vars not set")

        self.session = requests.Session()

        retry_strategy = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 501, 502, 504, 429]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def emit(self, record):
        try:
            message = self.format(record)

            status = getattr(record, "status_code", None)
            if status:
                message = f"\nStatus: {status}\nLogger: {record.levelname}\n{message}"

            if len(message) > self.MAX_MESSAGE:
                message = message[:3997] + "..."

            response = self.session.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                data={"chat_id": self.chat_id, "text": message},
                timeout=5,
            )
            print(response.status_code)
            print(response.text)

            response.raise_for_status()

        except Exception:
            self.handleError(record)

    def close(self):
        if hasattr(self, "session"):
            self.session.close()
        super().close()
