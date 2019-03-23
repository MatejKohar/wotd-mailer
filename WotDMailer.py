# WotDMailer.py - A script to get the DeutschPerfekt Word of the Day and email
# it to a set e-mail address.

from email.message import Message
import os
import smtplib
import sys

from selenium import webdriver

def scrapeWotD() -> dict:
    """Scrape the website for the Word of the Day.

    Return a dictionary with the word, word-type, explanation and example
    sentence. Return None if scraping fails.
    """
    return None

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
