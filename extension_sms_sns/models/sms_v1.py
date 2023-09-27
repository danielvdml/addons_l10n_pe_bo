from odoo import models, fields, api
import logging
from ..utils.service import SMS

_logger = logging.getLogger("------ log de alex:")

class CustomSendSMS(models.TransientModel):
    _inherit = 'sms.composer'

    def action_send_sms(self):
        res = super(CustomSendSMS, self).action_send_sms()
        user = self.read()[0]['recipient_single_description']
        phone = self.read()[0]['recipient_single_number']
        message = self.read()[0]['body']
        params = {
            "user":user,
            "phone":phone,
            "message":message
        } 
        _logger.info(params)

        config_values = self.env['ir.config_parameter'].search([])
        paramaters = ['ARN','ID_AWS','KEY_AWS','REGION']

        credentials = {}
        for i in config_values:
            if i.key in paramaters:
                credentials[i.key] = i.value
        _logger.info(credentials)

        sms = SMS(id_aws=credentials['ID_AWS'], 
                    key_aws=credentials['KEY_AWS'], 
                    region=credentials['REGION'])
        subs = sms.subscribe(arn=credentials['ARN'], phone=phone)
        if subs:
            p = sms.publish(phone=phone, message=message)

            if(p['ResponseMetadata']['HTTPStatusCode'] == 200):
                _logger.info("El mensaje ha sido enviado")
            else:
                _logger.error("Mensaje no enviado")

        else: 
            _logger.error("El número no pudo suscribirse")

        return res