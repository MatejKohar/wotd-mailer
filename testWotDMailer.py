import os
import smtplib
import unittest

import wotd_mailer


class TestWotDMailer(unittest.TestCase):

    @unittest.skip('Testing the message constructor now')
    def test_scrapeWotD(self):
        """Test the scraping function of the WotDMailer script."""
        # Populate correct_answers with the daily Deutsch Perfekt content for
        # testing.
        correct_answers = {'word': 'die Reiseunterlagen (Pl.)',
                           'type': 'Nomen',
                           'explanation': 'Dokumente für eine Reise (z. B. Hotelreservierung, Informationen)',
                           'example': 'Hast du schon die Reiseunterlagen eingepackt?'
                           }
        results = wotd_mailer.scrapeWotD()
        for key, value in correct_answers.items():
            with self.subTest(key = key):
                self.assertEqual(value, results.get(key))

    def test_constructMessage(self):
        scraped_data = {'word': 'die Reiseunterlagen (Pl.)',
                        'type': 'Nomen',
                        'explanation': 'Dokumente für eine Reise (z. B. Hotelreservierung, Informationen)',
                        'example': 'Hast du schon die Reiseunterlagen eingepackt?'
                         }
        message = wotd_mailer.constructMessage(scraped_data)
        self.assertEqual(os.environ['GMAIL_ADDRESS'], message['From'])
        self.assertEqual(os.environ['GMAIL_ADDRESS'], message['To'])
        self.assertEqual('Wort des Tages', message['Subject'])
        message_body = message.get_content()
        self.assertIn('Reiseunterlagen', message_body)
        self.assertIn('Nomen', message_body)
        self.assertIn('Dokumente', message_body)
        self.assertIn('eingepackt', message_body)

    def test_sendWotDMessage(self):
        pass

if __name__ == '__main__':
    unittest.main()
