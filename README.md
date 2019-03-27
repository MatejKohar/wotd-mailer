#Word of the Day mailer

This script scrapes www.deutsch-perfekt.com for its daily updated Word of the day and then connects to GMail's SMTP server to mail it to yourself.

###Requirements

+ Python 3.6
+ Selenium 2
+ Firefox
+ geckodriver

###Usage

Your email address must be stored in the $GMAIL_ADDRESS environment variable.
Your password (it is recommended to use a separate app password) must be stored in the $GMAIL_PASSWD environment variable.
Set up a cronjob to perform once daily.
