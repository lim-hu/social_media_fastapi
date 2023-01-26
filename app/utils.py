from passlib.context import CryptContext
from email.message import EmailMessage
import ssl, smtplib
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(pwd):
    pwd_hashed = pwd_context.hash(pwd)
    return pwd_hashed

def verify_pwd(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def send_token(email, token):

    email_sender = settings.from_email
    email_password = settings.email_pass
    email_reciver = email

    subject = "Token for Reset Password"
    body = f'''
<html>
    <body>
    
            <h2>User this token for create new password:</h1>
            <h3>{token}</h3>
            

          
    </body>
</html>
    '''


    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["subject"] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        
        smtp.sendmail(email_sender, email_reciver, em.as_string())