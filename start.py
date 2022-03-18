import os
from flask import Flask, request, jsonify
from flasgger import Swagger,swag_from
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
swagger = Swagger(app)

# 12 Factor -> Stessa Codebase per sviluppo e produzione -> Supporta SQLITE e MYSQL -> Scelta dipende da var d'ambiente
db_type=os.getenv("DB_TYPE","SQLITE")
if db_type=="SQLITE":
    sqlite_db=os.getenv("SQLITE_PATH")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+sqlite_db
    print("utilizzo sqlite")
if db_type=="MYSQL":
    db_user=os.getenv("DB_USER")
    db_password=os.getenv("DB_PASSWORD")
    db_hostname=os.getenv("DB_HOSTNAME")
    db_name=os.getenv("DB_NAME")
    print("utilizzo mysql")
                                              #mysql://username:    password    @   server      /    db
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+db_user+":"+db_password+"@"+db_hostname+"/"+db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

class Cocktail_bar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(256), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)

#POST,GET,PUT,DELETE ---> CRUD(Create, Read, Update, Delete)
@app.route("/cocktail_bars",methods=["POST","GET"])
@swag_from('cocktail_bar_generic_get.yml',methods=['GET'])
@swag_from('cocktail_bar_generic_post.yml',methods=['POST'])
def cocktail_bar(): # /cocktails_bars/ POST, GET
    if request.method == "GET":
        cocktails=Cocktail_bar.query.all() #SELECT * FROM cocktail_bar
        message={"cocktails": []}
        for c in cocktails:
            message["cocktails"].append({"name":c.name,"id":c.id})
        return jsonify(message),200
    if request.method == "POST":
        cocktail_bar=Cocktail_bar(name="nuovo bar",address="via lazzaro palazzi",city="Milano")
        db.session.add(cocktail_bar)
        db.session.commit()
        return jsonify({"message":"creazione di un nuovo cocktail bar"}),201
    
@app.route("/cocktail_bars/<id>",methods=["PUT","GET","DELETE"])
def cocktail_bar_single(id): # /cocktails_bars/ POST, GET
    if id != None:
        if request.method == "GET":
            result=Cocktail_bar.query.filter_by(id=id) #select * from cocktail_bars where id==ID  
            if result is None:
                return jsonify({}),404
            else:
                return jsonify(result.to_dict())
                return jsonify({"name":result.name,"city":result.city,"address":result.address}),200
        if request.method == "PUT":
            return jsonify({"message":"aggiornamento di cocktail bar con id"+str(id)}),200
        if request.method == "DELETE":
            result=Cocktail_bar.query.filter_by(id=id).first() #select * from cocktail_bars where id==ID
            if result is None:
                return jsonify({}),404
            else:
                db.session.delete(result)
                db.session.commit()
                return jsonify({"name":result.name}),204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)

########
# cocktail bar 
# /cocktail_bars/
# /cocktail_bars/<id>
#  name,address,city
#
#
# cocktail
# /cocktail_bars/<id>/cocktails/
# /cocktail_bars/<id>/cocktails/<c_id>/
#
#
#/typo_risorsa/<id_risorsa_singola>/<typo_risorsa>/>id_risorsa_2>
#
#
