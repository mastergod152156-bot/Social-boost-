# save as telegram_bot.py
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sys
import os
import threading
import time

# Add the booster script to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Your bot token - REPLACE THIS!
BOT_TOKEN = "8356691147:AAEsky59j7C2M8nOtsbGiIHfXygdQ_553zs"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user data
user_sessions = {}

# Global application instance
application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
👋 Welcome {user.first_name} to TikTok Booster Bot!

⚡ **Features Available:**
• Boost TikTok Views
• Boost TikTok Likes
• Dual Boost (Views + Likes)

📋 **How to use:**
1. Send /boost to start
2. Choose boost type
3. Enter TikTok URL
4. Set boost count
5. Let the bot work!

⚠️ **Note:** Use responsibly!
"""
    
    keyboard = [
        [InlineKeyboardButton("🚀 Start Boosting", callback_data='start_boost')],
        [InlineKeyboardButton("📊 Check Status", callback_data='status')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def boost_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /boost command."""
    keyboard = [
        [InlineKeyboardButton("👁 Views", callback_data='boost_views')],
        [InlineKeyboardButton("❤ Likes", callback_data='boost_likes')],
        [InlineKeyboardButton("⚡ Dual", callback_data='boost_dual')],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Select Boost Type:**\n\n"
        "• 👁 Views - Increase video views\n"
        "• ❤ Likes - Increase video likes\n"
        "• ⚡ Dual - Boost both views & likes",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'start_boost':
        keyboard = [
            [InlineKeyboardButton("👁 Views", callback_data='boost_views')],
            [InlineKeyboardButton("❤ Likes", callback_data='boost_likes')],
            [InlineKeyboardButton("⚡ Dual", callback_data='boost_dual')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎯 **Select Boost Type:**",
            reply_markup=reply_markup
        )
    
    elif query.data in ['boost_views', 'boost_likes', 'boost_dual']:
        user_sessions[user_id] = {'boost_type': query.data}
        
        if query.data == 'boost_views':
            boost_type = "Views"
        elif query.data == 'boost_likes':
            boost_type = "Likes"
        else:
            boost_type = "Dual (Views + Likes)"
        
        await query.edit_message_text(
            f"✅ **{boost_type} Boost Selected**\n\n"
            "📎 Now send me the TikTok video URL:\n"
            "(Example: https://www.tiktok.com/@user/video/123456789)"
        )
    
    elif query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("🚀 Start Boosting", callback_data='start_boost')],
            [InlineKeyboardButton("📊 Check Status", callback_data='status')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🏠 **Main Menu**\n\n"
            "Select an option below:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'help':
        await query.edit_message_text(
            "❓ **Help Guide**\n\n"
            "📌 **How to use:**\n"
            "1. Select boost type\n"
            "2. Send TikTok URL\n"
            "3. Set boost count (default: 100)\n"
            "4. Bot will start processing\n\n"
            "⏱ **Processing Time:**\n"
            "• 100 boosts ≈ 15-30 minutes\n"
            "• Progress updates every 10 boosts\n\n"
            "⚠️ **Important:**\n"
            "• Don't send multiple URLs at once\n"
            "• Use valid TikTok URLs\n"
            "• Be patient during processing"
        )
    
    elif query.data == 'status':
        await query.edit_message_text(
            "📊 **Bot Status**\n\n"
            "✅ **Online & Running**\n"
            "⚡ **Ready to boost**\n\n"
            "👥 Active users: Checking...\n"
            "🔄 Last update: Just now"
        )
    
    elif query.data.startswith('count_'):
        await handle_count_callback(query, user_id)

async def handle_count_callback(query, user_id):
    """Handle count selection callback."""
    if query.data == 'count_custom':
        await query.edit_message_text(
            "✏️ **Enter Custom Count:**\n\n"
            "Send a number between 1-9999\n"
            "(Example: 350)"
        )
        user_sessions[user_id]['awaiting_count'] = True
        return
    
    # Get count from button
    count_map = {
        'count_100': 100,
        'count_250': 250,
        'count_500': 500
    }
    
    count = count_map.get(query.data, 100)
    await start_boosting(query, user_id, count)

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle TikTok URL input."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Check if user is awaiting custom count
    if user_id in user_sessions and user_sessions[user_id].get('awaiting_count'):
        await handle_custom_count_input(update, user_id, text)
        return
    
    # Handle URL input
    if user_id not in user_sessions:
        await update.message.reply_text(
            "⚠️ Please select a boost type first!\n"
            "Use /boost command."
        )
        return
    
    if 'tiktok.com' not in text:
        await update.message.reply_text(
            "❌ Invalid TikTok URL!\n"
            "Please send a valid TikTok video URL."
        )
        return
    
    # Store URL
    user_sessions[user_id]['url'] = text
    
    keyboard = [
        [InlineKeyboardButton("100 (Default)", callback_data='count_100')],
        [InlineKeyboardButton("250", callback_data='count_250')],
        [InlineKeyboardButton("500", callback_data='count_500')],
        [InlineKeyboardButton("Custom", callback_data='count_custom')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ **URL Received:**\n`{text[:50]}...`\n\n"
        "🔢 **Select Boost Count:**\n"
        "(Higher counts take longer)",
        reply_markup=reply_markup
    )

async def handle_custom_count_input(update: Update, user_id: int, text: str):
    """Handle custom count input."""
    try:
        count = int(text.strip())
        if not (1 <= count <= 9999):
            raise ValueError
        
        del user_sessions[user_id]['awaiting_count']
        await start_boosting_message(update.message, user_id, count)
        
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid number!\n"
            "Please enter a number between 1-9999."
        )

async def start_boosting_message(message, user_id, count):
    """Start boosting from message handler."""
    session = user_sessions.get(user_id, {})
    
    if not session.get('url'):
        await message.reply_text("❌ Error: URL not found!")
        return
    
    boost_type = session.get('boost_type', 'boost_views')
    url = session['url']
    
    await message.reply_text(
        f"🚀 **Starting Boost Campaign**\n\n"
        f"📌 Type: {boost_type.replace('boost_', '').title()}\n"
        f"🔢 Count: {count}\n"
        f"📎 URL: {url[:40]}...\n\n"
        f"⏳ **Processing...**\n"
        f"This may take several minutes.\n"
        f"I'll notify you when complete!"
    )
    
    # Run booster in background
    threading.Thread(target=run_booster_sync, args=(user_id, boost_type, url, count, message.chat_id)).start()

async def start_boosting(query, user_id, count):
    """Start boosting from callback query."""
    session = user_sessions.get(user_id, {})
    
    if not session.get('url'):
        await query.edit_message_text("❌ Error: URL not found!")
        return
    
    boost_type = session.get('boost_type', 'boost_views')
    url = session['url']
    
    await query.edit_message_text(
        f"🚀 **Starting Boost Campaign**\n\n"
        f"📌 Type: {boost_type.replace('boost_', '').title()}\n"
        f"🔢 Count: {count}\n"
        f"📎 URL: {url[:40]}...\n\n"
        f"⏳ **Processing...**\n"
        f"This may take several minutes.\n"
        f"I'll notify you when complete!"
    )
    
    # Run booster in background
    threading.Thread(target=run_booster_sync, args=(user_id, boost_type, url, count, query.message.chat_id)).start()

def run_booster_sync(user_id, boost_type, url, count, chat_id):
    """Run booster synchronously in a thread."""
    try:
        # Import and run booster
        from boost1 import TikTokUnlimitedBooster
        booster = TikTokUnlimitedBooster()
        
        # Run the appropriate booster function
        if boost_type == 'boost_views':
            result = booster.unlimited_boost_views(url, count)
        elif boost_type == 'boost_likes':
            result = booster.unlimited_boost_likes(url, count)
        elif boost_type == 'boost_dual':
            result = booster.dual_boost_views_likes(url, count)
        else:
            result = False
        
        # Send completion message via async
        asyncio.run(send_completion_message(chat_id, boost_type, count, url, result))
        
        # Clean up session
        if user_id in user_sessions:
            del user_sessions[user_id]
            
    except Exception as e:
        asyncio.run(send_error_message(chat_id, str(e)))

async def send_completion_message(chat_id, boost_type, count, url, success):
    """Send completion message."""
    if success:
        message = (
            f"✅ **Boost Campaign Complete!**\n\n"
            f"📊 Type: {boost_type.replace('boost_', '').title()}\n"
            f"🎯 Target: {count}\n"
            f"📎 URL: {url[:30]}...\n\n"
            f"✨ Process finished successfully!\n"
            f"Use /boost to start another."
        )
    else:
        message = (
            f"⚠️ **Boost Campaign Finished with Issues**\n\n"
            f"📊 Type: {boost_type.replace('boost_', '').title()}\n"
            f"🎯 Target: {count}\n"
            f"📎 URL: {url[:30]}...\n\n"
            f"❌ Some boosts may have failed.\n"
            f"Use /boost to try again."
        )
    
    await application.bot.send_message(chat_id=chat_id, text=message)

async def send_error_message(chat_id, error_msg):
    """Send error message."""
    message = f"❌ **Error during boosting:**\n`{error_msg[:200]}`"
    await application.bot.send_message(chat_id=chat_id, text=message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        "📚 **TikTok Booster Bot Help**\n\n"
        "**Commands:**\n"
        "/start - Start the bot\n"
        "/boost - Start boosting\n"
        "/help - Show this help\n\n"
        "**How to use:**\n"
        "1. Use /boost command\n"
        "2. Choose boost type\n"
        "3. Send TikTok URL\n"
        "4. Select boost count\n"
        "5. Wait for completion\n\n"
        "**Note:**\n"
        "• One URL at a time\n"
        "• Processing takes time\n"
        "• Use responsibly!"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    await update.message.reply_text(
        "📊 **Bot Status:**\n\n"
        "✅ Online\n"
        "⚡ Ready\n"
        f"👥 Active sessions: {len(user_sessions)}\n"
        "🔄 Last check: Now\n\n"
        "Everything is working fine!"
    )

async def print_bot_info(app):
    """Print bot info after initialization."""
    bot_info = await app.bot.get_me()
    print(f"📱 Bot username: @{bot_info.username}")
    print(f"🆔 Bot ID: {bot_info.id}")
    print(f"👤 Bot name: {bot_info.first_name}")
    print("✅ Ready to receive commands!")
    print("📡 Polling for updates...")

def main():
    """Start the bot."""
    global application
    
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("boost", boost_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Add callback handlers
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Start the bot
    print("🤖 TikTok Booster Bot is starting...")
    
    # Run the bot with event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Create a task to print bot info
    loop.create_task(print_bot_info(application))
    
    # Run polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
    )

if __name__ == '__main__':
    # Suppress the warning
    import warnings
    warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")