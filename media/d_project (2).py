'''
Created on Feb 11, 2018

@author: muthu
'''
from flask.app import Flask
from flask.templating import render_template
from flask.globals import request, session
from werkzeug.utils import secure_filename
import os
import boto
import boto.s3
import sys
from boto.s3.key import Key
from Crypto.Cipher import AES
from flask_mail import Mail,Message



AWS_ACCESS_KEY_ID = 'AKIAIPKJPA4BHGD4PNXQ'
AWS_SECRET_ACCESS_KEY = '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'





app=Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'project2016mails@gmail.com'
app.config['MAIL_PASSWORD'] = 'messengerforall'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
import random
import string
random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
key="bGCBVqxEEejIAf9w4WW9NsyGCB6UHobj"
app.secret_key="hello"
import MySQLdb
con=MySQLdb.connect(host='localhost' ,port=3306,user='root',passwd='root',db='cloud')
cmd=con.cursor()
path="C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\image"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

cloud_path="C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\cloud"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open('C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\downloads\\'+file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open('C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\downloads\\'+"dcr"+file_name[:-4], 'wb') as fo:
        fo.write(dec)

@app.route('/index')
def main():
    return render_template('index.html')
@app.route('/twofactor')
def twofactor():
    do=request.args.get('dec')
    session['did']=do
    cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid and cloud.id='"+str(do)+"'")
    dat=cmd.fetchone()
    return render_template('two factor.html',data=dat)
@app.route('/logout')
def logout():
    session.pop('id',None)
    return render_template('sender.html')
@app.route('/logoutrec')
def logoutrec():
    session.pop('id',None)
    return render_template('receiver.html')
    
        
@app.route('/deleteuse')
def dele():
    id=session['id']
    cmd.execute("select * from reg")
    dat=cmd.fetchall()
    return render_template('delete.html',data=dat)

@app.route('/deleteuser',methods=['POST','GET'])
def deleteuser():
    idd=request.args.get('val')
    cmd.execute("delete from reg where lid='"+str(idd)+"'")
    cmd.execute("delete from login where id='"+str(idd)+"'")
    id=session['id']
    cmd.execute("select * from reg")
    dat=cmd.fetchall()
    con.commit()
    return render_template('delete.html',data=dat)
@app.route('/down')
def down():  
    bucket_name = 'hidethis'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
    key = bucket.get_key(request.args.get('myfile')+".enc")
    key.get_contents_to_filename('C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\downloads\\'+request.args.get('myfile')+".enc")
    decrypt_file(request.args.get('myfile')+".enc", "bGCBVqxEEejIAf9w4WW9NsyGCB6UHobj")
    return "Download Completed"
     
@app.route('/download')
def download():
    do=request.args.get('dec')
    session['did']=do
    cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid and cloud.id='"+str(do)+"'")
    dat=cmd.fetchone()
    return render_template('download.html',data=dat)

@app.route('/check',methods=['POST'])
def check():
    
    adjectives = request.form.getlist('match')
   
    
    for a in adjectives:
        
        did=session['did']
        cmd.execute("insert into access values(null,'"+a+"','"+did+"',curdate())")
        con.commit()
        cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid")
        dat=cmd.fetchall()
        return render_template('admin.html',data=dat)  
        
        
    
@app.route('/receiver')
def receiver():
    return render_template('receiver.html')
    
@app.route('/access',methods=['POST','GET'])
def access():
    dt=request.args.get('val')
    session['did']=dt
    cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid and cloud.id='"+str(dt)+"'")
    dat=cmd.fetchone()
    return render_template('access.html',data=dat)



@app.route('/tick',methods=['POST'])
def tick():
    cmd.execute("select * from reg")
    dat=cmd.fetchall()
    return render_template('tick.html',data=dat)
@app.route('/sender')
def sender():
    return render_template('sender.html')

@app.route('/delete',methods=['POST','GET'])
def delete():
    idd=request.args.get('val')
    cmd.execute("delete from cloud where id='"+idd+"'")
    id=session['id']
    cmd.execute("select * from cloud where uid='"+str(id)+"'")
    dat=cmd.fetchall()
    con.commit()
    return render_template('sender2.html',data=dat)
   
    
@app.route('/sendregister')
def sendregister():
    return render_template('sendregister.html')
@app.route('/sender1')
def sender1():
    return render_template('sender1.html')
@app.route('/upload',methods=['POST'])
def upload():
    f=request.files['pi']
    dataname=request.form['your_email']
    message=request.form['your_enquiry']
    id=session['id'] 
    cmd.execute("select * from cloud where uid='"+str(id)+"'")
    dat=cmd.fetchall()
     
    
    UPLOAD_FOLDER = cloud_path
    img=secure_filename(dataname)
    
      #  file.save(os.path.join(UPLOAD_FOLDER, filename))
    f.save(os.path.join(UPLOAD_FOLDER,secure_filename(dataname)))
    encrypt_file(UPLOAD_FOLDER+"\\"+img, key)
    bucket_name = 'hidethis'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)
    
    
    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
    
    testfile = cloud_path+"\\"+img+".enc"
    tes=testfile.split("\\")
    leng=len(tes)
    namef=tes[leng-1]
    
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    
    k = Key(bucket)
    k.key = namef
    k.set_contents_from_filename(testfile,
        cb=percent_cb, num_cb=10)



    cmd.execute("insert into cloud values(null,'"+img+"','"+dataname+"','"+message+"','"+str(id)+"',curdate())")
    con.commit()
    return render_template('sender1.html',data=dat)
    
