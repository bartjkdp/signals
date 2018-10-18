from django.core import mail
from django.test import TestCase

from signals.apps.email_integrations.integrations import core
from signals.apps.signals import workflow
from tests.apps.signals.factories import SignalFactory, StatusFactory


class TestCore(TestCase):

    def setUp(self):
        self.signal = SignalFactory.create(reporter__email='foo@bar.com')
        self.signal_invalid = SignalFactory.create(reporter__email='no-valid-email-address')

    def test_get_valid_email(self):
        email = core.get_valid_email(self.signal)
        self.assertEqual(email, 'foo@bar.com')

    def test_get_valid_email_invalid(self):
        email = core.get_valid_email(self.signal_invalid)
        self.assertEqual(email, None)

    def test_send_mail_reporter_created(self):
        num_of_messages = core.send_mail_reporter_created(self.signal)

        self.assertEqual(num_of_messages, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Bedankt voor uw melding ({self.signal.id})')
        self.assertEqual(mail.outbox[0].to, ['foo@bar.com', ])

    def test_send_mail_reporter_created_invalid_email(self):
        num_of_messages = core.send_mail_reporter_created(self.signal_invalid)

        self.assertEqual(num_of_messages, None)

    def test_create_initial_create_notification_message(self):
        message = core.create_initial_create_notification_message(self.signal)

        self.assertIn(str(self.signal.id), message)
        self.assertIn(self.signal.text, message)
        self.assertIn(self.signal.reporter.email, message)

    def test_send_mail_reporter_status_changed(self):
        # Prepare signal with status change to `AFGEHANDELD`.
        status = StatusFactory.create(_signal=self.signal, state=workflow.AFGEHANDELD)
        self.signal.status = status
        self.signal.status.save()

        num_of_messages = core.send_mail_reporter_status_changed(self.signal, status)

        self.assertEqual(num_of_messages, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Betreft melding: {self.signal.id}')
        self.assertEqual(mail.outbox[0].to, ['foo@bar.com', ])

    def test_send_mail_reporter_status_changed_no_status_afgehandeld(self):
        num_of_messages = core.send_mail_reporter_status_changed(self.signal, self.signal.status)

        self.assertEqual(num_of_messages, None)

    def test_send_mail_reporter_status_changed_invalid_email(self):
        # Prepare signal with status change to `AFGEHANDELD`.
        status = StatusFactory.create(_signal=self.signal_invalid, state=workflow.AFGEHANDELD)
        self.signal_invalid.status = status
        self.signal_invalid.status.save()

        num_of_messages = core.send_mail_reporter_status_changed(self.signal_invalid, status)

        self.assertEqual(num_of_messages, None)

    def test_create_status_change_notification_message(self):
        # Prepare signal with status change to `AFGEHANDELD`.
        status = StatusFactory.create(_signal=self.signal, state=workflow.AFGEHANDELD, text='Done.')
        self.signal.status = status
        self.signal.status.save()

        message = core.create_status_change_notification_message(self.signal, self.signal.status)

        self.assertIn(str(self.signal.id), message)
        self.assertIn(self.signal.text, message)
        self.assertIn(self.signal.status.text, message)
