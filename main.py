
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes
)
from BET_FLEX_V2 import hash_round, predict_match_result, calculate_potential_goals

import logging

logging.basicConfig(level=logging.INFO)

TEAM1, TEAM2, GOALS1, GOALS2, ROUND, TEAM1_RESULTS, TEAM1_GOALS, TEAM2_RESULTS, TEAM2_GOALS = range(9)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بك في بوت 🔍 BetFlexAI 🔍.

أدخل الأحرف الثلاثة للفريق 1:")
    return TEAM1

async def get_team1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team1'] = update.message.text.upper()
    await update.message.reply_text("أدخل الأحرف الثلاثة للفريق 2:")
    return TEAM2

async def get_team2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team2'] = update.message.text.upper()
    await update.message.reply_text("أدخل عدد أهداف الفريق 1:")
    return GOALS1

async def get_goals1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['goals1'] = int(update.message.text)
    await update.message.reply_text("أدخل عدد أهداف الفريق 2:")
    return GOALS2

async def get_goals2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['goals2'] = int(update.message.text)
    await update.message.reply_text("أدخل رقم الجولة (من 1 إلى 31):")
    return ROUND

async def get_round(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['round'] = int(update.message.text)
    await update.message.reply_text("أدخل نتائج آخر 3 مباريات للفريق 1 (مثال: فوز,خسارة,تعادل):")
    return TEAM1_RESULTS

async def get_team1_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team1_results'] = [r.strip() for r in update.message.text.split(',')]
    await update.message.reply_text("أدخل عدد الأهداف في آخر 3 مباريات للفريق 1 (مثال: 2,0,1):")
    return TEAM1_GOALS

async def get_team1_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team1_goals_list'] = list(map(int, update.message.text.split(',')))
    await update.message.reply_text("أدخل نتائج آخر 3 مباريات للفريق 2:")
    return TEAM2_RESULTS

async def get_team2_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team2_results'] = [r.strip() for r in update.message.text.split(',')]
    await update.message.reply_text("أدخل عدد الأهداف في آخر 3 مباريات للفريق 2:")
    return TEAM2_GOALS

async def get_team2_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['team2_goals_list'] = list(map(int, update.message.text.split(',')))
    hr = hash_round(user_data['team1'], user_data['team2'], user_data['round'])
    result_text = predict_match_result(user_data['goals1'], user_data['goals2'])
    avg_goals = calculate_potential_goals(user_data['team1_goals_list'], user_data['team2_goals_list'])
    response = (
        f"🔢 رقم الجولة: {user_data['round']}
"
        f"📝 نتيجة المباراة: {result_text}
"
        f"⚽ متوسط الأهداف المتوقعة: {avg_goals:.2f}
"
        f"🔁 رمز التوقع: {hr}
"
    )
    await update.message.reply_text(response)
    return ConversationHandler.END

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        TEAM1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team1)],
        TEAM2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team2)],
        GOALS1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goals1)],
        GOALS2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goals2)],
        ROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_round)],
        TEAM1_RESULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team1_results)],
        TEAM1_GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team1_goals)],
        TEAM2_RESULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team2_results)],
        TEAM2_GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_team2_goals)],
    },
    fallbacks=[]
)
app.add_handler(conv_handler)
app.run_polling()
