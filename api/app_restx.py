from flask import Flask, abort
from flask_restx import Resource, Api, fields, marshal
from flask_sqlalchemy import SQLAlchemy # ORM
import api.marshal_models as mm

import os

basedir = os.path.abspath(os.path.dirname(__file__)).replace('api', '')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'database.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

# Swagger
model_cve = api.model('cve', mm.cve_fields)
model_cpe = api.model('cpe', mm.cpe_fields)
model_cvssv3 = api.model('cvssv3', mm.cvssv3_fields)

fields_cve_response = {}
fields_cve_response['cve_id'] = fields.String(attribute='cve_id')
fields_cve_response['description'] = fields.String(attribute='description')
fields_cve_response['published_date'] = fields.DateTime(attribute='published_date')
fields_cve_response['last_modified'] = fields.DateTime(attribute='last_modified')
fields_cve_response['cpes'] = fields.List(fields.Nested(model_cpe))
fields_cve_response['cvssv3'] = fields.Nested(model_cvssv3)

# Swagger
model_vendor_product = api.model('/cve/{cve_id}', fields_cve_response)
fields_vendor_product_response = {}
fields_vendor_product_response['cves'] = fields.List(fields.Nested(model_cve))

# Swagger
model_cve = api.model('/cpe/{vendor}/{product}', fields_vendor_product_response)

class cve(db.Model):
    __tablename__='cve'
    def __init__(self):
        super().__init__()

    cve_id = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, unique=False)    
    published_date = db.Column(db.DateTime, unique=False)
    last_modified = db.Column(db.DateTime, unique=False)    
    cpes = db.relationship('cpe', back_populates='cve_d')


class cpe(db.Model):
    __tablename__='cpe'
    def __init__(self):
        super().__init__()

    id = db.Column(db.Integer, primary_key=True)    
    id_cve = db.Column('cve_id', db.String, db.ForeignKey('cve.cve_id'))
    vulnerable = db.Column('vulnerable', db.Boolean)
    cpe_23_uri = db.Column('cpe_23_uri', db.String)
    vendor = db.Column('vendor', db.String)
    product = db.Column('product', db.String)  
    cve_d = db.relationship("cve", back_populates="cpes")


class cvssv3(db.Model):
    __tablename__='cvssv3'
    def __init__(self):
        super().__init__()

    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column('cve_id', db.String, db.ForeignKey('cve.cve_id'))
    version = db.Column(db.String, unique=False)
    vector_string = db.Column(db.String, unique=False)
    attack_vector = db.Column(db.String, unique=False)
    cvssv3_score = db.Column(db.Float, unique=False)


@api.route('/api/cve/<string:cve_id>')
class CveController(Resource):
    @api.marshal_with(model_vendor_product)
    def get(self, cve_id):
        _cve = db.session.query(cve).filter(cve.cve_id == cve_id).first()
        if not bool(_cve): abort(404, 'Resource not found')
        _cvssv3 = db.session.query(cvssv3).filter(cvssv3.cve_id == cve_id).first()
        _cpes = db.session.query(cpe).filter(cpe.id_cve == cve_id).all()
        _data = {'cve_id':_cve.cve_id, 'description':_cve.description, 'published_date':_cve.published_date, 'last_modified':_cve.last_modified,
                'cvssv3':_cvssv3, 'cpes':_cpes}
        return marshal(_data, model_vendor_product)


@api.route('/api/cpe/<string:vendor>/<string:product>')
class VendorProductController(Resource):
    @api.marshal_with(model_cve)
    def get(self, vendor, product):
        _cpes = db.session.query(cpe).\
            filter(cpe.vendor == vendor).filter(cpe.product == product).all()
        if not bool(_cpes): abort(404, 'Resource not found')
        _cves = self.__get_cves(_cpes)
        _data = {'cves': _cves}
        return marshal(_data, model_cve)

    def __get_cves(self, cpes):
        cves = []
        for cpe in cpes:
            cves += db.session.query(cve).filter(cve.cve_id == cpe.id_cve).all()
        return cves
