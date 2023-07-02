import requests
import re
import json
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)



ENDPOINT = "https://api.peruapis.com/v1"
API_DNI = "%s/dni?document=%s" % (ENDPOINT,"%s")
API_RUC = "%s/ruc?document=%s" % (ENDPOINT,"%s")
API_KYC_MATCH = "%s/kyc/match?document=%s" % (ENDPOINT,"%s")
API_EXCHANGE = "%s/exchange?document=%s" % (ENDPOINT,"%s")
API_SOAT = "%s/soat?document=%s" % (ENDPOINT,"%s") 
API_PLATE = "%s/plate-v2?document=%s" % (ENDPOINT,"%s")

patron_ruc = re.compile('[12]\d{10}$')
patron_dni = re.compile('\d{8}$')

class PeruApis(object):

    def __init__(self,ACCESS_KEY) -> None:
        self.ACCESS_KEY = ACCESS_KEY

    def get(self,api,value):
        try:
            headers = {"Authorization":"Bearer %s" % self.ACCESS_KEY}
            response = requests.get(api % value,headers=headers,data={})
            
            try:
                result = response.json()
            except Exception as e:
                result = {}
        except Exception as e:
            raise UserError(e)
        
        if result.get("success",False):
            result = result.get("data",{})

        return result
        
    def get_dni(self,value,force=False):
        if patron_dni.match(value):
            return self.get(API_DNI,value)
        raise ValidationError("El valor de DNI no cumple con su formato de 8 dígitos.")
        

    def get_ruc(self,value,force=False):
        if patron_ruc.match(value):
            return self.get(API_RUC,value)
        
        raise ValidationError("El valor de RUC no tiene un formato correcto.")
    
    def get_plate(self,value):
        return self.get(API_PLATE,value)
    
    def get_soat(self,value):
        return self.get(API_SOAT,value)
    
    def get_exchange(self,date):
        return self.get(API_SOAT,date)