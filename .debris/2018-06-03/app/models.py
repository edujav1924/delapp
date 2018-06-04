# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class modelo_comentario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    comentario = models.CharField(max_length=200)
class modelo_empresa(models.Model):
    empresa = models.CharField(max_length=30)
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    tipo_pago = models.CharField(max_length=20)
    hora_atencion_inicio = models.TimeField(max_length=20)
    hora_atencion_fin = models.TimeField(max_length=20)
    fechas_de_atencion = models.CharField(max_length=25)
    rango_delivery = models.CharField(max_length=200)
    costo_delivery = models.CharField(max_length=200)
    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s' % (self.empresa, self.latitud, self.longitud,self.telefono,self.tipo_pago,self.hora_atencion_inicio,self.hora_atencion_fin
                                                     ,self.fechas_de_atencion,self.rango_delivery,self.costo_delivery)

class modelo_producto(models.Model):
    empresa = models.ForeignKey(modelo_empresa,related_name='productos',on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    precio = models.PositiveIntegerField()
    def __unicode__(self):
        return '%s %s %d' % (self.empresa, self.producto, self.precio)

class modelo_cliente(models.Model):
    cliente_id =models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    celular = models.IntegerField(blank=True)
    latitud = models.CharField(max_length=30)
    longitud = models.CharField(max_length=30)
    precio_total = models.CharField(max_length=30)
    distancia = models.CharField(max_length=10,blank=True,null=True)
    tipo_pedido = models.CharField(max_length=15)
    empresa = models.CharField(max_length=30)
    ubicacion = models.CharField(max_length=100,blank=True,null=True)
    encargado = models.CharField(max_length=30,blank=True,null=True)
    comentario = models.CharField(max_length=200,blank=True,null=True)
    status = models.IntegerField(default=0,validators=[MaxValueValidator(3), MinValueValidator(0)])
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    token = models.CharField(max_length=200)
    fecha_programado = models.DateField(null=True)
    hora_programado = models.TimeField(null=True)
    fecha_aceptado = models.DateField(blank=True,null=True)
    hora_aceptado = models.TimeField(blank=True,null=True)
    def __unicode__(self):
        return '%s %s %d %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.nombre,self.apellido,self.celular,self.latitud,self.longitud,self.precio_total,self.distancia,self.tipo_pedido,self.empresa,self.comentario,
                                                                             self.ubicacion,self.fecha,self.hora,self.token,self.encargado,self.status,self.fecha_aceptado,self.hora_aceptado,self.fecha_programado,self.hora_programado)

class modelo_pedido(models.Model):
    cliente = models.ForeignKey(modelo_cliente, related_name='pedidos', on_delete=models.CASCADE)
    producto = models.CharField(max_length=200, blank=True,null=True)
    cantidad = models.CharField(max_length=30, blank=True,null=True)
    def __unicode__(self):
        return '%s %s %s' % (self.cliente, self.producto, self.cantidad)


class modelo_encargado(models.Model):
    cargo= (
    ('Sp', 'Supervisor'),
    ('En', 'Encargado'),
)
    nombre = models.ForeignKey(User)
    telefono = models.IntegerField(blank=True)
    puesto = models.CharField(max_length=15,choices=cargo)
    empresa = models.ForeignKey(modelo_empresa,related_name='encargado',on_delete=models.CASCADE)
    class Meta:
            unique_together = (("nombre", "empresa"),)
    def __str__(self):
             return '%s %d %s %s' % (self.nombre,self.telefono,self.puesto,self.empresa)

class modelo_contador(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField( default=0 , null=True)
    def __str__(self):
             return '%s %s %d' % (self.fecha,self.hora,self.cantidad)
