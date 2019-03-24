import email
import smtplib
import unittest

import wotd_mailer


class TestWotDMailer(unittest.TestCase):

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
            with self.subtest(key = key):
                self.assertEqual(value, results.get(key))

    def test_constructMessage(self):
        pass

    def test_sendWotDMessage(self):
        pass
