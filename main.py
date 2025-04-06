import requests
import schedule
import time
from supabase import create_client, Client
import telebot
from keep_alive import keep_alive

# اتصال به Supabase
url = "https://djioxuobvlbqajzlcdmr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
supabase: Client = create_client(url, key)

# ربات تلگرام
bot = telebot.TeleBot("توکن ربات", parse_mode="HTML")
chat_id = 6892568530

# فعال کردن سرور Flask
keep_alive()

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

# زمان‌بندی
schedule.every(10).minutes.do(save_price)

# اجرای اولیه
print("🚀 اجرای اولیه...")
save_price()

# حلقه همیشگی
print("⏳ منتظر اجرای خودکار هر ۱۰ دقیقه...")
while True:
    schedule.run_pending()
    time.sleep(1)
