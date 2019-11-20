from mongoengine import PULL
from mongoengine import connect
from mongoengine import ValidationError
from mongoengine import IntField, FloatField, StringField
from mongoengine import ComplexDateTimeField, DateTimeField
from mongoengine import Document, DynamicDocument, EmbeddedDocument
from mongoengine import ListField, ReferenceField, EmbeddedDocumentField

from datetime import datetime


# Document --> No permite guardar campos no declarados en el esquema.
# DynamicDocument --> Permite almacenar campos que no estan en el esquena.
# Una clase ha de tener el mismo nombre que la coleccion y las variables el mismo nombre que el campo en la coleccion.
# pero esto puede cambiarse: nombre = StringField(db_field='name')
# Object.save() --> Inserta el objeto en mongoDB si pasa la validacion

class Producto(Document):
    codigoBarras = StringField(required=True, min_length=13, max_length=13, regex="^[0-9]{13}$")
    nombre = StringField(required=True)
    categoriaPrincipal = IntField(required=True, min_value=0)
    listaCategoriasSecundarias = ListField(IntField(required=False, min_value=0))

    def clean(self):  # Se lanza al llamar a .save(), permite hacer comprobaciones personalizadas.

        # Los 2-3 primeros digitos identifican al pais.
        # Codigo del/la fabricante/empresa: Entre 5 y 8 dígitos.
        # Producto + Fabricante = 9 o 10 digitos (dependiendo de la longitud del codigo del pais)
        # Codigo del producto: Producto + Fabricante + (2-3 digitos) --> En total son los 12 primeros digitos.
        # Digito de control: 1 digito, sirve para verificar que el código leído es correcto.
        # Calculo del digito de control: Se suman los dígitos de las posiciones impares, se multiplica por 3,
        # se le suman los dígitos de las posiciones pares. El resultado final ha de coincidir con el dígito de control.

        tenPower = 1

        controlNumber = 0

        for index in range(0, 12):
            controlNumber += (int(self.codigoBarras[index])) if (index % 2 == 0) else (
                        int(self.codigoBarras[index]) * 3)

        while (controlNumber - tenPower > 0):
            tenPower *= 10

        controlNumber = tenPower - controlNumber

        if (controlNumber != int(self.codigoBarras[12])):
            raise ValidationError(f"El digito de control es {self.codigoBarras[12]} pero deberia ser {controlNumber}")

        if (self.categoriaPrincipal != self.listaCategoriasSecundarias[0]):
            raise ValidationError(
                f"La categoria principal {self.categoriaPrincipal} no aparece como la primera de las secundarias {self.listaCategoriasSecundarias[0]}")

        if (self.categoriaPrincipal != int(self.categoriaPrincipal)):
            raise ValidationError(f"La categoria principal {self.categoriaPrincipal} no es un numero natural.")

        for categoria in self.listaCategoriasSecundarias:

            if (categoria != int(categoria)):
                raise ValidationError(f"La categoria secundaria {categoria} no es un numero natural.")


class LineaPedido(EmbeddedDocument):
    cantidadProductosComprados = IntField(required=True, min_value=1)
    precioProducto = FloatField(required=True, min_value=0)
    nombreProducto = StringField(required=True)
    precioTotalLinea = FloatField(required=True, min_value=0)
    referenciaProducto = ReferenceField(Producto, required=True)

    def clean(self):  # Se lanza al llamar a .save(), permite hacer comprobaciones personalizadas.

        if (self.precioTotalLinea != self.cantidadProductosComprados * self.precioProducto):
            raise ValidationError(
                f"El preio de la linea es {self.precioTotalLinea} pero deberia ser {self.cantidadProductosComprados * self.precioProducto}")

        if (self.nombreProducto != self.referenciaProducto.nombre):
            raise ValidationError(
                f"El nombre del producto es {self.nombreProducto} pero referencia a {self.referenciaProducto.nombre}")


class Pedido(Document):
    precioTotalPedido = FloatField(required=True, min_value=0)
    fechaPedido = ComplexDateTimeField(required=True, separator="-")
    listaLineasPedido = ListField(EmbeddedDocumentField(LineaPedido, required=True))

    def clean(self):  # Se lanza al llamar a .save(), permite hacer comprobaciones personalizadas.

        totalLineas = 0

        for linea in self.listaLineasPedido:
            totalLineas += linea.precioTotalLinea

        if (totalLineas != self.precioTotalPedido):
            raise ValidationError(
                f"El precio total {self.precioTotalPedido} no coincide con la suma de las lineas {totalLineas}")


