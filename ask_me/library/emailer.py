from decouple import config
from django.core.mail import send_mail

class emailer:
    def emailQuestion(self, subject, message='', mailTo='Pradeep <prdepyadv@gmail.com>', mailFrom='AskMe <no-reply@askme.com>'):
        try:
            mailGunDomainName = config('Mailgun_Domain_Name')
            mailGunApiKey = config('Mailgun_API_Key')
            send_mail(subject, message, mailFrom, [mailTo])
            return True
        except NameError:
            print(NameError)
            return False