@app.route('/sender2')
def sender2():
    id=session['id']
    cmd.execute("select * from cloud where uid='"+str(id)+"'")
    dat=cmd.fetchall()
    return render_template('sender2.html',data=dat)
@app.route('/securelogin')
def securelogin():
    return render_template('securelogin.html')

@app.route('/sender3')
def sender3():
   
    id=session['id']
    cmd.execute("select * from cloud where uid='"+str(id)+"'")
    dat=cmd.fetchall()
    return render_template('sender3.html',data=dat)

@app.route('/reg',methods=['POST'])
def reg():
    
        name=request.form['name']
        password=request.form['psw']
        email=request.form['email']
        number=request.form['number']
        address=request.form['address']
        birth=request.form['birth']
        pin=request.form['pincode']
        location=request.form['loc']
        f = request.files['pic']
        UPLOAD_FOLDER = path
        img=secure_filename(f.filename)
      #  file.save(os.path.join(UPLOAD_FOLDER, filename))
        f.save(os.path.join(UPLOAD_FOLDER,secure_filename(f.filename)))
        cmd.execute("insert into login values(null,'"+name+"','"+password+"','user')")
        id=con.insert_id()
        cmd.execute("insert into reg values('"+name+"','"+password+"','"+email+"','"+number+"','"+address+"','"+birth+"','"+pin+"','"+location+"','"+img+"','"+str(id)+"')")
        con.commit()
        return '''<html> <body>  <script> alert("Registration Successful")
            window.location="/sender"   </script></body>  </html> '''
    
     
     

     
@app.route('/sign',methods=['POST'])
def sign():
    name=request.form['your_name']
    password=request.form['your_email']
   
    cmd.execute("select * from login where username='"+name+"' and password='"+password+"'")
    d=cmd.fetchone()
    if d is None:
        return '''<html> <body>  <script> alert("Invalid user")
        window.location="/sender"   </script></body>  </html> '''
    
    session['id']=d[0]
    if (d[3]=="user"):
        return render_template('sender1.html')
    else:
        cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid")
        dat=cmd.fetchall()
        return render_template('admin.html',data=dat)
    con.commit()
    
    
    
    
