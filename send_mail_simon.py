
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
def sendMail(compte_envoi, password_envoi, to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list
    fro = "PiTech Raspberry Pi"
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)
    smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(compte_envoi, password_envoi)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()
