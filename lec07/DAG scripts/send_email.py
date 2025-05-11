import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_notification_email(**context):
    """
    Надсилає email з точністю моделі та топ-5 фіч за важливістю.
    """
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_MAIL_FROM")
    smtp_to = smtp_from

    # Отримання XCom-змінних
    ti = context['ti']
    accuracy = ti.xcom_pull(task_ids='train_model', key='accuracy')
    top_features = ti.xcom_pull(task_ids='train_model', key='top_features')

    # HTML контент з фічами
    feature_lines = "".join(
        f"<li><b>{feat}</b>: {imp:.4f}</li>" for feat, imp in top_features.items()
    )

    html_content = f"""
    <html>
      <body>
        <h3> DAG <code>process_iris</code> завершився успішно</h3>
        <p><b>Accuracy моделі:</b> {accuracy:.4f}</p>
        <p><b>Топ 5 найважливіших фіч:</b></p>
        <ul>
            {feature_lines}
        </ul>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Iris ML DAG завершився успішно"
    msg["From"] = smtp_from
    msg["To"] = smtp_to
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if os.getenv("SMTP_STARTTLS", "True").lower() == "true":
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from, smtp_to, msg.as_string())
            print("[INFO] Email успішно надіслано.")
    except Exception as e:
        print(f"[ERROR] Email помилка: {e}")
        raise
