{
    "name":"Contactos Localización Perú",
    "summary":"""
* Establece un formulario de contacto con los elementos de departamento, provincia y distrito ordenados y dependientes.
* Establece una base para la integración de consulta RUC/DNI con apis externas.
    """,
    "author":"Daniel Moreno <daniel@bigodoo.com>",
    "depends":[
        "l10n_pe",
        "base_vat",
        "base_setup"
    ],
    "data":[
        "data/res_country_data.xml",
        "data/ir_config_parameter.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml"
    ]
}