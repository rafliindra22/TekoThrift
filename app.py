from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import function
import sqlite3
from sqlite3 import Error
import os

basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "tekodb.sqlite")

# inisialisasi object flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database

# inisialisasi object flask restful
api = Api(app)

# inisialisasi object flask cors
CORS(app)

# inisialisasi object flask sqlalchemy
db = SQLAlchemy(app=app)

# buat field database
class ModelDb(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    namaProduk = db.Column(db.String)
    stockProduk = db.Column(db.Integer)
    jenisProduk = db.Column(db.String)
    hargaProduk = db.Column(db.Integer)
    sizeProduk = db.Column(db.String)
    statusProduk = db.Column(db.Boolean)
    imgProduk = db.Column(db.TEXT)
            
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
# create database
with app.app_context():
    db.create_all()

# inisialisasikan variable kosong bertipe dictionary untuk pembacaan JSON
isian = {}

class Produk(Resource):
    def get(self):
        getAllQuery = ModelDb.query.all()
        
        viewProduk = [
            {
                "id":produk.id,
                "nama produk":produk.namaProduk,
                "stock":produk.stockProduk,
                "jenis":produk.jenisProduk,
                "harga":produk.hargaProduk,
                "size":produk.sizeProduk,
                "status":produk.statusProduk,
                "image":produk.imgProduk

            }
            for produk in getAllQuery
        ]
        response = {
            "status":200,
            "message":"berhasil menampilkan semua produk",
            "produk":viewProduk
        }
        return response

    def post(self):
        # request form pengisian data
        dataNama = request.form["nama"]
        dataStock = request.form["stock"]
        dataJenis = request.form["jenis"]
        dataHarga = request.form["harga"]
        dataSize = request.form["size"]
        dataImage = request.form["image"]
        
        if int(dataStock) >= 1 :
            status = 1
        else:
            status=0

        # masukan data ke dalam database
        model = ModelDb(
            namaProduk = dataNama,
            stockProduk = dataStock,
            jenisProduk = dataJenis,
            hargaProduk = dataHarga,
            sizeProduk = dataSize,
            statusProduk = status,
            imgProduk = dataImage
        )
        model.save()

        response = {
            "status"    : 200,
            "message"   : "data berhasil di-input dan disimpan",
        }
        return response

    def delete(self):
        getAllQuery = ModelDb.query.all()
        # looping
        for tiapdata in getAllQuery:
            # panggil methode untuk delete semua data
            db.session.delete(tiapdata)
            db.session.commit()

        response = {
            "status"    : 200,
            "message"   : "data keseluruhan berhasil dihapus"
        }
        return response

class ProdukByID(Resource):
    def get(self, id):

        getByIDQuery = ModelDb.query.get(id)

        viewByID = {
            "id": getByIDQuery.id,
            "nama produk": getByIDQuery.namaProduk,
            "stock": getByIDQuery.stockProduk,
            "jenis": getByIDQuery.jenisProduk,
            "harga": getByIDQuery.hargaProduk,
            "size": getByIDQuery.sizeProduk,
            "status": getByIDQuery.statusProduk,
            "image": getByIDQuery.imgProduk
        }

        response = {
            "status"    : 200,
            "message"   : "data dengan id: "+id+", berhasil ditampilkan",
            "produk"    : viewByID    
        }
        return response

    def delete(self, id):
        queryDelete = ModelDb.query.get(id)

        # panggil methode  untuk delete data by id
        db.session.delete(queryDelete)
        db.session.commit()

        response = {
            "status"    : 200,
            "message"   : "data dengan id: "+id+", berhasil dihapus"
        }
        return response


    def put(self, id):
        query = ModelDb.query.get(id)

        editNama = request.form["nama"]
        editStock = request.form["stock"]
        if int(editStock) >= 1:
            status = 1
        else:
            status = 0

        editJenis = request.form["jenis"]
        editHarga = request.form["harga"]
        editSize = request.form["size"]


        
        # replace nilai yang ada
        query.stockProduk = editStock
        query.statusProduk = status
        query.jenisProduk = editJenis
        query.shargaProduk = editHarga
        query.sizeProduk = editSize

        db.session.commit()

        response = {
            "status"    : 200,
            "message"   : "data berhasil diubah"
        }

        return response

class JumlahProduk(Resource):
    def get(self):
        jumQuery = ModelDb.query.all()
        
        


        viewProduk = [
            {
                "stock":produk.stockProduk
            }
            for produk in jumQuery  
        ]
        total=0
        for produk in jumQuery:
            
            total = total + produk.stockProduk
        #jumlahStock = produk + produk

        response = {
            "status" : 200,
            "message": "jumlah produk adalah : ",
            "jumlah stock": total
        }
        return response
            
        

api.add_resource(Produk, "/produk", methods = ["GET", "POST", "DELETE"])
api.add_resource(ProdukByID, "/produk/<id>", methods = ["GET","PUT","DELETE"])
api.add_resource(JumlahProduk, "/produk/jumlah", methods = ["GET"])

if __name__ == "__main__":
    app.run(debug=True, port=8888)