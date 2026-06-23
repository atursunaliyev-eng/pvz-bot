import pandas as pd
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8931236658:AAGRzJ5CsuAtr0bO0tkolOOlvV1ZJzfGSho"

df = pd.read_excel("pvz.xlsx")
df.columns = ["address", "pvz_name", "latitude", "longitude"]

async def search_pvz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip().upper()

    result = df[df["pvz_name"].astype(str).str.upper() == user_text]

    if result.empty:
        await update.message.reply_text("PVZ topilmadi.")
        return

    row = result.iloc[0]

    await update.message.reply_text(
        f"PVZ: {row['pvz_name']}\n\nManzil:\n{row['address']}"
    )

    await update.message.reply_location(
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"])
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, search_pvz)
)

print("Bot ishga tushdi...")
app.run_polling()