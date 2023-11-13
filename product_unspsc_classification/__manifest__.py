{
    "name":"Clasificación de productos según UNSPSC",
    "depends":[
        "account"
    ],
    "data":[
        "security/ir_model_access.xml",
        "views/product_template.xml"
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
}