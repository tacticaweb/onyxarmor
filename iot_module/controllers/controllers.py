import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import json

_logger = logging.getLogger(__name__)

class TacticaPrototipoController(http.Controller):
    @http.route('/iot/api', type='json', auth="public", methods=['POST'], csrf=False)
    def receive_data(self, **kwargs):
        try:
            # Obtener datos JSON directamente de la solicitud
            json_data = request.jsonrequest

            if isinstance(json_data, str):
                # Si json_data es una cadena, intenta cargarla como JSON
                json_data = json.loads(json_data)


            # Validar si los datos son una lista o un solo elemento
            if isinstance(json_data, (list, dict)):
                # Si se recibe una lista de elementos JSON o un solo elemento JSON
                return self.process_data_list(json_data)

            raise UserError("Formato de datos no válido.")

        except UserError as e:
            _logger.error("Error de usuario: %s", e)
            return {'status': 'Error', 'message': str(e)}, 400  # Bad Request
        except Exception as e:
            _logger.exception("Error inesperado: %s", e)
            return {'status': 'Error', 'message': 'Se produjo un error inesperado.'}, 500  # Internal Server Error

    def process_data_list(self, json_data_list):
        RFIDModel = request.env['rfid.data']

        # Verifica si json_data_list es un diccionario y si contiene la clave 'json_data_list'
        if isinstance(json_data_list, dict) and 'json_data_list' in json_data_list:
            json_data_list = json_data_list['json_data_list']  # Obtén la lista de elementos

            # Asegúrate de que json_data_list sea realmente una lista
            if isinstance(json_data_list, list):
                # Itera sobre los elementos de la lista
                for index, data in enumerate(json_data_list):
                    _logger.info("Processing item at index %s: %s", index, data)

                    # Verifica si el elemento es un diccionario
                    if isinstance(data, dict):
                        received_csn = data.get('csn')
                        received_etapa = data.get('etapa')

                        _logger.info("CSN received: %s", received_csn)
                        _logger.info("Received stage: %s", received_etapa)

                        # Validación de datos
                        _logger.info("Validating data for item at index %s", index)
                        if not received_csn or not received_etapa:
                            raise UserError("Fields 'csn' and 'etapa' are mandatory.")
                        _logger.info("Data validation successful for item at index %s", index)

                        # Validar que la clave CSN sea única
                        existing_rfid_data = RFIDModel.search([('csn', '=', received_csn)], limit=1)
                        _logger.info("Search results: %s", existing_rfid_data)

                        if existing_rfid_data:
                            # If the CSN already exists, update the existing record
                            existing_rfid_data.write({
                                'etapa': received_etapa,
                            })
                            _logger.info("Record updated successfully: %s", existing_rfid_data)
                        else:
                            # If the CSN doesn't exist, create a new record
                            new_rfid_data = RFIDModel.create({
                                'csn': received_csn,
                                'etapa': received_etapa,
                            })

                            _logger.info("Record created successfully: %s", new_rfid_data)

                    else:
                        raise UserError("Invalid data format. Expected a list of items (dictionaries).")

                _logger.info("End of loop for json_data_list.")
                return {'status': 'OK', 'message': 'Data received successfully.'}
            else:
                raise UserError("Invalid data format. Expected a list of items.")
        else:
            raise UserError("Invalid data format. 'json_data_list' key not found.")



#############################


    
    @http.route('/iot/sale', auth="public", csrf=False, website=True)
    def index(self, **kw):
        try:
            # Consulta todas las órdenes de venta
            _logger.info("Ingresando al endpoint /iot/sale")
            sales_orders = http.request.env['sale.order'].search([])

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir
            return "<h1>No se puede acceder al API</h1>"

        output = "<h1>Órdenes de Venta</h1><ul>"

        for sale in sales_orders:
            # Itera sobre las órdenes de venta y agrega sus nombres a la salida
            output += '<li>' + sale.name + '</li>'

        output += "</ul>"
        return output

    @http.route('/iot/contacts', auth="public", csrf=False, website=True)
    def show_contacts(self, **kw):
        try:
            # Consulta todos los contactos
            _logger.info("Ingresando al endpoint /iot/contacts")
            contacts = http.request.env['res.partner'].search([])

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir
            return "<h1>No se pueden recuperar los contactos</h1>"

        contact_output = "<h1>Contactos</h1><ul>"

        for contact in contacts:
            # Itera sobre los contactos y agrega sus nombres a la salida
            contact_output += '<li>' + contact.name + '</li>'

        contact_output += "</ul>"
        return contact_output
        
       

   