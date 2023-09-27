from odoo import models, fields, api
import logging
from ..utils.service import SMS
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class AWSSmsApi(models.AbstractModel):
    _inherit = 'sms.api'

    @api.model
    def _send_sms(self, numbers, content):
        SMS_PROVIDER = self.env["ir.config_parameter"].get_param("SMS_PROVIDER")
        if SMS_PROVIDER == "IAP":
            return super(AWSSmsApi, self)._send_sms(numbers, content)
        elif SMS_PROVIDER == "AWS_SNS":
            ARN = self.env["ir.config_parameter"].get_param("ARN","")
            ID_AWS = self.env["ir.config_parameter"].get_param("ID_AWS","")
            KEY_AWS = self.env["ir.config_parameter"].get_param("KEY_AWS","")
            REGION = self.env["ir.config_parameter"].get_param("REGION","")
            
            sms = SMS(id_aws=ID_AWS, 
                    key_aws=KEY_AWS, 
                    region=REGION)
            subs = sms.subscribe(arn=ARN, phone=numbers)
            if subs:
                p = sms.publish(phone=numbers, message=content)

                if(p['ResponseMetadata']['HTTPStatusCode'] == 200):
                    _logger.info("El mensaje ha sido enviado")
                else:
                    _logger.error("Mensaje no enviado")

            else: 
                _logger.error("El número no pudo suscribirse")

            return True
        
    @api.model
    def _send_sms_batch(self, messages):
        SMS_PROVIDER = self.env["ir.config_parameter"].get_param("SMS_PROVIDER")
        if SMS_PROVIDER == "IAP":
            return super(AWSSmsApi, self)._send_sms_batch(messages)
        elif SMS_PROVIDER == "AWS_SNS":
            ARN = self.env["ir.config_parameter"].get_param("ARN","")
            ID_AWS = self.env["ir.config_parameter"].get_param("ID_AWS","")
            KEY_AWS = self.env["ir.config_parameter"].get_param("KEY_AWS","")
            REGION = self.env["ir.config_parameter"].get_param("REGION","")
            
            for message in messages:
                numbers = message.get("number")
                content = message.get("content")
                sms = SMS(id_aws=ID_AWS, 
                    key_aws=KEY_AWS, 
                    region=REGION)
                subs = sms.subscribe(arn=ARN, phone=numbers)
                if subs:
                    p = sms.publish(phone=numbers, message=content)

                    if(p['ResponseMetadata']['HTTPStatusCode'] == 200):
                        _logger.info("El mensaje ha sido enviado")
                    else:
                        _logger.error("Mensaje no enviado")

                else: 
                    _logger.error("El número no pudo suscribirse")

            return [ {'res_id':message.get("res_id"),'state':'success','credit':0} for message in messages]
