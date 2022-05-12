# Libraries
import imaplib
import email
from email.header import decode_header
import datetime
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from imapclient import IMAPClient

# Testing
from grappa import should


# Dict with one key for array of elements
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


# Spam detecter class
class SpamDetected:
    def __init__(self, user, password, server):
        # logging:
        self.user = user
        self.password = password
        # Initiate a connection with the host
        self.server = server

    def decode(self):
        counter = []

        # Dict for counting latter's and numbs in subject+budy
        d = {'Letters': 0, 'Numbers': 0}

        SubjectListSorted = []
        BodyListSorted = []

        SubjectDictlist = Dictlist()
        BodyDictlist = Dictlist()

        # Remake date into needed format
        CurrentDate = (datetime.datetime.now()).strftime("%d %b %Y")

        if CurrentDate[0] == '0':
            RedefinedDate = CurrentDate[1] + CurrentDate[2] + CurrentDate[3] + CurrentDate[4] + CurrentDate[5] + \
                            CurrentDate[6] + CurrentDate[7] + CurrentDate[8] + CurrentDate[9] + CurrentDate[10]
        else:
            RedefinedDate = CurrentDate

        # login into the gmail account
        imap = imaplib.IMAP4_SSL(self.server)
        imap.login(self.user, self.password)

        # Using SELECT to choose the e-mails.
        res, messages = imap.select('INBOX')

        # Calculating the total number of sent Emails
        messages = int(messages[0])

        # Number of recent e-mails to be fetched
        n = 20

        # Iterating over the sent emails
        for i in range(messages, messages - n, -1):
            res, msg = imap.fetch(str(i), "(RFC822)")  # Using the RFC822 protocol
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # Retrieving the senders email
                    From = msg["From"]

                    # Retrieving the subject of the email
                    subject = msg["Subject"]

                    # Retrieving the date of the email
                    DateOfMassages = msg["Date"]

                    # Remake date of mails into needed format (should be rewritten)
                    DateOfMassages_var = DateOfMassages[5] + DateOfMassages[6] + DateOfMassages[7] + DateOfMassages[8] \
                                         + DateOfMassages[9] + DateOfMassages[10] + DateOfMassages[11] \
                                         + DateOfMassages[12] + DateOfMassages[13] + DateOfMassages[14] + \
                                         DateOfMassages[15]

                    if DateOfMassages_var[0] == '0':
                        DateOfMassages_var = DateOfMassages[6] + DateOfMassages[7] + DateOfMassages[8] + \
                                             DateOfMassages[9] + DateOfMassages[10] + DateOfMassages[11] \
                                             + DateOfMassages[12] + DateOfMassages[13] + DateOfMassages[14] + \
                                             DateOfMassages[15]

                    # Revue current date with mails day (it's better to wound way how to immediately
                    # get mail with needed date without checking)
                    if DateOfMassages_var == RedefinedDate:

                        # Create dict where key is sender and parameters is subjects
                        counter.append(From)
                        tu = From

                        decode_header(msg["Subject"])[0][0] | should.exists

                        yo = decode_header(msg["Subject"])[0][0]  # дописать если нет сабджекта
                        SubjectDictlist[tu] = yo

                        # Create dict where key is sender and parameters is budy of letter
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    body = ""
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    BodyDictlist[From] = body

        # This variable creates container with keys which matching our requirement be larger than 9
        cont = list(x for x in set(counter) if counter.count(x) >= 2)

        cont | should.not_be.empty

        # Checking if there exist elements which less the 10. If them exist, it will delete them.
        x = 0
        while x < len(SubjectDictlist.keys()):
            if list(SubjectDictlist.keys())[x] in cont:
                pass
            else:
                SubjectDictlist.pop(list(SubjectDictlist.keys())[x])
                x -= 1
            x += 1

        x = 0
        while x < len(BodyDictlist.keys()):
            if list(BodyDictlist.keys())[x] in cont:
                pass
            else:
                BodyDictlist.pop(list(BodyDictlist.keys())[x])
                x -= 1
            x += 1

        # Avoiding massages from logging user
        try:
            del SubjectDictlist[self.user]
        except KeyError:
            print('there is no masage from you')

        # Create lists with only subjects and body's which already have been sorted
        for each in SubjectDictlist.values():
            for x in each: x | should.be.a('string')
            SubjectListSorted += each

        for each in BodyDictlist.values():
            for x in each: x | should.be.a('string')
            each = [i.split('\r\n', 1)[0] for i in each]

            BodyListSorted += each

        if len(BodyDictlist.values()) != 0 or len(SubjectDictlist.values()) != 0:
            d | should.not_be.empty

        # Indicate letters and numbers
        for each in " ".join(BodyListSorted):
            if each.isalpha():
                d['Letters'] += 1
            if each.isdigit():
                d['Numbers'] += 1
            else:
                pass

        for each in " ".join(SubjectListSorted):

            if each.isalpha():
                d['Letters'] += 1
            if each.isdigit():
                d['Numbers'] += 1
            else:
                pass

        # Create main string which will be sent like a report
        mainstring = "Received mails on themes:  " + ", ".join(SubjectListSorted) + " With messages: " + "\n".join(
            BodyListSorted) + \
                     "It contains " + str(d['Letters']) + " letters and " + str(d['Numbers']) + " numbers."

        # Sending mail
        recipients = [self.user]

        msg = MIMEText(mainstring, 'plain', 'utf-8')
        msg['Subject'] = Header('subject', 'utf-8')
        msg['From'] = self.user
        msg['To'] = ", ".join(recipients)

        # send it via gmail
        s = SMTP_SSL(self.server, 465, timeout=10)
        s.set_debuglevel(1)
        try:
            s.login(self.user, self.password)
            s.sendmail(msg['From'], recipients, msg.as_string())
        finally:
            s.quit()

        # Deleting massage
        mail = IMAPClient(self.server, ssl=True, port=993)
        mail.login(self.user, self.password)
        mail.select_folder('Inbox')

        for each in SubjectListSorted:
            delMsg = mail.search('subject "' + each + '"')
            mail.delete_messages(delMsg)


if __name__ == '__main__':
    SpamDetected('dan020304dan93@gmail.com', 'ufggzyqlhvrnrbic', "imap.gmail.com").decode()

'''
 for c in each:
        if isinstance(c, type(b'')):
            listt = ["".join(c.decode("utf-8"))]
            st += listt
            print('bytes found')
        else:
'''

# print(BodyListSorted)
# print(SubjectListSorted)

'''
    for v in each:
        if isinstance(v, type(b'')):
            listt = ["".join(v.decode("utf-8"))]
            stt += listt.decode("utf-8")
        else:
'''

# print(d['Numbers'], d['Letters'])


# print(mainstring)


# create message


'''
message = imap.search(None, 'subject "This Is a SPAM Subject"')
messages = messages[0].split()
for x in messages:
    message = imap.store(x, '+X-GM-LABELS', '\\Trash')
'''
