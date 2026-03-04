import smtplib
import datetime
import time

MY_EMAIL = ""
MY_PASSWORD = ""
RECEIVER_EMAIL = ""

TARGET_HOUR = 19
TARGET_MINUTE = 51

print("Code started")

while True:
    now = datetime.datetime.now()

    if now.hour == TARGET_HOUR and now.minute == TARGET_MINUTE:
        print("Test email")
        try:
            with open("email.txt", "r", encoding="utf-8") as file:
                email_body = file.read()

            subject = "Subject: Test email from bot\n\n"
            full_message = subject + email_body

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=RECEIVER_EMAIL,
                    msg=full_message.encode('utf-8')
                )

            print("Email sent successfully!")

            time.sleep(60)

        except FileNotFoundError:
            print("Error: 'message.txt' file not found.")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)

    else:
        time.sleep(30)