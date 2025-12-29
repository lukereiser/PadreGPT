"""
PadreGPT Telegram Bot — A Telegram interface to your Custom GPT Assistant.

Uses the OpenAI Assistants API to connect to an Assistant with your
uploaded PDFs (e.g., Catholic library documents from Telegram).
"""

import asyncio
import logging
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Your Assistant ID from OpenAI (created with your PDFs as knowledge)
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "").strip()

# Rate limiting (messages per user per hour)
RATE_LIMIT_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "60"))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# State Management
# ---------------------------------------------------------------------------


@dataclass
class UserState:
    """Tracks conversation thread and rate limiting per user."""

    thread_id: Optional[str] = None  # OpenAI thread ID for this user
    request_times: list[datetime] = field(default_factory=list)


# In-memory state (will reset on restart — could extend to Redis/DB if needed)
user_states: dict[int, UserState] = defaultdict(UserState)


def _prune_old_requests(state: UserState) -> None:
    """Remove request timestamps older than 1 hour."""
    cutoff = datetime.now() - timedelta(hours=1)
    state.request_times = [t for t in state.request_times if t > cutoff]


def _is_rate_limited(user_id: int) -> bool:
    """Check if user has exceeded rate limit."""
    state = user_states[user_id]
    _prune_old_requests(state)
    return len(state.request_times) >= RATE_LIMIT_PER_HOUR


def _record_request(user_id: int) -> None:
    """Record a new request for rate limiting."""
    user_states[user_id].request_times.append(datetime.now())


def _clear_thread(user_id: int) -> None:
    """Clear a user's conversation thread (start fresh)."""
    user_states[user_id].thread_id = None


# ---------------------------------------------------------------------------
# OpenAI Assistants API Client
# ---------------------------------------------------------------------------

openai_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    global openai_client
    if openai_client is None:
        openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    return openai_client


async def get_or_create_thread(user_id: int) -> str:
    """Get existing thread for user or create a new one."""
    state = user_states[user_id]
    if state.thread_id:
        return state.thread_id

    client = get_openai_client()
    thread = await client.beta.threads.create()
    state.thread_id = thread.id
    logger.info(f"Created new thread {thread.id} for user {user_id}")
    return thread.id


async def chat_with_assistant(user_id: int, user_message: str) -> str:
    """Send user message to the Assistant and get response."""
    client = get_openai_client()

    # Get or create a thread for this user
    thread_id = await get_or_create_thread(user_id)

    # Add the user's message to the thread
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message,
    )

    # Run the assistant on the thread
    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=OPENAI_ASSISTANT_ID,
    )

    if run.status != "completed":
        logger.error(f"Run failed with status: {run.status}")
        if run.last_error:
            logger.error(f"Error: {run.last_error}")
        raise RuntimeError(f"Assistant run failed: {run.status}")

    # Get the assistant's response (most recent message)
    messages = await client.beta.threads.messages.list(
        thread_id=thread_id,
        order="desc",
        limit=1,
    )

    if not messages.data:
        raise RuntimeError("No response from assistant")

    # Extract text content from the response
    response_message = messages.data[0]
    text_parts = []
    for block in response_message.content:
        if block.type == "text":
            text_parts.append(block.text.value)

    return "\n".join(text_parts) if text_parts else "I couldn't generate a response."


# ---------------------------------------------------------------------------
# Telegram Handlers
# ---------------------------------------------------------------------------


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    welcome = (
        f"👋 Hey {user.first_name}! I'm **PadreGPT**.\n\n"
        "I have access to a library of Catholic documents and resources. "
        "Ask me anything about Catholic teaching, doctrine, prayers, or traditions!\n\n"
        "**Commands:**\n"
        "• /new — Start a fresh conversation\n"
        "• /help — Show this help message\n\n"
        "Go ahead, ask me anything!"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = (
        "🤖 **PadreGPT Help**\n\n"
        "I'm an AI assistant with access to a library of Catholic documents. "
        "Ask me about:\n"
        "• Catholic doctrine and teaching\n"
        "• Prayers and devotions\n"
        "• Church history and traditions\n"
        "• Scripture and theology\n\n"
        "**Commands:**\n"
        "• /new — Clear conversation history and start fresh\n"
        "• /help — Show this help message\n\n"
        f"**Rate limit:** {RATE_LIMIT_PER_HOUR} messages/hour"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /new command — clears conversation history."""
    user_id = update.effective_user.id
    _clear_thread(user_id)
    await update.message.reply_text(
        "🧹 Conversation cleared! Let's start fresh. What would you like to know?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.effective_user.id
    user_message = update.message.text

    # Rate limiting check
    if _is_rate_limited(user_id):
        await update.message.reply_text(
            f"⏳ You've hit the rate limit ({RATE_LIMIT_PER_HOUR} messages/hour). "
            "Please wait a bit before sending more messages."
        )
        return

    # Record this request
    _record_request(user_id)

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        response = await chat_with_assistant(user_id, user_message)

        # Telegram has a 4096 char limit per message
        if len(response) > 4000:
            # Split into chunks
            chunks = [response[i : i + 4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error handling message from user {user_id}: {e}")
        await update.message.reply_text(
            "❌ Oops! Something went wrong. Please try again in a moment."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "Missing TELEGRAM_BOT_TOKEN. "
            "Create a bot with @BotFather and add the token to your .env file."
        )

    if not OPENAI_API_KEY:
        raise SystemExit(
            "Missing OPENAI_API_KEY. "
            "Get an API key from https://platform.openai.com/api-keys"
        )

    if not OPENAI_ASSISTANT_ID:
        raise SystemExit(
            "Missing OPENAI_ASSISTANT_ID. "
            "Create an Assistant at https://platform.openai.com/assistants "
            "and add the ID to your .env file."
        )

    logger.info(f"Starting PadreGPT bot with Assistant: {OPENAI_ASSISTANT_ID}")

    # Build application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("new", new_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error_handler)

    # Start polling
    logger.info("Bot is running! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
