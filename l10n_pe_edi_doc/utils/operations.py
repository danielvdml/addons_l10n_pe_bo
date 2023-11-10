def suma(a,b):
    return a + b

def division(a,b):
    return a/b

def multiplicacion(a,b):
    if str(a).isdigit() and str(b).isdigit():
        return a*b
    else:
        raise ValueError("Uno de los elemento del producto no es un numero")


#funcion que valida un número de ruc peruano
def validarucperuano(ruc):
    if len(ruc) == 11:
        if ruc.isdigit():
            return True
        else:
            return False
    else:
        return False
    
    