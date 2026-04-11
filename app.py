
from flask import  Flask,render_template, request, redirect, url_for
from pathlib  import Path
from werkzeug.utils import secure_filename
from supabase import create_client
import os
import hashlib
#from notify import notify

#import sqlite3

URL= os.environ.get('SUPABASE_URL')
KEY= os.environ.get('SUPABASE_KEY')
supabase = create_client(URL, KEY)

app = Flask(__name__)


#def init_db():
   # with sqlite3.connect(database) as con:
  #      con.execute('CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, year TEXT,month TEXT,day TEXT, hour TEXT,minute TEXT,event TEXT, file_name TEXT, file_title TEXT)')
        #存在しないなら作らない
 #       con.commit()
 
#init_db()


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method=='POST':
        action=request.form['action']
        
        match action:
            case 'add': #追加
                year=request.form['year']
                month=request.form['month']
                day=request.form['day']
                hour=request.form['hour']
                miute=request.form['minute']
                event=request.form['event']
                file=request.files.get('name')
                file_name=None
                file_title=request.form.get('title')

                if file and file.filename!='':
                    file_name=secure_filename(file.filename)
                    file.save(Path(__file__).parent /"static"/ file_name)

                webhook_url=request.form.get('webhook_url')
                password=request.form.get('password')
                search_key=request.form.get('search_key')

                if password:# noneをハッシュ化しないため
                    key=hashlib.sha256(password.encode()).hexdigest()#encodeでバイトにして、hashlib.sha256でハッシュ化、最後に16進数にする
                else:
                    key=None
                #with sqlite3.connect(database) as con:
                #    con.execute('INSERT INTO schedule (year,month,day,hour,minute,event,file_name,file_title)VALUES(?,?,?,?,?,?,?,?)',[year,month,day,hour,miute,event,file_name,file_title])
                #    con.commit()
                supabase.table('schedule').insert({
                    'year':year,'month':month,'day':day,'hour':hour,'minute':miute,
                    'event':event,'file_name':file_name,'file_title':file_title,'password':key,'webhook_url':webhook_url
                  }).execute()
                
                if search_key:
                    return redirect(url_for('index',search=search_key))
                else:
                    return redirect(url_for('index'))

            case 'edit': #編集
                row=request.form['row']
                year=request.form['year']
                month=request.form['month']
                day=request.form['day']
                hour=request.form['hour']
                miute=request.form['minute']
                event=request.form['event']
                file=request.files.get('name')
                current_name=request.form.get('current_name')
                file_title=request.form.get('title')

                if file and file.filename!='':
                    current_name=secure_filename(file.filename)
                    file.save(Path(__file__).parent /"static"/ current_name)
                
          #      with sqlite3.connect(database) as con:
           #         con.execute('UPDATE schedule SET year=?,month=?,day=?,hour=?,minute=?,event=?,file_name=?,file_title=? WHERE rowid=?',[year,month,day,hour,miute,event,current_name,file_title,row])
            #        con.commit()
                webhook_url=request.form.get('webhook_url')
                password=request.form.get('password')
                search_key=request.form.get('search_key')

                if password:# noneをハッシュ化しないため
                    key=hashlib.sha256(password.encode()).hexdigest()#encodeでバイトにして、hashlib.sha256でハッシュ化、最後に16進数にする
                    
                    supabase.table('schedule').update({
                        'year':year,'month':month,'day':day,'hour':hour,'minute':miute,
                        'event':event,'file_name':current_name,'file_title':file_title,'password':key,'webhook_url':webhook_url
                    }).eq('id',int(row)).execute()

                else:#入力がないならpasswordのカラムを変更しない
                    supabase.table('schedule').update({
                        'year':year,'month':month,'day':day,'hour':hour,'minute':miute,
                        'event':event,'file_name':current_name,'file_title':file_title,'webhook_url':webhook_url
                    }).eq('id',int(row)).execute()

                if search_key:
                    return redirect(url_for('index',search=search_key))
                else:
                    return redirect(url_for('index'))

            case 'delete': #削除 
                    #con=sqlite3.connect(database)
                #con.execute('DELETE FROM schedule  WHERE  rowid=?',(row,))
                #con.commit()
                #con.close()
                row=request.form['row']
                search_key=request.form.get('search_key')

                supabase.table('schedule').delete().eq('id',int(row)).execute()
                
                if search_key:
                    return redirect(url_for('index',search=search_key))
                    
                else:
                    return redirect(url_for('index'))

            case 'search':#　パスワード検索用
                
                search_password=request.form.get('password')
                if search_password:# noneをハッシュ化しないため
                    search_key=hashlib.sha256(search_password.encode()).hexdigest()
                else:
                    search_key=None

                return redirect(url_for('index', search=search_key))
                #return render_template("index.html",schedule_list=search_schedule_list,search_key=search_key)#search_keyは暗号化されてる


    #con=sqlite3.connect(database)
   
    #schedule_list=con.execute('SELECT year,month,day,hour,minute,event,file_name,file_title,rowid from schedule where event is not NULL').fetchall()
    #con.close()

    search_key = request.args.get('search')
    if search_key:
        response=supabase.table('schedule').select('*').eq('password',search_key).execute()

    else:
        response=supabase.table('schedule').select('*').not_.is_('event','null').is_('password','null').execute()

    row_list=response.data
    schedule_list=[
        (
            schedule['year'],
            schedule['month'],
            schedule['day'],
            schedule['hour'],
            schedule['minute'],
            schedule['event'],
            schedule['file_name'],
            schedule['file_title'],
            schedule['id'],
            schedule['webhook_url']

        )for schedule in row_list
    ]
    
  
    return render_template("index.html",schedule_list=schedule_list,search_key=search_key)

#def notification():
  #  while True:
   #     notify()
 #       time.sleep(60)

#threading.Thread(target=notification, daemon=True).start()#並行処理するため
if __name__ == "__main__":
    
   
    port=int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port )
    #app.run(debug=True)
 

