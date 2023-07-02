import requests
import re
import json
from odoo.exceptions import UserError, ValidationError

ENDPOINT = "https://api.peruapis.com/v1"
API_DNI = "%s/dni" % ENDPOINT
API_RUC = "%s/ruc" % ENDPOINT
API_KYC_MATCH = "%s/kyc/match" % ENDPOINT
API_EXCHANGE = "%s/exchange" % ENDPOINT
API_SOAT = "%s/soat" % ENDPOINT 
API_PLATE = "%s/plate-v2" % ENDPOINT

patron_ruc = re.compile('[12]\d{10}$')
patron_dni = re.compile('\d{8}$')

class ApisPeru(object):

    def __init__(self,ACCESS_KEY) -> None:
        self.ACCESS_KEY = ACCESS_KEY

    def get(self,api,value):
        try:
            params = {"document":value}
            response = requests.get(api,params)
        except Exception as e:
            raise UserError(e)
        result = response.json()
        if result.get("succcess",False):
            return result.get("data")
        else :
            return {}

    def get_dni(self,value,force=False):
        if patron_dni.match(value):
            return self.get("{api}&force={force}".format(api=API_DNI,force=force),value)
        raise ValidationError("El valor de DNI no cumple con su formato de 8 dígitos.")
        

    def get_ruc(self,value,force=False):
        if patron_ruc.match(value):
            return self.get("{api}&force={force}".format(api=API_RUC,force=force),value)
        
        raise ValidationError("El valor de RUC no tiene un formato correcto.")
    
    def get_plate(self,value):
        return self.get(API_PLATE,value)
    
    def get_soat(self,value):
        return self.get(API_SOAT,value)
    
    def get_exchange(self,date):
        return self.get(API_SOAT,date)