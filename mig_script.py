#!/usr/bin/env python2
import xmlrpclib

class odoo_import:

    url1 = "https://odoo.com"
    db1 = "odoo1"
    username1 = "admin"
    password1 = "admin"
    common1 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url1))
    models1  = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url1))
    uid1 = common1.authenticate(db1,username1, password1, {})

    url2 = "https://odoo_importoo.com"
    db2 = "odoo2"
    username2 = "admin"
    password2 = "admin"
    common2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url2))
    models2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url2))
    uid2 = common2.authenticate(db2, username2, password2, {})
    
    def __init__(self):
        #definitions for first database/server
        self.url1 = "https://odoo.com"
        self.db1 = "odoo1"
        self.username1 = "admin"
        self.password1 = "admin"
        self.common1 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url1))
        self.models1 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url1))
        self.uid1 = self.common1.authenticate(self.db1, self.username1, self.password1, {})

        #definitions for second database/server
        self.url2 = "https://odoo.com"
        self.db2 = "odoo2"
        self.username2 = "admin"
        self.password2 = "admin"
        self.common2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(self.url2))
        self.models2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url2))
        self.uid2 = self.common2.authenticate(self.db2, self.username2, self.password2, {})

    def import_res_partner(self):
        args = [[]]
        query = self.models1.execute_kw(
                self.db1, self.uid1, self.password1, 'res.partner', 'search', args)
        res_partner = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'res.partner', 'read', [query], 
                                            {'fields': []})
        
        for record in res_partner:
            if record['country_id']:
                record.update({'country_id': record['country_id'][0]})
            if record['state_id']:
                record.update({'state_id': record['state_id'][0]})
            print record
            #migrated_contact = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'res.partner', 'create', [record])

    def remove_duplicate(self):
        #remove dubplicate categories
        #remove duplicate attributes
        #remove duplicate attribute values
        #Remove duplicate products
        #remove duplicate contacts
        pass

    def product_product_import(self):
        #import Product.product
        args = [[]]
        query = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.template', 'search', args)
        for item in query:
            self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.template', 'create_variant_ids', [int(item)])

    def product_template_import(self):
        #import Product.template
        args = [[]]
        prod_id=None
        query = self.models1.execute_kw(
            self.db1, self.uid1, self.password1, 'product.template', 'search', args)
        
        product_template = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.template', 'read', [
                                            query], {'fields': ['name','sale_ok','purchase_ok','type','uom_id','uom_po_id','standard_price','attribute_line_ids',
                                            'list_price','image_medium','categ_id','description','description_sale','route_ids','default_code',
                                            'description_purchase','produce_delay','sale_delay','description_pickingout','tracking','description_pickingin','description_picking']})       
        
        for item in product_template:
            product_categories = self.models2.execute_kw(self.db2, self.uid2, self.password2,
                                'product.category', 'search',
                                [[['name', '=', item['categ_id'][1].split("/ ")[-1]]]])
            prod_id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.template', 'create', [
                            {
                            'type':item['type'],
                            'default_code':item['default_code'],
                            'route_ids':item['route_ids'],
                            'name':item['name'],
                            'image_medium':item['image_medium'],
                            'uom_id':item['uom_id'][0],
                            'uom_po_id':item['uom_po_id'][0],
                            'categ_id':product_categories[0],
                            'sale_ok':item['sale_ok'],
                            'purchase_ok':item['purchase_ok'],
                            'standard_price':item['standard_price'],
                            'list_price':item['list_price'],
                            'engineering_code':item['engineering_code'],
                            'description':item['description'],
                            'description_sale':item['description_sale'],
                            'description_purchase':item['description_purchase'],
                            'produce_delay':item['produce_delay'],
                            'sale_delay':item['sale_delay'],
                            'description_pickingout':item['description_pickingout'],
                            'tracking':item['tracking'],
                            'description_pickingin':item['description_pickingin'],
                            'description_picking':item['description_picking']
                            }])
            product_attrib_line = self.models1.execute_kw(self.db1, self.uid1, self.password1,'product.attribute.line', 'search_read'
                ,[[['product_tmpl_id', '=', item['id']]]],{'fields': ['display_name','attribute_id','value_ids','product_tmpl_id']})
            for item in product_attrib_line:
                list_attrib_values = []
                name_attrib = None
                product_attrib_values_names = self.models1.execute_kw(self.db1, self.uid1, self.password1,'product.attribute.value', 'search_read',
                    [[['id', 'in', item['value_ids']]]],{'fields': []})
                for items in product_attrib_values_names:
                    product_attrib_values = self.models2.execute_kw(self.db2, self.uid2, self.password2,'product.attribute.value', 'search_read',
                        [[['name', '=', items['name']]]],{'fields': []})
                    for a in product_attrib_values:
                        if a['attribute_id'][1]==items['attribute_id'][1]:
                            name_attrib = a['attribute_id'][0]
                            list_attrib_values.append(a['id'])
                id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute.line', 'create', [
                            {'attribute_id':name_attrib,'product_tmpl_id': prod_id}])
                self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute.line', 'write', [[id], {'value_ids':[(6,0,list_attrib_values)]}])
        
    
    def attribute(self):
        #import attribute
        args = [[]]
        query = self.models1.execute_kw(
            self.db1, self.uid1, self.password1, 'product.attribute', 'search', args)
        product_attrib = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.attribute', 'read', [
                                            query], {'fields': ['name','create_variant']})
        for item in product_attrib:
            id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute', 'create', [
                            {'create_variant':item['create_variant'], 'name':item['name']}])
    
    def attrib_values(self):
        #import attribute values
        args = [[]]
        query = self.models1.execute_kw(
            self.db1, self.uid1, self.password1, 'product.attribute.value', 'search', args)
        product_attrib_values = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.attribute.value', 'read', [
                                            query], {'fields': ['name','attribute_id','price_extra']})
        for item in product_attrib_values:
            parent = self.models2.execute_kw(self.db2, self.uid2, self.password2,
                                'product.attribute', 'search',
                                [[['name', '=',item['attribute_id'][1]]]])
            try:
                id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute.value', 'create', [
                            {'attribute_id': parent[0], 'name':item['name'],'price_extra':item['price_extra']}])
            except:
                pass

    def import_categories(self):
        #Importing Categories
        args = [[]]
        query = self.models1.execute_kw(
            self.db1, self.uid1, self.password1, 'product.category', 'search', args)
        product_categories = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.category', 'read', [
                                            query], {'fields': ['name','parent_id','removal_strategy_id','property_cost_method']})
        for category in product_categories:
            if category["name"] in ["Saleable","All"]:
                continue
            else:
                if category['removal_strategy_id'] == False:
                    if category["parent_id"] == False:
                        id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.category', 'create', [
                            {'name': category['name'], 'property_cost_method':category['property_cost_method']}])
                    else:
                        parent = self.models2.execute_kw(self.db2, self.uid2, self.password2,
                                'product.category', 'search',
                                [[['name', '=', category["parent_id"][1].split("/ ")[-1]]]])

                        id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.category', 'create', [
                            {'name': category['name'],'parent_id':parent[0],'property_cost_method':category['property_cost_method']}])
                else:
                    if category["parent_id"] == False:
                        id =  self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.category', 'create', [
                            {'name': category['name'], 'removal_strategy_id':category['removal_strategy_id'][0], 'property_cost_method':category['property_cost_method']}])
                    else:
                        parent = self.models2.execute_kw(self.db2, self.uid2, self.password2,
                                'product.category', 'search',
                                [[['name', '=', category["parent_id"][1].split("/ ")[-1]]]])
                        id = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.category', 'create', [
                            {'name': category['name'],'parent_id':parent[0] , 'removal_strategy_id':category['removal_strategy_id'][0], 'property_cost_method':category['property_cost_method']}])

    def import_vendor_pricelist(self):
        args = [[]]
        query = self.models1.execute_kw(
                self.db1, self.uid1, self.password1, 'product.supplierinfo', 'search', args)
        product_supplierinfo = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.supplierinfo', 'read', [query],
                                                {'fields': ['product_name', 'delay', 'product_code',
                                                    'min_qty', 'price', 'date_start', 'date_end',
                                                    'product_id', 'product_tmpl_id', 'name',
                                                    ]})
        for record in product_supplierinfo:
            #Search product in source database
            if record['product_id']:
                product_id = [[['id', '=', record['product_id'][0]]]]
                query = self.models1.execute_kw(
                    self.db1, self.uid1, self.password1, 'product.product', 'search', product_id)
                values = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.product', 'read', [query],
                                                        {'fields': ['attribute_value_ids',]})
                attrs_values = []
                attrs_names = []
                if values[0]['attribute_value_ids']:
                    for id in values[0]['attribute_value_ids']:
                        vals = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.attribute.value', 'read', [id],
                                                                {'fields': ['name','attribute_id']})
                        attrs_values.append(vals[0].get('name'))
                        attribute_id = vals[0].get('attribute_id')[0]
                        attr = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.attribute', 'read', [attribute_id],
                                                                {'fields': ['name']})
                        attrs_names.append(attr[0].get('name'))

                    #############################################################
                    #                                                           #
                    #   Search product in destination database with same name   #
                    #                                                           #
                    #############################################################

                    product_tmpl_id = record['product_tmpl_id'][0]
                    product_name = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.template', 'read', [product_tmpl_id],
                                                            {'fields': ['name', 'default_code']})
                    formatted_product_name = product_name[0].get('name')
                    product_default_code = product_name[0].get('default_code')
                    product_name_match = [['&', ['name', '=', formatted_product_name], ['default_code', '=', product_default_code]]]
                    product_name_match = [[['name', '=', formatted_product_name]]]
                    query1 = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'product.template', 'search', product_name_match)
                    srch_product_attrs = [['&', ['name', 'in', attrs_values], ['attribute_id', 'in', attrs_names]]]
                    attr_val_query = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'product.attribute.value', 'search', srch_product_attrs)
                    #########################################################################
                    #                                                                       #
                    #   Search product attibutes in destination database with same name     #
                    #                                                                       #
                    #########################################################################
                    srch_product = [['&', ['product_tmpl_id', 'in', query1], ['attribute_value_ids', 'in', attr_val_query]]]
                    query2 = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'product.product', 'search', srch_product)
                    attr_vals = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.product', 'read', [query2],
                                                            {'fields': ['attribute_value_ids',]})
                    attr_id = False
                    for product in attr_vals:
                        attribute_names = []
                        attribute_values = []
                        for id in product['attribute_value_ids']:
                            vals = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute.value', 'read', [id],
                                                                    {'fields': ['name','attribute_id']})
                            attribute_values.append(vals[0].get('name'))
                            attribute_id = vals[0].get('attribute_id')[0]
                            attr = self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.attribute', 'read', [attribute_id],
                                                                    {'fields': ['name']})
                            attribute_names.append(attr[0].get('name'))
                        if (set(attribute_values) == set(attrs_values)) and (set(attribute_names) == set(attrs_names)):
                            attr_id = product.get('id')
                    dict = {}
                    for key in record.keys():
                        dict.update({key : record.get(key)})
                    if dict['product_id']:
                        dict.update({'product_id': attr_id})
                    if dict['product_tmpl_id']:
                        dict.update({'product_tmpl_id': query1[0]})


                    srch_contact = [[['name', '=', dict['name'][1]], ['supplier', '=', True]]]
                    query3 = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'res.partner', 'search', srch_contact)
                    if dict['name']:
                        dict.update({'name': query3[0]})
                else:
                    dict = {}
                    for key in record.keys():
                        dict.update({key : record.get(key)})
                    product_tmpl_id = record['product_tmpl_id'][0]
                    product_name = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.template', 'read', [product_tmpl_id],
                                                            {'fields': ['name', 'default_code']})
                    formatted_product_name = product_name[0].get('name')
                    product_default_code = product_name[0].get('default_code')
                    product_name_match = [['&', ['name', '=', formatted_product_name], ['default_code', '=', product_default_code]]]
                    product_name_match = [[['name', '=', formatted_product_name]]]
                    query1 = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'product.template', 'search', product_name_match)
                    product_name_match = [['&', ['name', '=', formatted_product_name], ['product_tmpl_id', '=', query1]]]
                    attr_id = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'product.product', 'search', product_name_match)
                    if dict['product_id']:
                        dict.update({'product_id': attr_id[0]})
                    if dict['product_tmpl_id']:
                        dict.update({'product_tmpl_id': query1[0]})
                    srch_contact = [[['name', '=', dict['name'][1]], ['supplier', '=', True]]]
                    query3 = self.models2.execute_kw(
                        self.db2, self.uid2, self.password2, 'res.partner', 'search', srch_contact)
                    if dict['name']:
                        dict.update({'name': query3[0]})
            else:
                dict = {}
                for key in record.keys():
                    dict.update({key : record.get(key)})
                product_tmpl_id = record['product_tmpl_id'][0]
                product_name = self.models1.execute_kw(self.db1, self.uid1, self.password1, 'product.template', 'read', [product_tmpl_id],
                                                        {'fields': ['name', 'default_code']})
                formatted_product_name = product_name[0].get('name')
                product_name_match = [[['name', '=', formatted_product_name]]]
                query1 = self.models2.execute_kw(
                    self.db2, self.uid2, self.password2, 'product.template', 'search', product_name_match)
                if dict['product_tmpl_id']:
                    dict.update({'product_tmpl_id': query1[0]})
                srch_contact = [[['name', '=', dict['name'][1]], ['supplier', '=', True]]]
                query3 = self.models2.execute_kw(
                    self.db2, self.uid2, self.password2, 'res.partner', 'search', srch_contact)
                if dict['name']:
                    dict.update({'name': query3[0]})
            self.models2.execute_kw(self.db2, self.uid2, self.password2, 'product.supplierinfo', 'create', [dict])

if __name__ == "__main__":
    a=odoo_import()
    a.import_res_partner()
    a.import_categories()
    a.attribute()
    a.attrib_values()
    a.product_template_import()
    a.product_product_import()
    a.import_vendor_pricelist()
