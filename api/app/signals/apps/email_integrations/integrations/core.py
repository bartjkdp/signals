"""
E-mail integration for 'core' Signal behaviour.
"""
import re

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from signals.apps.email_integrations.messages import ALL_AFHANDELING_TEXT
from signals.apps.signals import workflow


def get_valid_email(signal):
    """Get e-mail address from given `Signal` object.

    :param signal: Signal object
    :returns: e-mail address (str)
    """
    email_valid = r'[^@]+@[^@]+\.[^@]+'
    if signal.reporter and signal.reporter.email and re.match(email_valid, signal.reporter.email):
        return signal.reporter.email
    return None


def send_mail_reporter_created(signal):
    """Send a notification e-mail to the reporter about initial create of the given `Signal` object.

    :param signal: Signal object
    :returns: number of successfully send messages or None
    """
    email = get_valid_email(signal)
    if not email:
        return None

    subject = f'Bedankt voor uw melding ({signal.id})'
    message = create_initial_create_notification_message(signal)
    to = signal.reporter.email

    return send_mail(subject, message, settings.NOREPLY, (to, ))


def create_initial_create_notification_message(signal):
    """Create e-mail body message about initial create of the given `Signal` object.

    :param signal: Signal object
    :returns: message (str)
    """
    context = {
        'signal': signal,
        'afhandelings_text': (
            ALL_AFHANDELING_TEXT[signal.category_assignment.sub_category.handling]
        ),
    }
    template = loader.get_template('email/signal_created.txt')
    message = template.render(context)
    return message


def send_mail_reporter_status_changed(signal, status):
    """Send a notification e-mail to the reporter about status change of the given `Signal` object.

    :param signal: Signal object
    :param status: Status object
    :returns: number of successfully send messages
    """
    signal_is_afgehandeld = status.state == workflow.AFGEHANDELD
    email = get_valid_email(signal)
    if not signal_is_afgehandeld or not email:
        return None

    subject = f'Betreft melding: {signal.id}'
    message = create_status_change_notification_message(signal, status)
    to = signal.reporter.email

    return send_mail(subject, message, settings.NOREPLY, (to, ))


def create_status_change_notification_message(signal, status):
    """Create e-mail body message about status change of the given `Signal` object.

    :param signal: Signal object
    :param status: Status object
    :returns: message (str)
    """
    context = {
        'signal': signal,
        'status': status,
    }
    template = loader.get_template('email/signal_status_changed.txt')
    message = template.render(context)
    return message
