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





  <div class="container-fluid">
    {% csrf_token %}
    <div class="card">
      <div class="card-header card text-white bg-dark mb-3">
        <div class="row">
          <div id="header" class="col-sm" align="center">
            <h2>Pedidos</h2>
          </div>
          <div id="header" class="col-sm" align="center">
            <button id="btn-noti" type="button" class="btn btn-warning">
              Nuevos Pedidos <span id="noti" class="badge badge-light"></span>
            </button>
          </div>
          <div id="header" class="col-sm" align="center">
            <input  onclick="window.open('http://192.168.43.158:8000/home/nuevo')" type="button"  class="btn btn-outline-warning" value="+ Nuevo Pedido" />
            <input  onclick="window.open('http://192.168.43.158:8000/home/encargados')" type="button"  class="btn btn-outline-warning" value="Encargados" />
            <input  onclick="window.open('http://192.168.43.158:8000/home/datos')" type="button"  class="btn btn-outline-warning" value="Datos almacenados" />
            <label for="[object Object]">{{user.username}}</label>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table id="example" class="table table-striped table-bordered " style="text-align: center;">
            {% if datos %}
            <thead>

              <tr>
                <th scope="col">Nombre</th>
                <th scope="col">Celular</th>
                <th scope="col">producto</th>
                <th scope="col">ubicacion</th>
                <th scope="col">encargado</th>
                <th scope="col">Aceptar</th>
                <th>Cancelar</th>
              </tr>
            </thead>
            <tbody>
              {% for dato in datos %}

              <tr id=row-{{dato.cliente_id}}>
                <div>
                  <td data-priority="1" id={{dato.cliente_id}}-name>{{dato.nombre}} {{dato.apellido}}</td>
                  <td id={{dato.cliente_id}}-telefono>{{dato.celular}}</td>
                  <td id={{dato.cliente_id}}-producto>
                    <ul>
                      {%for y in dato.pedidos%}
                      <li style="text-align:left;"> <strong>{{y.cantidad}}</strong> {{y.producto}}</li>
                      {%endfor%}
                    </ul>
                  </td>
                  <td><a id={{dato.cliente_id}}-ubicacion href={{dato.ubicacion}} target="_blank">Ubicacion</a></td>
                  <td>
                    <div class="">
                      <select id={{dato.cliente_id}}-encargado style="width:150px;" class="custom-select">
                        <option value="value">--seleccione--</option>
                        {%for e in encargados %}
                        <option value={{e.nombre}}>{{e.nombre}}</option>
                        {%endfor%}
                      </select>
                    </div>
                  </td>
                  <td>
                    <button id='aceptar-{{dato.cliente_id}}' type="button" class="btn btn-primary confirm">Aceptar</button>
                  </td>
                  <td>
                    <button id='rechazar-{{dato.cliente_id}}' type="button" class="btn btn-danger delete">Eliminar</button>
                  </td>
                </div>
              </tr>
              {% endfor %}
              <span id="jola" hidden>{{valor}}</span>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</div>
    {% else %}
    <p>no hay pedidos disponibles</p>
    {% endif %}
  </body>
