from sqlalchemy import  create_engine,text
import os
db_conn_str = "mysql+pymysql://2wwiif0y09umup9316og:pscale_pw_5BhhFz5AkxRWUOnAASfWDvfD33JA4l6rGtHjU50ti80@aws.connect.psdb.cloud/portfolio?charset=utf8mb4"

engine = create_engine(db_conn_str, connect_args={
  "ssl":{
    "ssl_ca": "/etc/ssl/cert.pem"
  }
},echo=True) 
def row_to_dict(result_proxy):
    row = result_proxy.fetchone()
    if row:
        column_names = result_proxy.keys()
        values = row
        diction = dict(zip(column_names, values))
        return diction
    else:
        return {}
def rows_to_list_of_dicts(result_proxy):
    rows = []
    for row in result_proxy:
        column_names = result_proxy.keys()
        values = row
        diction = dict(zip(column_names, values))
        rows.append(diction)
    return rows

def login(name, pword):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT username, password FROM users WHERE username = :val"),{"val": name})
        conn.execute(text("Update users set status='Active' where username=:val"),{"val": name})
        d = row_to_dict(result)
        if not d:
          return("Username not found")
        elif d['password'] == pword:
          return("Welcome")
        else:
          return("Wrong password")
def logout(name):
    with engine.connect() as conn:
        conn.execute(text("Update users set status='Inactive' where username=:val"), {"val": name})


def signupinsert(data):
  username = data['username']
  fullname = data['fullname']
  email = data['email']
  gender= data['gender']
  password = data['password']
  try:
        with engine.connect() as conn:
           conn.execute(
               text("insert into users(`username`, `fullname`, `email`,`gender`,`created_date`,`password`,`status`)values(:z,:x,:y,:a,curdate(),:c,'Inactive')"),
              {"x": fullname,"z": username, "y": email, "a": gender,"c": password}
           )
        print("Success")
        return "Success"
  except Exception as e:
        return "Username Already in use"
with engine.connect() as conn:
        r=conn.execute(text("select * from users"))
        print(r)
