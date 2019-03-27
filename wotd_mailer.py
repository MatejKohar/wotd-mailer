# wotd_mailer.py - A script to get the DeutschPerfekt Word of the Day and email
# it to a set e-mail address.
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
    """Scrape the website for the Word of the Day.

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
    """Return an email.Message from the *WotDInfo*\ .

    Fill in the sender and receiver information as well as the email body.
    """
    theDate = date.today()
    message = EmailMessage()
    message['From'] = os.environ['GMAIL_ADDRESS']
    message['To'] = os.environ['GMAIL_ADDRESS']
    message['Subject'] = f'Wort des Tages {theDate.strftime("%d.%m%Y")}'
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
    """
    return None

def main():
    """Run the scraper, construct, and send the message."""
    WotDInfo = scrapeWotD()
    if WotDInfo is None:
        sys.exit(0)
    WotDMessage = constructMessage(WotDInfo)
    sendWotDMessage(WotDMessage)

if __name__ == '__main__':
    main()
