
from flask import  Flask,render_template, request, redirect, url_for
from pathlib  import Path
from werkzeug.utils import secure_filename
from supabase import create_client
import os
import hashlib
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

                password=request.form.get('password')
                if password:# noneをハッシュ化しないため
                    key=hashlib.sha256(password.encode()).hexdigest()#encodeでバイトにして、hashlib.sha256でハッシュ化、最後に16進数にする


                #with sqlite3.connect(database) as con:
                #    con.execute('INSERT INTO schedule (year,month,day,hour,minute,event,file_name,file_title)VALUES(?,?,?,?,?,?,?,?)',[year,month,day,hour,miute,event,file_name,file_title])
                #    con.commit()
                supabase.table('schedule').insert({
                    'year':year,'month':month,'day':day,'hour':hour,'minute':miute,'event':event,'file_name':file_name,'file_title':file_title,'password':key
                  }).execute()
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
                supabase.table('schedule').update({
                    'year':year,'month':month,'day':day,'hour':hour,'minute':miute,'event':event,'file_name':current_name,'file_title':file_title
                }).eq('id',int(row)).execute()

                return redirect(url_for('index'))

            case 'delete': #削除
                row=request.form['row']
                #con=sqlite3.connect(database)
                #con.execute('DELETE FROM schedule  WHERE  rowid=?',(row,))
                #con.commit()
                #con.close()
                supabase.table('schedule').delete().eq('id',int(row)).execute()
                return redirect(url_for('index'))

            case 'search':#　パスワード検索用
                search_password=request.form.get('password')
                search_response=supabase.table('schedule').select('*').eq('password',search_password).execute()
                search_row_list=search_response.data
                search_schedule_list=[
                    (
                        row['year'],
                        row['month'],
                        row['day'],
                        row['hour'],
                        row['minute'],
                        row['event'],
                        row['file_name'],
                        row['file_title'],
                        row['id'],
                        row['password']
                    )for row in search_row_list
                ]
                return render_template("index.html",schedule_list=search_schedule_list)


    #con=sqlite3.connect(database)
   
    #schedule_list=con.execute('SELECT year,month,day,hour,minute,event,file_name,file_title,rowid from schedule where event is not NULL').fetchall()
    #con.close()
    response=supabase.table('schedule').select('*').not_.is_('event',None).is_('password',None).execute()
    row_list=response.data
    schedule_list=[
        (
            row['year'],
            row['month'],
            row['day'],
            row['hour'],
            row['minute'],
            row['event'],
            row['file_name'],
            row['file_title'],
            row['id']

        )for row in row_list
    ]
    
  
    return render_template("index.html",schedule_list=schedule_list)

if __name__ == "__main__":
    
   
    port=int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port )
    #app.run(debug=True)
 

