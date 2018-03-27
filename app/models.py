# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class modelo_producto(models.Model):
    producto = models.CharField(max_length=30)
    precio = models.PositiveIntegerField()
    def __unicode__(self):
        return '%s %d' % (self.producto, self.precio)

class modelo_cliente(models.Model):
    cliente_id =models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,default='')
    apellido = models.CharField(max_length=30,blank=True,default='')
    celular = models.IntegerField(blank=True,null=True)
    ubicacion = models.CharField(max_length=100,blank=True,null=True)
    encargado = models.CharField(max_length=30,blank=True,null=True)
    status = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s %s %d %s' % (self.nombre, self.apellido,self.celular,self.ubicacion)

class modelo_pedido(models.Model):
    cliente = models.ForeignKey(modelo_cliente, related_name='pedidos', on_delete=models.CASCADE)
    producto = models.CharField(max_length=30, blank=True,null=True)
    cantidad = models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return '%s %s %d' % (self.cliente, self.producto, self.cantidad)

class modelo_encargado(models.Model):
    nombre = models.CharField(max_length=30)
    telefono = models.IntegerField(blank=True)
    def __str__(self):
             return '%s' % (self.nombre)


'''
class modelo_ (models.Model):
    pedido_tipo = models.CharField(max_length=10);
    pedido_cantidad = models.IntegerField()

class modelo_cliente(models.Model):
    cliente_nombre = models.CharField(max_length=30, blank=True, default='')
    cliente_ubicacion = models.CharField(max_length=30, blank=True, default='')
    cliente_status = models.BooleanField(default=False)
    def __str__(self):
        return '%s %s %s'% (self.cliente_nombre,self.cliente_ubicacion,self.cliente_status)

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
        return '%d %s %s' % (self.pedido_id,self.encargado,self.pedido_cliente)'''
