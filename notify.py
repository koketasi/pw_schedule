
import httpx
from supabase import create_client
import os
from datetime import datetime
from zoneinfo import ZoneInfo 

URL= os.environ.get('SUPABASE_URL')
KEY= os.environ.get('SUPABASE_KEY')
supabase = create_client(URL, KEY)

def notify():
    now =datetime.now(ZoneInfo("Asia/Tokyo"))
    current_year=str(now.year)
    current_month=str(now.month)
    current_day=str(now.day)
    current_hour=str(now.hour)
    current_minute=str(now.minute).zfill(2)

    try:
        response=supabase.table('schedule').select('*')\
        .eq('year',current_year).eq('month',current_month).eq('day',current_day).eq('hour',current_hour).eq('minute',current_minute)\
        .execute()
        schedule_list=response.data
    except Exception as e:  #エラーが起きると変数eにエラー内容を入れる
        print(f'データベースエラー{e}')
        return
    
    for schedule in schedule_list:
        webhook_url=None
        webhook_url=schedule.get('webhook_url')
    
        if webhook_url:
            message={
                'content':f'スケジュールWEBアプリの通知です\n{schedule["hour"]}:{schedule["minute"]}\n{schedule["event"]}'
            }
            try:
                response2=httpx.post(webhook_url,json=message)
                if 200<=response2.status_code<300:
                    print(f'成功')    
                else:
                    print(f'失敗{response2.status_code}')
            except Exception as e:
                print(f'通知エラー{e}')

if __name__=='__main__':
    notify()