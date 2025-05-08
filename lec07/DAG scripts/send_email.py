import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_notification_email():
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_MAIL_FROM")
    smtp_to = smtp_from  

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Iris ML DAG завершився успішно"
    msg["From"] = smtp_from
    msg["To"] = smtp_to

    html_content = """
    <html>
      <body>
        <h3>DAG process_iris завершився успішно!</h3>
        <p>Модель була навчена, результат збережено.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if os.getenv("SMTP_STARTTLS", "True").lower() == "true":
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from, smtp_to, msg.as_string())
            print("[INFO] Email успішно надіслано.")
    except Exception as e:
        print(f"[ERROR] Помилка надсилання email: {e}")
        raise
