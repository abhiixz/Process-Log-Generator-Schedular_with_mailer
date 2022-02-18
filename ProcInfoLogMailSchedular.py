import os
from sys import *
import psutil
import time
from urllib.request import urlopen
import smtplib
import schedule
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urlopen('https://www.google.com', timeout = 1)
        return True
    except:
        return False

def MailSender(filename, time):
    try:
        fromaddr = "your_mailid"
        toaddr = "receivers_mailid"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        body = """
            type body here
                sent at : %s"""%(time)

        Subject = """
            Your Process Log generated at : %s
            """ %(time)

        msg['Subject'] = Subject
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "your_password")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

        print("Log file successfully sent through Mail")

    except Exception as E:
        print("Unable to send mail : ", E)

def ProecssLog(log_dir="Logger"):
    listprocess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "-" * 80
    log_path = os.path.join(log_dir, "Log%s.log" % (time.ctime()))
    f = open(log_path, 'w')
    f.write(separator + "\n")
    f.write("Logger Application : " + time.ctime() + "\n")
    f.write(separator + "\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'username', 'name'])
            # vms = proc.memory_info().vms / (1024 * 1024)
            # pinfo['vms'] = vms
            listprocess.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil, ZombieProcess):
            pass

    for element in listprocess:
        f.write("%s\n" % element)

    print("Log is successfully generated at location : ", log_path)

    connected = is_connected()

    if connected:
        startTime = time.time()
        MailSender(log_path, time.ctime())
        endTime = time.time()
        print("Took %s seconds to send mail" %(endTime - startTime))

    else:
        print("There is no internet connecion")
        ProecssLog()

def main():
    print("-----Process Log Info-----")
    print("Application Name : " + argv[0])

    if (len(argv) != 2):
        print("Error: Invalid number of arguments")
        exit()

    if (argv[1] == "-h") or (argv[1] == "-H"):
        print("Help : This Script is used to create log of running processess")
        exit()

    if (argv[1] == "-u") or (argv[1] == "=U"):
        print("Usage : ApplicationName AbsolutePath_of_Directory")
        exit()

    try:
        schedule.every(int(argv[1])).seconds.do(ProecssLog)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid datatye of input")

    except Exception as E:
        print("Error : Invalid Input", E)


if __name__ == "__main__":
    main()