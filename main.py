import requests
import schedule
import time
from supabase import create_client, Client
import telebot
from keep_alive import keep_alive  # برای روشن موندن Replit

# اتصال به Supabase
url = "https://djioxuobvlbqajzlcdmr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqaW94dW9idmxicWFqemxjZG1yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4ODU0NDUsImV4cCI6MjA1OTQ2MTQ0NX0.5WTffVeX8FqrypHuBv0_-GNthwSqDtvK3koscTOqglc"
supabase: Client = create_client(url, key)

# اطلاعات ربات تلگرام
telegram_token = "8107734105:AAE-W8DAkBTA1AIYmW2nhW6SakcILnsy0LQ"
chat_id = 6892568530

bot = telebot.TeleBot(telegram_token, parse_mode="HTML")

# فعال کردن سرور Flask
keep_alive()

# دریافت قیمت از نوسان
def get_gold_price():
    try:
        response = requests.get(
            "http://api.navasan.tech/latest/?api_key=freexgsQRlDiWxI665SrMqQaTwrclMsN",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        data = response.json()
        price = int(data["harat_naghdi_sell"]["value"].replace(",", ""))
        return price
    except Exception as e:
        print("❌ خطا در دریافت قیمت:", e)
        return None

# ذخیره در دیتابیس و ارسال به تلگرام
def save_price():
    print("⏳ دریافت قیمت...")
    price = get_gold_price()
    if price:
        print(f"📦 قیمت: {price} تومان")
        try:
            supabase.table("gold_prices").insert({"price": price}).execute()
            print("✅ ذخیره شد.")
            bot.send_message(chat_id, f"📢 قیمت جدید:\n<code>{price:,}</code> تومان")
            print("📩 پیام ارسال شد.")
        except Exception as e:
            print("❌ خطا در ذخیره یا ارسال:", e)
    else:
        print("⚠️ قیمت دریافت نشد.")

# ⏱ زمان‌بندی: هر ۱۰ دقیقه
schedule.every(10).minutes.do(save_price)

# اجرای تست اولیه
print("🚀 تست اولیه...")
save_price()

print("⏳ منتظر اجرای خودکار هر ۱۰ دقیقه...")
while True:
    schedule.run_pending()
    time.sleep(1)
