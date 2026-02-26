import os
import logging
import dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from components.rag import pipeline


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = (
        "Привет! 👋\n\n"
        "Я консультант для поступающих в Финансовый Университет.\n\n"
        "Задавайте свои вопросы, и я постараюсь вам помочь!\n\n"
        "Используйте /help для справки."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_message = (
        "Доступные команды:\n\n"
        "/start - Начать диалог\n"
        "/help - Показать справку\n\n"
        "Просто напишите свой вопрос, и я постараюсь вам помочь!"
    )
    await update.message.reply_text(help_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages and process them through RAG pipeline."""
    try:
        user_id = update.effective_user.id
        question = update.message.text
        chat_history_id = f"user_{user_id}"
        
        # Show typing indicator
        await update.message.chat.send_action('typing')
        
        # Run RAG pipeline
        res = pipeline.run(
            data={
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
                "message_retriever": {"chat_history_id": chat_history_id},
                "message_writer": {"chat_history_id": chat_history_id},
            },
            include_outputs_from={"llm"},
        )
        
        # Get response from LLM
        response_text = res["llm"]["replies"][0].text
        
        # Send response back to user
        await update.message.reply_text(response_text)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "Извините, произошла ошибка при обработке вашего вопроса. "
            "Пожалуйста, попробуйте позже."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a Telegram message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    """Start the bot using polling mode."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # log all errors caused by updates and the dispatcher's try statement
    application.add_error_handler(error_handler)
    
    # Start the Bot using polling mode
    logger.info("Starting bot in polling mode...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
