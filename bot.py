import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ==========================
# BOT TOKEN
# ==========================
TOKEN = "8931236658:AAHPg0gAOIT8MjaZvBsV-CyUiStB11D4908"

# ==========================
# EXCEL
# ==========================
df = pd.read_excel("pvz.xlsx")
df.columns = ["address", "pvz_name", "latitude", "longitude"]

# ==========================
# TEXTNI TOZALASH
# ==========================
def normalize(text):
    return (
        str(text)
        .upper()
        .replace(" ", "")
        .replace("-", "")
    )

# ==========================
# QIDIRUV
# ==========================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text.strip()
    search_text = normalize(user_text)

    # ==========================
    # 1. QR KOD QIDIRISH
    # ==========================
    qr_folders = ["qr1", "qr2"]

for qr_folder in qr_folders:

    if not os.path.isdir(qr_folder):
        continue

    for file in os.listdir(qr_folder):

        if file.lower().endswith(".png"):

            file_name = os.path.splitext(file)[0]

            if normalize(file_name) == search_text:

                with open(os.path.join(qr_folder, file), "rb") as photo:

                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"🚚 Mashina: {file_name}"
                    )

                return

            if file.lower().endswith(".png"):

                file_name = os.path.splitext(file)[0]

                if normalize(file_name) == search_text:

                    with open(os.path.join(qr_folder, file), "rb") as photo:

                        await update.message.reply_photo(
                            photo=photo,
                            caption=f"🚚 Mashina: {file_name}"
                        )

                    return

    # ==========================
    # 2. PVZ QIDIRISH
    # ==========================
    result = df[df["pvz_name"].astype(str).str.upper() == user_text.upper()]

    if not result.empty:

        row = result.iloc[0]

        await update.message.reply_text(
            f"📍 PVZ: {row['pvz_name']}\n\n"
            f"🏠 Manzil:\n{row['address']}"
        )

        await update.message.reply_location(
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"])
        )

        return

    # ==========================
    # TOPILMADI
    # ==========================
    await update.message.reply_text("❌ Ma'lumot topilmadi.")

print("Current folder:", os.getcwd())
print("Files:", os.listdir("."))
print("QR exists:", os.path.isdir("qr"))

if os.path.isdir("qr"):
    print("QR files:", os.listdir("qr"))


# ==========================
# BOT
# ==========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search
        )
    )

    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    main()
