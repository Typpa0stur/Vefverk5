from flask import Flask, render_template, request
import pyrebase

app = Flask(__name__)

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    # hér kemur tengingin þín við Firebase gagnagrunninn ( realtime database )
    "apiKey": "AIzaSyBUJlkBPkOyk-WPnpPtBlxnfxUEm2wLSyg",
    "authDomain": "vefverk5.firebaseapp.com",
    "databaseURL": "https://vefverk5.firebaseio.com",
    "projectId": "vefverk5",
    "storageBucket": "vefverk5.appspot.com",
    "messagingSenderId": "505433608658",
    "appId": "1:505433608658:web:5065321210b854cc21780b",
    "measurementId": "G-2Q94CFXMD5"
}

fb = pyrebase.initialize_app(config)
db = fb.database()

# Route sem keyrir upp login formið
@app.route('/')
def index():
    return render_template("index.html")

# Route sem keyrir upp register formið
@app.route('/register')
def register():
    return render_template("register.html")

# Route sem útfærir register virkni, ekkert annað en bara register virkni...
@app.route('/doregister', methods=['GET','POST'])
def doregister():
    allusernames = [] # gerum tóman lista sem á að geyma öll username
    u = db.child("user").get().val()
    lst = list(u.items())
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword']

        for i in range(len(lst)):
            allusernames.append(lst[i][1]['uname']) # Mokum öllum userum í listann

        
        # Ef user er til í database leyfum við ekki push í grunninn / ef user ekki til leyfum við push...
        if uname not in  allusernames:
            # user ekki til
            db.child("user").push({"uname":uname, "pword":pword}) 
            return "<h3>New user in database!!<h3> <a href='/'>Home</a>"
        else:
            # user er til
            return "<h3>Username exists in database, try again!!<h3> <a href='/'>Home</a>"
    else:
        return render_template("register.html")

# Route sem útfærir login virkni, ekkert annað en bara login virkni...
@app.route('/dologin', methods=['GET','POST'])
def dologin():
    # Hér þarftu að útfæra login virknina Ýmir!
    tf = False
    culo = False
    u = db.child("user").get().val()
    lst = list(u.items())
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword'] 
        
        print(tf)
        if tf == True:
            db.child("user").push({"uname":uname, "pword":pword})
        tf = False
        #check if uname and pword is correct to send to seacret.html
        for i in range(len(lst)):
            if uname == lst[i][1]['uname'] and pword == lst[i][1]['pword']:
                culo = True
        if culo == True:
            return render_template("seacret.html",uname = uname)
        else:
            return "<h3>Wrong username or password!!<h3> <a href='/'>Home</a>"
    else:
        return "<h1>Má ekki !</h1>"
    
    return "<h1>Login<h1>"

if __name__ == "__main__":
	app.run(debug=True)

# Test route til að sækja öll gögn úr db
#@app.route('/lesa')
#def lesa():
#    u = db.child("user").get().val()
#    lst = list(u.items())
#    print(lst[0][1]['uname'])
#    return "Lesum úr grunni"

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())