class TarjetaCredito(EmbeddedDocument):
    nombrePropietario = StringField(required=True)
    numeroTarjeta = StringField(required=True, min_length=16, max_length=16, regex="^[0-9]{16}$")
    mesCaducidad = StringField(required=True, min_length=2, max_length=2, regex="^[0-9]{2}$")
    añoCaducidad = StringField(required=True, min_length=4, max_length=4, regex="^[0-9]{4}$")
    codigoVerificacionTarjeta = StringField(required=True, min_length=3, max_length=3, regex="^[0-9]{3}$")

    def clean(self):  # Se lanza al llamar a .save(), permite hacer comprobaciones personalizadas.

        mes = int(self.mesCaducidad)
        año = int(self.añoCaducidad)

        if (mes < 1 or mes > 12):
            raise ValidationError(f"El mes {mes} no es un mes valido.")

        if (año < datetime.today().year):
            raise ValidationError(f"El año {año} no es un año valido.")

        if (año != datetime.today().year + 4):
            raise ValidationError(f"Año de caducidad {año} incorrecto, las tarjetas se renuevan cada cuatro años.")

        if (mes != datetime.today().month):
            raise ValidationError(f"El mes de caducidad ({mes}) difiere del de expedicion ({datetime.today().month}).")


class Usuario(DynamicDocument):
    dni = StringField(required=True, unique=True, min_length=9, max_length=9, regex="^[0-9]{8}[A-Z]{1}$")
    nombre = StringField(required=True)
    primerApellido = StringField(required=True)
    segundoApellido = StringField(required=False)
    fechaNacimiento = DateTimeField(required=True, separator="-")
    fechaUltimosDiezAccesos = ListField(ComplexDateTimeField(required=False, separator="-"))
    listaTarjetasCredito = ListField(EmbeddedDocumentField(TarjetaCredito, required=False))
    listaReferenciasPedidos = ListField(ReferenceField(Pedido, required=False, reverse_delete_rule=PULL))

    def clean(self):  # Se lanza al llamar a .save(), permite hacer comprobaciones personalizadas.

        numero = int(self.dni[0:8])

        letras = "TRWAGMYFPDXBNJZSQVHLCKE"

        if (self.dni[8] != letras[numero % 23]):
            raise ValidationError(f"El DNI {self.dni} es incorrecto, fallo en el calculo de su letra.")


