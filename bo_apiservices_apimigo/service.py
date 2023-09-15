import requests
import re
import json
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)



ENDPOINT = "https://api.migo.pe/api/v1"
API_RUC = "%s/ruc" % ENDPOINT
API_DNI = "%s/dni" % ENDPOINT
API_EXCHANGE_DATE = "%s/exchange/date" % ENDPOINT
API_RUC_ACTIVIDAD = "%s/ruc/actividad/%s" % (ENDPOINT,"%s")
API_CPE = "%s/cpe" % ENDPOINT
API_CDR = "%s/cdr" % ENDPOINT

class ApiMigo(object):

    def __init__(self,TOKEN) -> None:
        self.TOKEN = TOKEN

    def _post(self,api_url,args):
        headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }
        payload = {
            "token": self.TOKEN,
        }
        payload.update(args)
        headers = {"Authorization":"Bearer %s" % self.TOKEN}
        response = requests.post(api_url,json=payload,headers=headers)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        if not result.get("success",False):
                result = {}
        return result

    def post(self,api_url,args):
        try:
            return self._post(api_url,args)
        except Exception as e:
            raise UserError(e)
                

    def get_ruc(self,value):
        return self.post(API_RUC,{"ruc":value})
    

    def get_dni(self,value):
        return self.post(API_DNI,{"dni":value})
    
    def get_exchange_date(self,value):
        return self.post(API_EXCHANGE_DATE,{"fecha":value})
    
    def validaty_cpe(self,ruc_emisor,tipo_comprobante,serie,numero,fecha_emision,monto):
        return self.post(API_CPE,{
            "ruc_emisor":ruc_emisor,
            "tipo_comprobante":tipo_comprobante,
            "serie":serie,
            "numero":numero,
            "fecha_emision":fecha_emision,
            "monto":monto
        })
    
    def get_cdr(self,ruc_comprobante,tipo_comprobante,serie_comprobante,numero_comprobante):
        return self.post(API_CDR,{
            "ruc_comprobante":ruc_comprobante,
            "tipo_comprobante":tipo_comprobante,
            "serie_comprobante":serie_comprobante,
            "numero_comprobante":numero_comprobante
        })