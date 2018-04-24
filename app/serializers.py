from app.models import *
from rest_framework import serializers
class productoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelo_producto
        fields = ('producto','precio')

class empresaSerializer(serializers.ModelSerializer):
    productos = productoSerializer(many=True)
    class Meta:
        model = modelo_empresa
        fields = ('empresa','latitud','longitud','productos')

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        print productos_data
        empresa_1 = modelo_empresa.objects.create(**validated_data)
        for p in productos_data:
            modelo_producto.objects.create(cliente=empresa_1, **p)
        return empresa_1



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
        fields = ('cliente_id','nombre', 'apellido', 'celular','pedidos','ubicacion','empresa','encargado','status','fecha','hora')

    def create(self, validated_data):
        pedidos_data = validated_data.pop('pedidos')
        print pedidos_data
        cliente_1 = modelo_cliente.objects.create(**validated_data)
        for pedido in pedidos_data:
            modelo_pedido.objects.create(cliente=cliente_1, **pedido)
        return cliente_1
