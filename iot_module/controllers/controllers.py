# -*- coding: utf-8 -*-
# from odoo import http


# class TacticaPrototipo(http.Controller):
#     @http.route('/tactica_prototipo/tactica_prototipo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tactica_prototipo/tactica_prototipo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tactica_prototipo.listing', {
#             'root': '/tactica_prototipo/tactica_prototipo',
#             'objects': http.request.env['tactica_prototipo.tactica_prototipo'].search([]),
#         })

#     @http.route('/tactica_prototipo/tactica_prototipo/objects/<model("tactica_prototipo.tactica_prototipo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tactica_prototipo.object', {
#             'object': obj
#         })



from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class TacticaPrototipoController(http.Controller):
    @http.route('/iot/api', type='json', auth="public", methods=['POST'], csrf=False)
    def receive_data(self):
        try:
            # Obtener datos JSON directamente de la solicitud
            json_data = request.jsonrequest

            print("Veré Recibiendo datos desde Postman:", json_data)

            received_csn = json_data.get('csn')
            received_etapa = json_data.get('etapa')

            print(f"Veré CSN recibido: {received_csn}")
            print(f"Veré Etapa recibida: {received_etapa}")

            # Validación de datos
            if not received_csn or not received_etapa:
                raise UserError("Los campos 'csn' y 'etapa' son estrictamente obligatorios.")

            RFIDModel = request.env['rfid.data']
            new_rfid_data = RFIDModel.create({
                'csn': received_csn,
                'etapa': received_etapa,
            })

            print("Veré Registro creado exitosamente:", new_rfid_data)

            return {'status': 'OK', 'message': 'Data received Ok.'}
        except UserError as e:
            print(f"Veré Error de usuario: {e}")
            return {'status': 'Error', 'message': str(e)}
        except Exception as e:
            print(f"Veré Error inesperado: {e}")
            return {'status': 'Error', 'message': 'Se produjo un error inesperado.'}




    
    @http.route('/iot/sale', auth="public", csrf=False, website=True)
    def index(self, **kw):
        try:
            # Consulta todas las órdenes de venta
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
        
        # return http.request.render('odoo_controller.index', {
        #      "sales": sales_orders,
        #  })

    # @http.route('/contactos/<model("contact.template"):contact>', auth="public")
    # def contact_test(self, contact):
    #     return http.request.render('tactica_prototipo.contact', {
    #         "contact": contact
    #     })

    
    # @http.route('/tactica_prototipo/get_partners', type='json', auth="public", methods=['GET'])
    # def get_partners(self):
    #     # Recuperar los nombres de los registros de res.partner
    #     ContactModel = request.env['res.partner']
    #     partners = ContactModel.search([])

    #     # Extraer los nombres de los registros
    #     partner_names = partners.mapped('name')

    #     return {'partner_names': partner_names}
    

   