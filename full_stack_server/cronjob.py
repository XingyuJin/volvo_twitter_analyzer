from apscheduler.schedulers.blocking import BlockingScheduler

from dao.mysql_processor import write_mysql
from dao.twitter_crawler import Twitter, VolvoAccount, preprocess

CSV_PATH = ""


def start_job():
    # Update Twitter Mention Data
    n1, n2 = "volvo0501-1101.csv", "VolvoCarUSA.csv"
    mention = Twitter(n1)
    mention.run()
    preprocess(n1)

    # Update Volvo Account Data
    account = VolvoAccount(n2)
    account.run()
    preprocess(n2)

    write_mysql(f"{CSV_PATH}{n1}", "twitter_data.`volvomention`")
    write_mysql(f"{CSV_PATH}{n2}", "twitter_data.volvocarusa_account")


def main():
    sched = BlockingScheduler()
    sched.add_job(start_job, 'cron', day_of_week='0-6', hour='0')
    sched.start()


if __name__ == '__main__':
    main()
