# -*- coding: utf-8 -*-
import time
import smtplib

class EmailAlarmUtility:

    def trigger(self, route_detail, flight_detail, date):

        gmail_user = 'sucinusxjy@gmail.com'
        gmail_password = "bnnbuvzcasddtmgw"

        sent_from = gmail_user
        to = ['SOME_EMAIL']
        subject = 'Found ticket to buy'
        body = '{} {} -> {} @ {} on {} for ￥{}!'.format(flight_detail["flight_num"].encode('utf-8'),
                                                        route_detail["departure_city"].encode('utf-8'),
                                                        route_detail["arrival_city"].encode('utf-8'),
                                                        route_detail["departure_time"].encode('utf-8'),
                                                        date,
                                                        flight_detail["ticket_price"].encode('utf-8'))

        email_text = 'Subject: {}\n\n{}'.format(subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print 'Email sent!'
        except:
            print 'Something went wrong...'

        time.sleep(600)