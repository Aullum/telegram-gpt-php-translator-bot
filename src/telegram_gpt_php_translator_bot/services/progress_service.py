from aiogram import Bot
from aiogram.types import Message
from typing import Optional


class ProgressUI:
    """Single-message progress UI that updates in-place."""

    def __init__(self, bot: Bot, chat_id: int):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id: Optional[int] = None
        self._last_text: str = ""

    @staticmethod
    def _bar(percent: int, width: int = 24) -> str:
        filled = max(0, min(width, (percent * width) // 100))
        return "█" * filled + "░" * (width - filled)

    async def start(self, stage: str = "Starting", percent: int = 0):
        text = self._render(stage, percent)
        msg: Message = await self.bot.send_message(self.chat_id, text)
        self.message_id = msg.message_id
        self._last_text = text

    async def update(self, stage: str, percent: int):
        """Edit only if content actually changed to avoid 'message is not modified'."""
        text = self._render(stage, percent)
        if text == self._last_text:
            return
        if self.message_id is None:
            await self.start(stage, percent)
            return
        try:
            await self.bot.edit_message_text(
                chat_id=self.chat_id, message_id=self.message_id, text=text
            )
            self._last_text = text
        except Exception as e:
            _ = e

    async def fail(self, reason: str):
        text = (
            "Translation progress\n"
            f"Stage: ❌ Failed: {reason}\n"
            f"{self._bar(0)} 0%"
        )
        if self.message_id is None:
            msg: Message = await self.bot.send_message(self.chat_id, text)
            self.message_id = msg.message_id
            self._last_text = text
            return
        try:
            await self.bot.edit_message_text(
                chat_id=self.chat_id, message_id=self.message_id, text=text
            )
            self._last_text = text
        except Exception:
            pass

    async def done(self):
        await self.update("✅ Completed", 100)

    def _render(self, stage: str, percent: int) -> str:
        percent = max(0, min(100, percent))
        return (
            "Translation progress\n"
            f"Stage: {stage}\n"
            f"{self._bar(percent)} {percent}%"
        )
