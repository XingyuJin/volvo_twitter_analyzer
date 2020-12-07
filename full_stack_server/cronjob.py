from apscheduler.schedulers.blocking import BlockingScheduler

from dao.mysql_processor import write_mysql
from dao.twitter_crawler import Twitter, VolvoAccount

CSV_PATH = "./data/"


def start_job():
    # Update Twitter Mention Data
    mention = Twitter()
    mention.run()

    # Update Volvo Account Data
    account = VolvoAccount()
    account.run()

    write_mysql(f"{CSV_PATH}volvo0701-1101.csv", "twitter_data.`volvo0701-1101`")
    write_mysql(f"{CSV_PATH}volvocarusa_account.csv", "twitter_data.volvocarusa_account")


def main():
    sched = BlockingScheduler()
    sched.add_job(start_job, 'cron', day_of_week='0-6', hour='0')
    sched.start()


if __name__ == '__main__':
    main()
