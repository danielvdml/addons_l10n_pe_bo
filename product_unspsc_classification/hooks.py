 # coding: utf-8

from odoo import tools

def post_init_hook(env):
    csv_path = 'product_unspsc_classification/data/product_unspsc_code.csv'
    with tools.misc.file_open(csv_path, 'rb') as csv_file:
        csv_file.readline() 
        env.cr.copy_expert(
            """COPY product_unspsc_code (code, name, active)
               FROM STDIN WITH DELIMITER '|'""", csv_file)

    env.cr.execute(
        """INSERT INTO ir_model_data
           (name, res_id, module, model, noupdate)
           SELECT concat('unspsc_code_', code), id, 'product_unspsc_classification', 'product.unspsc.code', 't'
           FROM product_unspsc_code""")

def uninstall_hook(env):
    env.cr.execute("DELETE FROM product_unspsc_code;")
    env.cr.execute("DELETE FROM ir_model_data WHERE model='product_unspsc_code';")