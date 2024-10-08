from app import db

class Pagos(db.Model):
    __tablename__ = "pagos"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer)
    precio = db.Column(db.Float)
    medio_pago = db.Column(db.String(50))
    fecha_pago = db.Column(db.DateTime)

    @staticmethod
    def crear_pago(producto_id, precio, medio_pago):
        nuevo_pago = Pagos(producto_id=producto_id, precio=precio, medio_pago=medio_pago)
        db.session.add(nuevo_pago)
        db.session.commit()
        return nuevo_pago

    @staticmethod
    def obtener_pagos():
        return Pagos.query.all()

    @staticmethod
    def obtener_pago_por_id(pago_id):
        return Pagos.query.get(pago_id)
