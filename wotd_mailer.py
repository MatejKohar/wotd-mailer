# wotd_mailer.py - A script to get the DeutschPerfekt Word of the Day and email
# it to yourself through GMail.
from datetime import date
from email.message import EmailMessage
import os
import smtplib
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapeWotD() -> dict:
    """Scrape the DeutschPerfect website for the Word of the Day.

    Return a dictionary with the word, word-type, explanation and example
    sentence. Return None if scraping fails.
    """
    results = {}
    browser = webdriver.Firefox()
    browser.get('https://www.deutsch-perfekt.com/')
    # wait till the wotd section has loaded
    try:
        header = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'wotd-header')))
        info = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'wotd-info')))
    except TimeoutException:
        browser.quit()
        return None

    word = header.find_element_by_tag_name('div')
    type = header.find_element_by_tag_name('small')
    explanation = info.find_element_by_xpath('./div[1]/p')
    example = info.find_element_by_xpath('./div[last()]/p')

    results = {'word': word.text,
               'type': type.text,
               'explanation': explanation.text,
               'example': example.text
               }
    browser.quit()
    return results

def constructMessage(WotDInfo: dict) -> EmailMessage:
    """Return an email.EmailMessage from the *WotDInfo*\ .

    Fill in the sender and receiver information as well as the email body.
    The email address to be used must be stored in the environment variable
    $GMAIL_ADDRESS
    """
    theDate = date.today()
    message = EmailMessage()
    try:
        message['From'] = os.environ['GMAIL_ADDRESS']
        message['To'] = os.environ['GMAIL_ADDRESS']
    except KeyError:
        print("Set $GMAIL_ADDRESS environment variable to use this script.")
        return None
    message['Subject'] = f'Wort des Tages {theDate.strftime("%d.%m.%Y")}'
    message_body = f"""\
    Wort: {WotDInfo['word']}
    Wortart: {WotDInfo['type']}
    Erklärung: {WotDInfo['explanation']}
    Beispielsatz: {WotDInfo['example']}"""
    message.set_content(message_body)

    return message

def sendWotDMessage(WotDMessage: EmailMessage) -> None:
    """Send the *WotDMessage* via GMail.

    Connect to the GMail SMTP server, authenticate, and send the *WotDMessage*\ .
    Password must be stored in the $GMAIL_PASSWD environment variable.
    """
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(os.environ['GMAIL_ADDRESS'], os.environ['GMAIL_PASSWD'])
        except smtplib.SMTPAuthenticationError:
            print('Wrong password. Reset your $GMAIL_PASSWD environment',
                  'variable to the correct password.'
                  )
            return
        except KeyError:
            # If we got this far, it must be the password missing.
            print('Set $GMAIL_ADDRESS environment variable to use this script.')
            return

        smtp.send_message(WotDMessage)

def main():
    """Run the scraper, construct, and send the message."""
    WotDInfo = scrapeWotD()
    if WotDInfo is None:
        sys.exit(0)
    WotDMessage = constructMessage(WotDInfo)
    sendWotDMessage(WotDMessage)

if __name__ == '__main__':
    main()
