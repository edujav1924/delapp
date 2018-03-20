# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
class modeloencargado(models.Model):
    nombre = models.CharField(max_length=30)
    telefono = models.IntegerField()
    def __str__(self):
             return '%s' % (self.nombre)

class modelocliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    cliente_pedido = models.CharField(max_length=30, blank=True, default='')
    cliente_nombre = models.CharField(max_length=30, blank=True, default='')
    cliente_ubicacion = models.CharField(max_length=30, blank=True, default='')
    cliente_status = models.BooleanField(default=False)
    def __str__(self):
        return '%s %s %s'% (self.cliente_pedido,self.cliente_nombre,self.cliente_ubicacion)

class modeloempresa(models.Model):
    empresa_nombre = models.CharField(max_length=30, blank=True, default='')
    def __str__(self):
        return '%s' % (self.empresa_nombre)

class modelodespachopedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    encargado = models.CharField(max_length=30,blank=True)
    pedido_cliente = models.CharField(max_length=30,blank=True)
    pedido_cliente_nombre = models.CharField(max_length=30,blank=True)
    def __str__(self):
        return '%d %s %s' % (self.pedido_id,self.encargado,self.pedido_cliente)
