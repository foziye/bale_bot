from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)


# ==========================
# تنظیمات ربات بله
# ==========================

TOKEN = os.getenv("BOT_TOKEN")

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

USERS_FILE = "users.json"

ADMIN_ID = 890553531


# ==========================
# لینک کانال
# ==========================

CHANNEL_LINK = "https://ble.ir/biochem_akademy"


# ==========================
# مدیریت کاربران
# ==========================

def load_users():

    if not os.path.exists(USERS_FILE):
        return {}

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {}



def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=2
        )


# ==========================
# ارسال پیام
# ==========================

def send_message(chat_id, text, keyboard=None):

    data = {

        "chat_id": chat_id,

        "text": text

    }


    if keyboard:

        data["reply_markup"] = keyboard


    try:

        requests.post(
            BASE_URL + "/sendMessage",
            json=data
        )


    except Exception as e:

        print(e)



# ==========================
# گزارش ادمین
# ==========================

def send_admin_report(text):

    send_message(
        ADMIN_ID,
        text
    )
# ==========================
# کیبوردها
# ==========================

def phone_keyboard():

    return {

        "keyboard": [

            [
                {
                    "text": "📱 ارسال شماره موبایل",
                    "request_contact": True
                }
            ]

        ],

        "resize_keyboard": True,

        "one_time_keyboard": True

    }



def grade_keyboard():

    return {

        "keyboard": [

            [
                {
                    "text": "🧬 دهم"
                }
            ],

            [
                {
                    "text": "🧬 یازدهم"
                }
            ],

            [
                {
                    "text": "🧬 دوازدهم"
                }
            ]

        ],

        "resize_keyboard": True

    }



def remove_keyboard():

    return {

        "remove_keyboard": True

    }



# ==========================
# صفحه تست ربات
# ==========================

@app.route("/", methods=["GET"])
def home():

    return "Bale Bot Running"



# ==========================
# دریافت پیام‌های بله
# ==========================

@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json(force=True)


    if "message" not in update:

        return "ok"


    message = update["message"]


    chat_id = message["chat"]["id"]


    user_id = str(message["from"]["id"])


    text = message.get(
        "text",
        ""
    )


    users = load_users()



    # ==========================
    # ساخت کاربر جدید
    # ==========================

    if user_id not in users:

        users[user_id] = {

            "phone": "",

            "name": "",

            "grade": "",

            "step": "phone"

        }



    # ==========================
    # شروع ربات
    # ==========================

    if text == "/start":


        users[user_id]["step"] = "phone"


        save_users(users)


        send_message(

            chat_id,

            "🌱 سلام.\n\n"
            "به آکادمی زیست و شیمی کنکور خوش آمدید.\n\n"
            "برای دریافت هدیه رایگان ابتدا شماره موبایل خود را ارسال کنید.",

            phone_keyboard()

        )


        return "ok"

    # ==========================
    # دریافت شماره موبایل
    # ==========================

    if "contact" in message:


        phone = message["contact"]["phone_number"]


        users[user_id]["phone"] = phone


        users[user_id]["step"] = "name"


        save_users(users)



        send_admin_report(

            "📱 ثبت شماره جدید\n\n"
            f"ID: {user_id}\n"
            f"شماره: {phone}"

        )



        send_message(

            chat_id,

            "✅ شماره شما ثبت شد.\n\n"
            "لطفاً نام و نام خانوادگی خود را ارسال کنید.",

            remove_keyboard()

        )


        return "ok"





    # ==========================
    # دریافت نام
    # ==========================

    if users[user_id]["step"] == "name":


        users[user_id]["name"] = text


        users[user_id]["step"] = "grade"


        save_users(users)



        send_admin_report(

            "👤 ثبت نام کاربر\n\n"
            f"نام: {text}\n"
            f"شماره: {users[user_id]['phone']}"

        )



        send_message(

            chat_id,

            f"🌸 {text} عزیز\n\n"
            "پایه تحصیلی خود را انتخاب کنید:",

            grade_keyboard()

        )


        return "ok"





    # ==========================
    # انتخاب پایه و ارسال لینک آپارات
    # ==========================

    if users[user_id]["step"] == "grade":


        if text == "🧬 دهم":


            users[user_id]["grade"] = "دهم"


            message_text = (

                "🎬 هدیه رایگان زیست و شیمی دهم:\n\n"

                "🧪 شیمی:\n"
                "آموزش خفن آرایش الکترونی برای شیمی:\n"
                "https://www.aparat.com/v/jhebxd3\n\n"

                "🧬 زیست:\n"
                "آموزش خفن و مفهومی دستگاه لنفی:\n"
                "https://www.aparat.com/v/phu28x8"

            )



        elif text == "🧬 یازدهم":


            users[user_id]["grade"] = "یازدهم"


            message_text = (

                "🎬 هدیه رایگان زیست و شیمی یازدهم:\n\n"

                "🧪 شیمی:\n"
                "قانون هس در ۱۰ دقیقه:\n"
                "https://www.aparat.com/v/ejadt63\n\n"

                "🧬 زیست:\n"
                "آموزش خفن ساختار و نحوه انقباض ماهیچه‌ها:\n"
                "https://www.aparat.com/v/rhqt74j"

            )
        elif text == "🧬 دوازدهم":


            users[user_id]["grade"] = "دوازدهم"


            message_text = (

                "🎬 هدیه رایگان زیست و شیمی دوازدهم:\n\n"

                "🧪 شیمی:\n"
                "تدریس خفن جدول پتانسیل استاندارد برای شیمی:\n"
                "https://www.aparat.com/v/gar626c\n\n"

                "🧬 زیست:\n"
                "آموزش خفن سرنوشت پروتئین:\n"
                "https://www.aparat.com/v/jatf9qt"

            )


        else:


            send_message(

                chat_id,

                "لطفاً یکی از گزینه‌های پایه را انتخاب کنید."

            )


            return "ok"




        users[user_id]["step"] = "done"


        save_users(users)



        send_message(

            chat_id,

            message_text

        )



        send_message(

            chat_id,

            "🌱 برای دریافت هدیه‌های بیشتر و آموزش‌های رایگان وارد کانال آکادمی شوید:\n\n"
            + CHANNEL_LINK

        )



        return "ok"





    # ==========================
    # کاربران تکمیل شده
    # ==========================

    if users[user_id]["step"] == "done":


        send_message(

            chat_id,

            "✅ اطلاعات شما قبلاً ثبت شده است.\n\n"
            "برای دریافت آموزش‌های بیشتر وارد کانال شوید:\n\n"
            + CHANNEL_LINK

        )


        return "ok"



    return "ok"





# ==========================
# اجرای برنامه
# ==========================

if __name__ == "__main__":


    port = int(

        os.environ.get(

            "PORT",

            5000

        )

    )


    app.run(

        host="0.0.0.0",

        port=port

    )