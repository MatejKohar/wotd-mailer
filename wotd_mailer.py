# wotd_mailer.py - A script to get the DeutschPerfekt Word of the Day and email
# it to a set e-mail address.

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
    return results

def constructMessage(WotDInfo: dict) -> Message:
    """Return an email.Message from the *WotDInfo*\ .

    Fill in the sender and receiver information as well as the email body.
    """
    pass

def sendWotDMessage(WotDMessage: Message) -> None:
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