@app.route('/receiversign',methods=['POST'])
def receiversign():
    name=request.form['your_name']
    password=request.form['your_email']
   
    cmd.execute("select * from login where username='"+name+"' and password='"+password+"'")
    d=cmd.fetchone()
    if d is None:
        return '''<html> <body>  <script> alert("Invalid user")
        window.location="/sender"   </script></body>  </html> '''
    
    session['id']=d[0]
    if (d[3]=="user"):
        id=session['id']
        print(id)
        cmd.execute("select cloud.*,reg.sendername from access,cloud,reg where cloud.id=access.did and access.rid='"+str(id)+"' and reg.lid=cloud.uid")
        dat=cmd.fetchall();
        return render_template('receiver1.html',data=dat)
    else:
        cmd.execute("select cloud.*,reg.sendername from reg,cloud where cloud.uid=reg.lid")
        dat=cmd.fetchall()
        return render_template('admin.html',data=dat)
    con.commit()
    
@app.route('/profile')
def profile():
    
    id=session['id']
    cmd.execute("select sendername,email,mobile,address,birth,location,image from reg where lid='"+str(id)+"'")
    dat=cmd.fetchone()
    return render_template('profile.html',data=dat)
@app.route('/factor')
def factor():
    cmd.execute("select email from reg")
    data=cmd.fetchall()
    
    
    
    
    return render_template('factor.html ',data=data)



@app.route('/factorupload',methods=['POST'])
def factorupload():
    f=request.files['pi']
    dataname=request.form['your_email']
    message=request.form['your_enquiry']
    email=request.form['email']
    id=session['id'] 
    cmd.execute("select * from cloud where uid='"+str(id)+"'")
    dat=cmd.fetchall()
     
    
    UPLOAD_FOLDER = cloud_path
    img=secure_filename(dataname)
    
      #  file.save(os.path.join(UPLOAD_FOLDER, filename))
    f.save(os.path.join(UPLOAD_FOLDER,secure_filename(dataname)))
    
    ju= random
    f= open("sruthi.txt","w+")
    f.write(ju)
    msg = Message('Your Key For Decryption ', sender = 'project2016mails@gmail.com', recipients = [email])
    msg.body = 'Decrypt Using this Key'+str(ju)
    mail.send(msg)
    
    encrypt_file(UPLOAD_FOLDER+"\\"+img, ju)
    bucket_name = 'hidethis'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)
    
    
    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
    
    testfile = cloud_path+"\\"+img+".enc"
    tes=testfile.split("\\")
    leng=len(tes)
    namef=tes[leng-1]
    
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    
    k = Key(bucket)
    k.key = namef
    k.set_contents_from_filename(testfile,
        cb=percent_cb, num_cb=10)



    cmd.execute("insert into twofactor values(null,'"+img+"','"+dataname+"','"+message+"','"+str(id)+"','"+str(email)+"',curdate())")
    con.commit()
    return render_template('sender1.html',data=dat)



@app.route('/two')
def two():
    cmd.execute("select twofactor.*,reg.sendername from reg,twofactor where twofactor.uid=reg.lid")
    data=cmd.fetchall()
    
    return render_template('/twodownload.html',data=data)


@app.route('/keyplease')
def keyplease():
    dat=request.args.get('dat')
    session['dat']=str(dat)
    return render_template('keyhere.html')

@app.route('/decry',methods=['POST'])
def decry():
    key1=request.form['your_email']
    strfile=session['dat']
    bucket_name = 'hidethis'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

    bucket = conn.create_bucket(bucket_name,location=boto.s3.connection.Location.DEFAULT)
    key = bucket.get_key(strfile+".enc")
    key.get_contents_to_filename('C:\\Users\\muthu\\Desktop\\project\\Facor\\project\\static\\downloads\\'+strfile+".enc")
    decrypt_file(strfile+".enc", key1)
    return ''' <html>
    <body>
    
    <script>alert("Download Success")
    window.location="/index"
    </script>
    </body>
    </html>   '''
    
    
    
    

if(__name__=="__main__"):
    app.run(debug=True)
