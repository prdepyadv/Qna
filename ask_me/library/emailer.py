from decouple import config
from django.core.mail import send_mail

class emailer:
    def emailQuestion(self, message='', mailTo='Pradeep <prdepyadv@gmail.com>', mailFrom='AskMe <no-reply@askme.com>'):
        try:
            mailGunDomainName = config('Mailgun_Domain_Name')
            mailGunApiKey = config('Mailgun_API_Key')
            send_mail('New Question added!!', message, mailFrom, [mailTo])
            return True
        except NameError:
            print(NameError)
            return False
