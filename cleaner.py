import os
import sys
from tabulate import tabulate
from Bcolors import Bcolors
from time import sleep
from dotenv import load_dotenv, dotenv_values
import mysql.connector



def main():
    # Connect to database and get mailboxes in DB
    load_dotenv()
    mailboxes_db = connect()

    domain = os.environ['DOMAIN']
    maildir = '/home/vmail/' + domain + '/'
    print("Directory with mailboxes - ", maildir)

    removed_dir = '/home/vmail/_deleted/'
    print("Directory for deleted mailboxes - ", removed_dir)
    sleep(1.5)

    current_file = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.curdir)
    maildir = os.path.join(current_dir, 'mail', domain)

    mailboxes = os.listdir(maildir)
    mailboxes.sort()
    results = []
    mb_to_be_removed = []
    stat = {
        'good': 0,
        'bad': 0
    }

    for mailbox in mailboxes:
        full_path = os.path.join(maildir, mailbox)

        if not os.path.isdir(full_path):
            continue

        if not mailbox in mailboxes_db:
            results.append([Bcolors.warning(mailbox), 'Not in DB'])
            # print(Bcolors.warning(f"{mailbox} \t\t - not in DB. User already removed"))
            mb_to_be_removed.append(full_path)
            stat['bad'] += 1
        else:
            results.append([Bcolors.green(mailbox), 'OK'])
            # print(Bcolors.green(f"{mailbox} \t\t - is OK"))
            stat['good'] += 1

    print(tabulate(results, headers=['Username', 'Status'], showindex=True))

    print(f"\n\n OK - {stat['good']}.\n BAD - {stat['bad']}\n")

    if len(mb_to_be_removed) > 0:
        print("\n\n\n              Bash commands:\n\n")
        for mb in mb_to_be_removed:
            print(f"mv {mb} {removed_dir}")


def connect():
    config = dotenv_values(".env")
    try:
        cnx = mysql.connector.connect(
            host = config['DB_HOST'],
            user = config['DB_USER'],
            password = config['DB_PASSWORD'],
            database = config['DB_DATABASE']
        )

    except mysql.connector.Error as e:
        print(e)
        sys.exit()

    cursor = cnx.cursor()

    cursor.execute("""
        SELECT username,domain
        FROM mailuser
        ORDER BY domain,username
        """)

    myresult = cursor.fetchall()
    mailboxes_db = []

    for itm in myresult:
        mailboxes_db.append(itm[0])

    cursor.close()
    cnx.close()

    return mailboxes_db


if __name__ == '__main__':
    main()

