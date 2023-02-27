from threading import Thread
import schedule
import yagmail
import os, time
from datetime import datetime

class Notify(Thread):

    def __init__(self, log, config, stats):
        super().__init__()
        self.log = log
        self.config = config
        self.stats = stats

        self.emailServer = os.getenv('emailServer')
        self.emailUsername = os.getenv('emailUsername')
        self.emailPassword = os.getenv('emailPassword')
        

    def run(self):
        schedule.every().day.at("09:00").do(self.dailyNotify)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def dailyNotify(self):
        yag = yagmail.SMTP(user = self.emailUsername, password = self.emailPassword, host = self.emailServer)
        now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        for account in self.config.accounts:
            acc = self.config.accounts[account]
            if acc['email']:
                totalDrops = self.stats.accountData[account]['totalDrops']
                subject = f'观赛引擎每日提醒({totalDrops})'
                contents = f'''
                截至{now}，账号'{acc['username']}'的生涯掉落总数为{totalDrops}。
                '''
                yag.send(to = acc['email'], subject = subject, contents = contents)
                time.sleep(10) # 间隔10s再发送

