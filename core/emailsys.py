import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(to_email, subject, body_text, body_html=None):
    from_email = "uncovered.comrade@gmail.com"
    password = "tdkm eayf mdpe ougg" # APP PASSWORD
    
    # t3st1nG4PP
    # #t3st1nG4PP u.c
    msg = MIMEMultipart("alternative")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(body_text, "plain")
    msg.attach(part1)
    
    if body_html:
        part2 = MIMEText(body_html, "html")
        msg.attach(part2)
        
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.send_message(msg)

def send_excel_report(recipient, subject, body, excel_generator, filename=None):
    from_email = "uncovered.comrade@gmail.com"
    password = "tdkm eayf mdpe ougg"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = recipient
    msg.set_content(body)

    msg.add_attachment(excel_generator.read(), maintype='application', subtype='vnd.opnxmlformats-officedocument.spreadsheetml.sheet', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465)as smtp:
      smtp.login(from_email,password)
      smtp.send_message(msg)

      
def generate_email_template(user_name, book_title, message, color="#1f6aa5"):
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px;">
          <h2 style="color: {color};">OrgaNicer Notification</h2>
          <p>Hello <strong>{user_name}</strong>,</p>
          <p>{message}</p>
          <p style="font-size: 18px;">📘<em>{book_title}</em></p>
          <hr>
          <p style="font-size: 12px; color: #999;">This is an automated message from the Library System.</p>
        </div>
      </body>
    </html>
    """