def insertar():
    # Inserción de productos.

    productos = []

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Samurai Sword",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 17]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Dominion",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 11]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Trivial",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 24]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Saboteur",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 24]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Colonos de Catan",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 24]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Carcasone",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 16]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="Bang",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 11]
    )

    productos.append(producto)

    producto = Producto(
        codigoBarras="9780201379624",
        nombre="El espía que se perdió",
        categoriaPrincipal=0,
        listaCategoriasSecundarias=[0, 8, 9]
    )

    productos.append(producto)

    try:

        for producto in productos:
            producto.save()

    except Exception as ex:

        print(ex)

    for producto in Producto.objects:
        print(
            producto.codigoBarras,
            producto.nombre,
            producto.categoriaPrincipal,
            producto.listaCategoriasSecundarias
        )

    print()

    # Creacion de los pedidos y sus líneas.

    pedidos = []

    pedido = Pedido(
        precioTotalPedido=84.90,
        fechaPedido=datetime.strptime('2019-11-2-08-15-27-243860', '%Y-%m-%d-%H-%M-%S-%f'),
        listaLineasPedido=[]
    )

    pruebaBorrado = pedido

    linea = LineaPedido(
        cantidadProductosComprados=2,
        precioProducto=24.95,
        nombreProducto="Colonos de Catan",
        precioTotalLinea=49.90,
        referenciaProducto=Producto.objects.get(nombre="Colonos de Catan")
    )

    pedido.listaLineasPedido.append(linea)

    linea = LineaPedido(
        cantidadProductosComprados=1,
        precioProducto=35.00,
        nombreProducto="Carcasone",
        precioTotalLinea=35.00,
        referenciaProducto=Producto.objects.get(nombre="Carcasone")
    )

    pedido.listaLineasPedido.append(linea)

    pedidos.append(pedido)

    pedido = Pedido(
        precioTotalPedido=44.95,
        fechaPedido=datetime.strptime('2019-11-2-08-15-27-253960', '%Y-%m-%d-%H-%M-%S-%f'),
        listaLineasPedido=[]
    )

    linea = LineaPedido(
        cantidadProductosComprados=1,
        precioProducto=12.50,
        nombreProducto="Bang",
        precioTotalLinea=12.50,
        referenciaProducto=Producto.objects.get(nombre="Bang")
    )

    pedido.listaLineasPedido.append(linea)

    linea = LineaPedido(
        cantidadProductosComprados=1,
        precioProducto=32.45,
        nombreProducto="El espía que se perdió",
        precioTotalLinea=32.45,
        referenciaProducto=Producto.objects.get(nombre="El espía que se perdió")
    )

    pedido.listaLineasPedido.append(linea)

    pedidos.append(pedido)

    pedido = Pedido(
        precioTotalPedido=58.60,
        fechaPedido=datetime.strptime('2019-8-15-13-20-30-499992', '%Y-%m-%d-%H-%M-%S-%f'),
        listaLineasPedido=[]
    )

    linea = LineaPedido(
        cantidadProductosComprados=3,
        precioProducto=12.00,
        nombreProducto="Samurai Sword",
        precioTotalLinea=36.00,
        referenciaProducto=Producto.objects.get(nombre="Samurai Sword")
    )

    pedido.listaLineasPedido.append(linea)

    linea = LineaPedido(
        cantidadProductosComprados=2,
        precioProducto=11.30,
        nombreProducto="Saboteur",
        precioTotalLinea=22.60,
        referenciaProducto=Producto.objects.get(nombre="Saboteur")
    )

    pedido.listaLineasPedido.append(linea)

    pedidos.append(pedido)

    pedido = Pedido(
        precioTotalPedido=139.75,
        fechaPedido=datetime.strptime('2019-8-15-13-20-30-500000', '%Y-%m-%d-%H-%M-%S-%f'),
        listaLineasPedido=[]
    )

    linea = LineaPedido(
        cantidadProductosComprados=2,
        precioProducto=50.00,
        nombreProducto="Trivial",
        precioTotalLinea=100.00,
        referenciaProducto=Producto.objects.get(nombre="Trivial")
    )

    pedido.listaLineasPedido.append(linea)

    linea = LineaPedido(
        cantidadProductosComprados=1,
        precioProducto=39.75,
        nombreProducto="Dominion",
        precioTotalLinea=39.75,
        referenciaProducto=Producto.objects.get(nombre="Dominion")
    )

    pedido.listaLineasPedido.append(linea)

    pedidos.append(pedido)

    try:

        for pedido in pedidos:
            pedido.save()

    except Exception as ex:

        print(ex)

    for pedido in Pedido.objects:
        print(
            pedido.precioTotalPedido,
            pedido.fechaPedido,
            pedido.listaLineasPedido
        )

    print()

    # Inserción de usuarios y sus tarjetas de crédito (tambien asignamos sus pedidos).

    usuarios = []

    usuario = Usuario(
        dni="05959302W",
        nombre="Manuel",
        primerApellido="Guerrero",
        segundoApellido="Moñús",
        fechaNacimiento=datetime(1994, 10, 15),
        listaReferenciasPedidos=[
            Pedido.objects.get(fechaPedido=datetime.strptime('2019-11-2-08-15-27-243860', '%Y-%m-%d-%H-%M-%S-%f')),
            Pedido.objects.get(fechaPedido=datetime.strptime('2019-11-2-08-15-27-253960', '%Y-%m-%d-%H-%M-%S-%f'))
        ]
    )

    tarjeta = TarjetaCredito(
        nombrePropietario="Manuel",
        numeroTarjeta="0123456789012345",
        mesCaducidad=str(datetime.today().month),
        añoCaducidad=str(datetime.today().year + 4),
        codigoVerificacionTarjeta="123"
    )

    usuario.listaTarjetasCredito.append(tarjeta)

    usuarios.append(usuario)

    usuario = Usuario(
        dni="74960173E",
        nombre="Víctor",
        primerApellido="Del Pino",
        segundoApellido="Castilla",
        fechaNacimiento=datetime(1988, 7, 5),
        listaReferenciasPedidos=[
            Pedido.objects.get(fechaPedido=datetime.strptime('2019-8-15-13-20-30-499992', '%Y-%m-%d-%H-%M-%S-%f')),
            Pedido.objects.get(fechaPedido=datetime.strptime('2019-8-15-13-20-30-500000', '%Y-%m-%d-%H-%M-%S-%f'))
        ]
    )

    tarjeta = TarjetaCredito(
        nombrePropietario="Víctor",
        numeroTarjeta="0000111122223333",
        mesCaducidad=str(datetime.today().month),
        añoCaducidad=str(datetime.today().year + 4),
        codigoVerificacionTarjeta="456"
    )

    usuario.listaTarjetasCredito.append(tarjeta)

    tarjeta = TarjetaCredito(
        nombrePropietario="Víctor",
        numeroTarjeta="4444555566667777",
        mesCaducidad=str(datetime.today().month),
        añoCaducidad=str(datetime.today().year + 4),
        codigoVerificacionTarjeta="789"
    )

    usuario.listaTarjetasCredito.append(tarjeta)

    usuarios.append(usuario)

    try:

        for usuario in usuarios:
            usuario.save()

    except Exception as ex:

        print(ex)

    for usuario in Usuario.objects:
        print(
            usuario.dni,
            usuario.nombre,
            usuario.primerApellido,
            usuario.segundoApellido,
            usuario.fechaNacimiento,
            usuario.fechaUltimosDiezAccesos,
            usuario.listaTarjetasCredito,
            usuario.listaReferenciasPedidos
        )

    try:

        pruebaBorrado.delete()

    except Exception as ex:

        print(ex)


