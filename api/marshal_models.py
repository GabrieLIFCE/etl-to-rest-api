from flask_restx import fields

cpe_fields= {}
cpe_fields['cpe_23_uri'] = fields.String(attribute='cpe_23_uri')
cpe_fields['vendor'] = fields.String(attribute='vendor')
cpe_fields['product'] = fields.String(attribute='product')
cpe_fields['vulnerable'] = fields.Boolean(attribute='vulnerable')

cvssv3_fields = {}
cvssv3_fields['version'] = fields.String(attribute='version')
cvssv3_fields['vector_string'] = fields.String(attribute='vector_string')
cvssv3_fields['attack_vector'] = fields.String(attribute='attack_vector')
cvssv3_fields['cvssv3_score'] = fields.Float(attribute=('cvssv3_score'))

cve_fields = {}
cve_fields['cve_id'] = fields.String(attribute='cve_id')
cve_fields['description'] = fields.String(attribute='description')
cve_fields['published_date'] = fields.DateTime(attribute='published_date')
cve_fields['last_modified'] = fields.DateTime(attribute='last_modified')

model_cve_controller = {}
model_cve_controller['cve_id'] = fields.String(attribute='cve_id')
model_cve_controller['description'] = fields.String(attribute='description')
model_cve_controller['published_date'] = fields.DateTime(attribute='published_date')
model_cve_controller['last_modified'] = fields.DateTime(attribute='last_modified')
model_cve_controller['cpes'] = fields.List(fields.Nested(cpe_fields))
model_cve_controller['cvssv3'] = fields.Nested(cvssv3_fields)

model_vendor_product_controller = {}
model_vendor_product_controller['cves'] = fields.List(fields.Nested(cve_fields))
