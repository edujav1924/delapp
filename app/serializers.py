from rest_framework import serializers
from app.models import modelocliente,modeloencargado,modelodespachopedido,modeloempresa
class modelopedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelodespachopedido
        fields =('pedido_id','encargado','pedido_cliente','pedido_cliente_nombre')

class modeloclienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelocliente
        fields = ('cliente_pedido','cliente_nombre','cliente_ubicacion')

class modeloempresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = modeloempresa
        fields = ('nombre')

class modeloencargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modeloencargado
        fields = ('nombre','telefono')
