from threading import Thread
from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from django.conf import settings


class SendEmail(Thread):
    def __init__(self, subject='', body='', to=None, context={}):
        Thread.__init__(self)
        self.__subject = subject
        self.__body = body
        
        if type(to) == str:
            self.__to = [to]
        else:
            self.__to = to

    def run(self):
        try:
            email = EmailMessage(
                    self.__subject,
                    self.__body,
                    settings.DEFAULT_FROM_EMAIL,
                    to = self.__to
                        )   
            email.content_subtype = "html"
            email.fail_silently=True           
            email.send()  

        except Exception as e:
            print(f'Exception while sending email: {e}')

        return


def _sendNormalEmail(to=None, context={}, template=None, purpose=""):
    subject = f'{purpose}'
    body = render_to_string(template, context)
    if to:
        email = SendEmail(subject=subject, body=body, to=to, context=context)
        email.start()
    return