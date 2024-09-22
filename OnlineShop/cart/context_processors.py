# Packages
from .cart import Cart

# Context

def cart(request:str) -> dict:
    return {'cart': Cart(request)}