# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User

class modelo_empresa(models.Model):
    empresa = models.CharField(max_length=30)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    tipo_pago = models.CharField(max_length=20,null=True)
    hora_atencion_inicio = models.CharField(max_length=20,null=True)
    hora_atencion_fin = models.CharField(max_length=20,null=True)
    fechas_de_atencion = models.CharField(max_length=25,null=True)
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
    nombre = models.CharField(max_length=30,blank=True,null=True)
    apellido = models.CharField(max_length=30,blank=True,null=True)
    celular = models.IntegerField(blank=True,null=True)
    latitud = models.CharField(max_length=30,blank=True,null=True)
    longitud = models.CharField(max_length=30,blank=True,null=True)
    precio_total = models.CharField(max_length=30,blank=True,null=True)
    distancia = models.CharField(max_length=10,blank=True,null=True)
    tipo_pedido = models.CharField(max_length=15,blank=True,null=True)
    empresa = models.CharField(max_length=30,blank=True,null=True)
    ubicacion = models.CharField(max_length=100,blank=True,null=True)
    encargado = models.CharField(max_length=30,blank=True,null=True)
    status = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    token = models.CharField(max_length=200)
    fecha_programado = models.CharField(max_length=12,blank=True,null=True)
    hora_programado = models.CharField(max_length=12,blank=True,null=True)
    fecha_aceptado = models.DateField(blank=True,null=True)
    hora_aceptado = models.TimeField(blank=True,null=True)
    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.nombre, self.apellido,self.celular,self.latitud,self.longitud,self.precio_total,self.distancia,self.tipo_pedido,self.empresa,
                                                                             self.ubicacion,self.encargado,self.status,self.fecha,self.hora,self.fecha_aceptado,self.hora_aceptado,self.fecha_programado,self.hora_programado,self.token)

class modelo_pedido(models.Model):
    cliente = models.ForeignKey(modelo_cliente, related_name='pedidos', on_delete=models.CASCADE)
    producto = models.CharField(max_length=30, blank=True,null=True)
    cantidad = models.CharField(max_length=30, blank=True,null=True)
    def __unicode__(self):
        return '%s %s %d' % (self.cliente, self.producto, self.cantidad)

class modelo_encargado(models.Model):
    nombre = models.ForeignKey(User)
    telefono = models.IntegerField(blank=True)
    empresa = models.ForeignKey(modelo_empresa,related_name='encargado',on_delete=models.CASCADE)
    class Meta:
            unique_together = (("nombre", "empresa"),)
    def __str__(self):
             return '%s %s %s' % (self.nombre,self.telefono,self.empresa)
