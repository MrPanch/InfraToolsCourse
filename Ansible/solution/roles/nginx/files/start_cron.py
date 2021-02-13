#! /usr/bin/env python3

from crontab import CronTab

JOB_COMMENT = 'Update nginx uptime'

if __name__ == '__main__':
    cron = CronTab(user='root')
    # remove all previous crons, it is better to use cron.remove(comment=JOB_COMMENT), but it didn`t work :( 
    cron.remove_all()
    job = cron.new(command='sed -i "s/is .*$/is $(($(ps -o etimes= -p $(cat /var/run/nginx.pid)) / 60)) minutes/" /opt/service_state', comment=JOB_COMMENT)
    job.minute.every(1)
    cron.write()
    print('Running cron')
