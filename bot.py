import os
import pandas as pd
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ---------------- FLASK (Render port uchun) ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ishlayapti"

# ---------------- BOT TOKEN ----------------
TOKEN = os.environ.get("BOT_TOKEN")

# ---------------- DATA ----------------
df = pd.read_excel("pvz.xlsx")
df.columns = ["address", "pvz_name", "latitude", "longitude"]

# ---------------- BOT LOGIC ----------------
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

# ---------------- BOT START ----------------
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_pvz))

    print("Bot ishga tushdi...")
    application.run_polling()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    import threading

    # BOT alohida thread
    threading.Thread(target=run_bot, daemon=True).start()

    # FLASK main thread (Render talab qiladi)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
