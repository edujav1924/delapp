# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import *
"""class PedidosAdmin(admin.ModelAdmin):
    list_display = ('pedido','cliente_pedido','cliente_nombre','cliente_apellido','cliente_celular', 'cliente_ubicacion','empresa_nombre','pedido_encargado')

admin.site.register(modelodespachopedido,PedidosAdmin)"""

class productosadmin(admin.ModelAdmin):
    list_display=('get_empresa','producto','precio')
    def get_empresa(self, productos):
        return productos.empresa.empresa
admin.site.register(modelo_producto,productosadmin)

class empresasadmin(admin.ModelAdmin):
    list_display=('empresa','latitud','longitud')
admin.site.register(modelo_empresa,empresasadmin)

class encargados_admin(admin.ModelAdmin):
    list_display=('nombre','empresas','telefono')
    def empresas(self, encargados):
        return encargados.empresa.empresa
admin.site.register(modelo_encargado,encargados_admin)

class pedidos_admin(admin.ModelAdmin):
    list_display = ('clientes','producto','cantidad')
    def clientes(self,pedidos):
        return pedidos.cliente.nombre
admin.site.register(modelo_pedido,pedidos_admin)

class clientes_admin(admin.ModelAdmin):
    list_display = ('nombre','apellido','celular','distancia','ubicacion','encargado','status','fecha','hora','token')
    
admin.site.register(modelo_cliente,clientes_admin)
