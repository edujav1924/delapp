from app.models import *
from rest_framework import serializers

class productoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelo_producto
        fields = ('producto','precio')

class pedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelo_pedido
        fields = ('producto', 'cantidad')

class encargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelo_encargado
        fields = ('nombre', 'telefono')
class clienteSerializer(serializers.ModelSerializer):
    pedidos = pedidoSerializer(many=True)

    class Meta:
        model = modelo_cliente
        fields = ('cliente_id','nombre', 'apellido', 'celular','pedidos','ubicacion','encargado','status','fecha','hora')

    def create(self, validated_data):
        pedidos_data = validated_data.pop('pedidos')
        print pedidos_data
        cliente_1 = modelo_cliente.objects.create(**validated_data)
        for pedido in pedidos_data:
            modelo_pedido.objects.create(cliente=cliente_1, **pedido)
        return cliente_1
