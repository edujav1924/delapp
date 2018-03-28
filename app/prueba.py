from rest_framework import *
from app.models import *
from app.serializers import *
from collections import OrderedDict
from json import loads,dumps
user = modelo_cliente.objects.create(nombre="lety",apellido="gomez",celular=032)
modelo_pedido.objects.create(cliente=user,producto="lomito",cantidad=5)
modelo_pedido.objects.create(cliente=user,producto="coca",cantidad=2)
modelo_pedido.objects.create(cliente=user,producto="coca 1ls",cantidad=2)
serializer = clienteSerializer(instance=user)
a = serializer.data
b = loads(dumps(a))
s = clienteSerializer(data=a)
s.is_valid()
user = modelo_cliente.objects.create(nombre="lucas",apellido="lopez",celular=032)
modelo_pedido.objects.create(cliente=user,producto="lomito",cantidad=5)
modelo_pedido.objects.create(cliente=user,producto="hamburguesa",cantidad=1)
modelo_pedido.objects.create(cliente=user,producto="cerveza",cantidad=1)
serializer = clienteSerializer(instance=user)
a = serializer.data
b = loads(dumps(a))
s = clienteSerializer(data=a)
s.is_valid()
s = clienteSerializer(data=b)
s.is_valid()
    {'nombre': u'edu', 'celular': 26, 'apellido': u'gonzalez', 'cliente':[OrderedDict([('tipo', u'hamburguesa'), ('cantidad', 5)]), OrderedDict([('tipo', u'lomito'), ('cantidad', 2)])]}
from json import loads, dumps
from collections import OrderedDict
 dumps({'nombre': u'edu', 'celular': 26, 'apellido': u'gonzalez', 'cliente':[OrderedDict([('tipo', u'hamburguesa'), ('cantidad', 5)]), OrderedDict([('tipo', u'lomito'), ('cantidad', 2)])]}
)
{u'nombre': u'edu', u'celular': 26, u'apellido': u'gonzalez', u'cliente': [{u'cantidad': 5, u'tipo': u'hamburguesa'}, {u'cantidad': 2, u'tipo': u'lomito'}]}
data = {
    u'album_name': u'The Grey Album',
    u'artist': 'Danger Mouse',
    u'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
    ],
}
{u'nombre': u'edu', u'apellido': u'gonzalez', u'celular': 26, u'pedidos': [{u'cantidad': 5, u'tipo': u'hamburguesa'}, {u'cantidad': 2, u'tipo': u'lomito'}]}


{"nombre": "edu", "apellido": "gonzalez", "celular": 26, "cliente": [{"tipo": "hamburguesa", "cantidad": 5}, {"tipo": "lomito", "cantidad": 2}]}
{'nombre': 'edu', 'celular': 26, 'apellido': 'gonzalez', 'cliente': [{'cantidad': 5, 'tipo': 'hamburguesa'}, {'cantidad': 2, 'tipo': 'lomito'}]}
{'tracks': [OrderedDict([('order', 1), ('title', u'Public Service Announcement'), ('duration', 245)]), OrderedDict([('order', 1), ('title', u'Public Service Announcement'), ('duration', 245)]), OrderedDict([('order', 2), ('title', u'What More Can I Say'), ('duration', 264)])], 'album_name': u'The Grey Album', 'artist': u'Danger Mouse'}
https://www.google.com/maps?q=-25.2454117,-57.4382988&z=17&hl=es
https://www.google.com/maps?q=-25.280438333333336,-57.53782666666666=17&hl=es


<script type="text/javascript">
""$(document).ready(function(){
    var myFunction = function() {
      $( "#hola" ).load("http://127.0.0.1:8000/pedidosrecientes/ #hola");

    };
    myFunction();
    setInterval(myFunction, 60000);
    $('#Notifications').click(function(){

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/ajax/",
        success: function(data) {
            console.log(document.getElementById('hhh').innerHTML);
            document.getElementById('hhh').innerHTML = data;
        }
    });

});

});

</script>


from rest_framework import *
from app.models import *
from app.serializers import *
from collections import OrderedDict
from json import loads,dumps
modelo_producto.objects.create(producto="hamburguesa chica",precio=7000)
modelo_producto.objects.create(producto="hamburguesa grande",precio=10000)
modelo_producto.objects.create(producto="coca cola mediana",precio=5000)
modelo_producto.objects.create(producto="coca cola grande",precio=10000)
modelo_producto.objects.create(producto="lomito",precio=12000)
modelo_encargado.objects.create(nombre="AZUL",telefono=0)
modelo_encargado.objects.create(nombre="VERDE",telefono=1)
modelo_encargado.objects.create(nombre="ROJO",telefono=2)
