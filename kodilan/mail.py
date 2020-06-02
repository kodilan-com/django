from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def do_mail(email, title, theme, variables):
    msg_plain = render_to_string('mail/{}.txt'.format(theme), variables)
    msg_html = render_to_string('mail/{}.html'.format(theme), variables)
    try:
        send_mail(
            'Kodilan - ' + title,
            msg_plain,
            getattr(settings, "SENDER_MAIL", ""),
            [email],
            fail_silently=False,
            html_message=msg_html
        )
    except ConnectionRefusedError as e:
        print('There was an error sending an email: ', e)
    pass


# todo: create post will update
def send_activation(email, first_name, last_name, token):
    do_mail(email, "İlan Onay", "activation",
            {'first_name': first_name, 'last_name': last_name, 'code': token})