# Operadores de consulta
# Mascota.objects(nombre__ne=”Fifi”) → distinto
# Persona.objects(edad__gt=10) → mayor que
# Persona.objects(edad__lte=10) → menor o igual a
# Persona.objects(nombre__in=["Eva","Pepe"]) → campo toma valores en un listado
# Persona.objects(dir__calle="Mayor")
# Persona.objects(dir__numero__gt=6)
# Ave.objects(nombre__endswith='i')
# Persona.objects(nombre='Eva', dir__calle='Mayor') --> AND
# Persona.objects(dir__calle='Mayor', edad__gt=25) --> AND
# Persona.objects( Q(edad=5) | Q(nombre='Pep') ) --> OR
# Persona.objects( Q(nombre='Pep') | (Q(edad=5) & Q(dir__calle='Mayor')) ) --> OR y AND
# Persona.objects(__raw__={'edad':{'$gt':5}}) --> Si queremos usar la sintaxis de mongo
# Persona.objects.only('nombre') --> Proyecta solamente el campo "nombre"
# Persona.objects(edad__gt=5).only('nombre','dir') --> Proyecta unicamente los campos "nombre" y "dir".
# Persona.objects(nombre='Eva')[:5] --> Filtra el numero de documentos a devolverse
# Persona.objects[10:20] --> Filtra el numero de documentos a devolverse
# Persona.objects(edad=55)[0] --> Filtra el numero de documentos a devolverse
# Persona.objects(nombre='Eva').limit(5) --> Filtra el numero de documentos a devolverse
# Persona.objects.skip(10).limit(10) --> Filtra el numero de documentos a devolverse
# Persona.objects(edad=55).first() --> Filtra el numero de documentos a devolverse
# Mascota.objects.get(nombre='Fifi') --> Si estamos seguros que el resultado de la busqueda solo devuelve un resultado.
# Mascota.objects.order_by('+nombre') --> Ordenar ascendente
# Mascota.objects.order_by('-edad', '+nombre')  --> Ordenar descendente y luego ascendente
# Mascota.objects(tipo='Gato').order_by('+edad') --> Ordenar ascendente
# ps = Persona.objects(nombre='Eva'); len(ps) ; ps.count() --> Obtener el numero  de resutados.

try:

    connect('practica8DB')

    insertar()

except Exception as ex:

    print(ex)