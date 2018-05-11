# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from fcm_django.models import FCMDevice

class modelo_empresa(models.Model):
    empresa = models.CharField(max_length=30)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s %s %s' % (self.empresa, self.latitud, self.longitud)
class modelo_producto(models.Model):
    empresa = models.ForeignKey(modelo_empresa,related_name='productos',on_delete=models.CASCADE)
    producto = models.CharField(max_length=30)
    precio = models.PositiveIntegerField()
    def __unicode__(self):
        return '%s %s %d' % (self.empresa, self.producto, self.precio)

class modelo_cliente(models.Model):
    cliente_id =models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,default='')
    apellido = models.CharField(max_length=30,blank=True,default='')
    celular = models.IntegerField(blank=True,null=True)
    distancia = models.CharField(max_length=10,blank=True,null=True)
    empresa = models.CharField(max_length=30,blank=True,null=True)
    ubicacion = models.CharField(max_length=100,blank=True,null=True)
    encargado = models.CharField(max_length=30,blank=True,null=True)
    status = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True, blank=True)
    hora = models.TimeField(auto_now_add=True)
    token=models.CharField(max_length=200)
    fecha_aceptado = models.DateField(blank=True,null=True)
    hora_aceptado = models.TimeField(blank=True,null=True)
    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.nombre, self.apellido,self.celular,self.distancia,self.empresa,self.ubicacion,self.encargado,self.status,self.fecha,self.hora,self.fecha_aceptado,self.hora_aceptado,self.token)



class modelo_pedido(models.Model):
    cliente = models.ForeignKey(modelo_cliente, related_name='pedidos', on_delete=models.CASCADE)
    producto = models.CharField(max_length=30, blank=True,null=True)
    cantidad = models.CharField(max_length=30, blank=True,null=True)
    def __unicode__(self):
        return '%s %s %d' % (self.cliente, self.producto, self.cantidad)

class modelo_encargado(models.Model):
    empresa = models.ForeignKey(modelo_empresa,related_name='encargado',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    telefono = models.IntegerField(blank=True)
    def __str__(self):
             return '%s %s %d' % (self.nombre,self.empresa,self.telefono)
