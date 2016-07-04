
import smtplib
from email.mime.text import MIMEText

def send_mail(from_addr, to_addr_list, subject, content):
    msg = MIMEText(content, _subtype="plain", _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ';'.join(to_addr_list)

    
    srv = smtplib.SMTP()
    srv.set_debuglevel(1)
    srv.connect("192.168.1.205")
    srv.login("matt", "matt")
    srv.sendmail(from_addr, to_addr_list, msg.as_string())
    srv.quit()
    
if __name__ == '__main__':
    send_mail("yy_meng@people2000.net", ["mengyy_linux@163.com"], "Test", "Test Email and Noreply.")