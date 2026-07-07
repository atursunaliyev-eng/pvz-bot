import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ==========================
# BOT TOKEN
# ==========================
TOKEN = "8931236658:AAHmAIyut4hZ9mAHIFHHhjxwP162rg9Pa_Q"

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
    # QR papkalar
    # ==========================
    qr_folders = ["qr1", "qr2", "qr3"]

    for qr_folder in qr_folders:

        if not os.path.isdir(qr_folder):
            continue

        for file in os.listdir(qr_folder):

            if not file.lower().endswith(".png"):
                continue

            file_name = os.path.splitext(file)[0]

            if normalize(file_name) == search_text:

                with open(os.path.join(qr_folder, file), "rb") as photo:

                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"🚚 Mashina: {file_name}"
                    )

                return

    # ==========================
    # PVZ qidirish
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
    # Topilmadi
    # ==========================
    await update.message.reply_text("❌ Ma'lumot topilmadi.")


# ==========================
# MAIN
# ==========================
def main():

    print("Current folder:", os.getcwd())
    print("Files:", os.listdir("."))

    print("QR1 exists:", os.path.isdir("qr1"))
    print("QR2 exists:", os.path.isdir("qr2"))

    if os.path.isdir("qr1"):
        print("QR1 files:", len(os.listdir("qr1")))

    if os.path.isdir("qr2"):
        print("QR2 files:", len(os.listdir("qr2")))

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
