# -*- coding: utf-8 -*-

import logging
import werkzeug
import math

from collections import namedtuple, OrderedDict, defaultdict
from odoo import api, fields, models, SUPERUSER_ID,_
from odoo import http, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.addons.stock.models.stock_rule import ProcurementException
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round, float_is_zero
import datetime
import pytz

import logging
_logger = logging.getLogger(__name__)

class ResSizing(models.Model):
    _inherit = 'res.sizing'
    
    state = fields.Selection([
            ('draft', 'Draft'),
            ('pending', 'Pending Authorization'),
            ('valid', 'Validated'),
        ],
        string='State', required=True,
        default='draft')
    
    
    size_front = fields.Selection([
            ('XS', 'XS'),
            ('SM', 'SM'),
            ('MD', 'MD'),
            ('LG', 'LG'),
            ('XL', 'XL'),
            ('2XL', '2XL'),
            ('3XL', '3XL'),
            ('4XL', '4XL'),
            ('5XL', '5XL'),
            ('6XL', '6XL'),
        ],
        string='Front Size', required=True,
        default='MD')
    
    size_front_length = fields.Selection([
            ('-5 inch', '-5 inch'),
            ('-4 inch', '-4 inch'),
            ('-3 inch', '-3 inch'),
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),
            ],
        string='Front Length', required=True,
        default='0 inch')
    size_width = fields.Selection([
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),            ],
        string='Size Width', required=True,
        default='0 inch')
    size_back = fields.Selection([
            ('XS', 'XS'),
            ('SM', 'SM'),
            ('MD', 'MD'),
            ('LG', 'LG'),
            ('XL', 'XL'),
            ('2XL', '2XL'),
            ('3XL', '3XL'),
            ('4XL', '4XL'),
            ('5XL', '5XL'),
            ('6XL', '6XL'),
        ],
        string='Back Size', required=True,
        default='MD')
    size_back_length = fields.Selection([
            ('-5 inch', '-5 inch'),
            ('-4 inch', '-4 inch'),
            ('-3 inch', '-3 inch'),
            ('-2 inch', '-2 inch'),
            ('-1 inch', '-1 inch'),
            ('0 inch', '0 inch'),
            ('+1 inch', '+1 inch'),
            ('+2 inch', '+2 inch'),
            ('+3 inch', '+3 inch'),
            ('+4 inch', '+4 inch'),
            ('+5 inch', '+5 inch'),
            ('+6 inch', '+6 inch'),
            ],
        string='Back Length', required=True,
        default='0 inch')
            
    def compute_size(self):
        for sizing in self:
            sizing.state = "valid"
            d = float(sizing.abdomen_measure) + (float(sizing.inf_overlap) * 2)
            d = d / 2
            print ("D: ", d)
            if d < 14.92 or sizing.length_front_measure == 0 or sizing.length_back_measure == 0:
                print ("Do Nothing")
            else:
                if d >= 14.92 and d <= 15.94:
                    print ("size_front XS")
                    sizing.size_front = 'XS'
                    sizing.size_back = 'XS'
                elif d > 15.94 and d <= 17.97:
                    print ("size_front SM")
                    sizing.size_front = 'SM'
                    if d == 15.94:
                        sizing.size_back = 'XS'
                    else:
                        sizing.size_back = 'SM'
                elif d > 17.97 and d <= 19.99:
                    print ("size_front MD")
                    sizing.size_front = 'MD'
                    if d == 17.97:
                        sizing.size_back = 'SM'
                    else:
                        sizing.size_back = 'MD'
                elif d > 19.99 and d <= 22.01:
                    print ("size_front LG")
                    sizing.size_front = 'LG'
                    if d == 19.99:
                        sizing.size_back = 'MD'
                    else:
                        sizing.size_back = 'LG'
                elif d > 22.01 and d <= 24.04:
                    print ("size_front XL")
                    sizing.size_front = 'XL'
                    if d == 22.01:
                        sizing.size_back = 'LG'
                    else:
                        sizing.size_back = 'XL'
                elif d > 24.04 and d <= 26.07:
                    print ("size_front 2XL")
                    sizing.size_front = '2XL'
                    if d == 24.04:
                        sizing.size_back = 'XL'
                    else:
                        sizing.size_back = '2XL'
                elif d > 26.07 and d <= 28.14:
                    print ("size_front 3XL")
                    sizing.size_front = '3XL'
                    if d == 26.07:
                        sizing.size_back = '2XL'
                    else:
                        sizing.size_back = '3XL'
                elif d > 28.14 and d <= 30.18:
                    print ("size_front 4XL")
                    sizing.size_front = '4XL'
                    if d == 28.14:
                        sizing.size_back = '3XL'
                    else:
                        sizing.size_back = '4XL'
                elif d > 30.18 and d <= 32.22:
                    print ("size_front 5XL")
                    sizing.size_front = '5XL'
                    if d == 30.18:
                        sizing.size_back = '4XL'
                    else:
                        sizing.size_back = '5XL'
                elif d > 32.22 and d <= 33.24:
                    print ("size_front 6XL")
                    sizing.size_front = '6XL'
                    if d == 32.22:
                        sizing.size_back = '5XL'
                    else:
                        sizing.size_back = '6XL'
        
                if sizing.size_front == 'XS':
                    print ("size_front XS")
                    fl = sizing.length_front_measure - 11.75
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl)))
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl)))  
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_front == 'SM':
                    print ("size_front SM")
                    fl = sizing.length_front_measure - 12.00
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_front == 'MD':
                    print ("size_front MD")
                    fl = sizing.length_front_measure - 12.25
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_front == 'LG':
                    print ("size_front LG")
                    fl = sizing.length_front_measure - 12.50
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_front == 'XL':
                    print ("size_front XL")
                    fl = sizing.length_front_measure - 12.75
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl)))
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl)))  
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_front == '2XL':
                    print ("size_front 2XL")
                    fl = sizing.length_front_measure - 13.00
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_front == '3XL':
                    print ("size_front 3XL")
                    fl = sizing.length_front_measure - 13.25
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_front == '4XL':
                    print ("size_front 4XL")
                    fl = sizing.length_front_measure - 13.50
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_front == '5XL':
                    print ("size_front 5XL")
                    fl = sizing.length_front_measure - 13.75
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl)))
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl)))  
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_front == '6XL':
                    print ("size_front 6XL")
                    fl = sizing.length_front_measure - 14.00
                    frac, whole = math.modf(fl)
                    if frac >= 0.75:
                        fl = whole + 1
                    else:
                        fl = whole  
                    if fl > 0:
                        sizing.size_front_length = "+%s inch" %(int(abs(fl))) 
                    elif fl == 0:
                        sizing.size_front_length = "%s inch" %(int(abs(fl))) 
                    else:
                        sizing.size_front_length = "-%s inch" %(int(abs(fl)))
                    if  fl >= 4 or fl <= -2:
                        sizing.state = "pending"
                    
                if sizing.size_back == 'XS':
                    bl = sizing.length_back_measure - 14.36
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_back == 'SM':
                    bl = sizing.length_back_measure - 14.61
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl)))  
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl)))
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_back == 'MD':
                    bl = sizing.length_back_measure - 14.86
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == 'LG':
                    bl = sizing.length_back_measure - 15.11
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == 'XL':
                    bl = sizing.length_back_measure - 15.36
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                
                elif sizing.size_back == '2XL':
                    bl = sizing.length_back_measure - 15.61
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl)))  
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl)))
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == '3XL':
                    bl = sizing.length_back_measure - 15.86
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == '4XL':
                    bl = sizing.length_back_measure - 16.11
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == '5XL':
                    bl = sizing.length_back_measure - 16.36
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl)))  
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl)))
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"
                        
                elif sizing.size_back == '6XL':
                    bl = sizing.length_back_measure - 16.61
                    frac, whole = math.modf(bl)
                    if frac >= 0.75:
                        bl = whole + 1
                    else:
                        bl = whole  
                    if bl > 0:
                        sizing.size_back_length = "+%s inch" %(int(abs(bl))) 
                    elif bl == 0:
                        sizing.size_back_length = "%s inch" %(int(abs(bl))) 
                    else:
                        sizing.size_back_length = "-%s inch" %(int(abs(bl)))
                    if  bl >= 4 or bl <= -2:
                        sizing.state = "pending"    
                    
            
                