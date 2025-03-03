import smtplib

def send_email(to, subject, body):
    sender = "your_email@example.com"
    password = "your_password"
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, message)