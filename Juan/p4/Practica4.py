import sqlite3


def open(dbfile):
    conn = sqlite3.connect(dbfile)
    return conn


def setupSalesTable(cursor: sqlite3.Cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Ventas (cifc TEXT, dni TEXT, codcoche TEXT, color TEXT, PRIMARY KEY (cifc,dni,codcoche))")

    sales = [
        ['0001', '0001', '0001', 'blanco'],
        ['0001', '0002', '0005', 'rojo'],
        ['0002', '0003', '0008', 'blanco'],
        ['0002', '0001', '0006', 'rojo'],
        ['0003', '0004', '0011', 'rojo'],
        ['0004', '0005', '0014', 'verde'],
        ['0004', '0005', '0013', 'azul'],
        ['0004', '0004', '0014', 'verde']
    ]

    cursor.executemany("INSERT OR IGNORE INTO Ventas VALUES (:cifc, :dni, :codcoche, :color)", sales)


def setupClientsTable(cursor: sqlite3.Cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Clientes (dni TEXT PRIMARY KEY, nombre TEXT, apellidos TEXT, ciudad TEXT)")

    clients = [
        ['0001', 'Luis', 'Garcia', 'Madrid'],
        ['0002', 'Antonio', 'López', 'Valencia'],
        ['0003', 'Juan', 'Martín', 'Madrid'],
        ['0004', 'María', 'García', 'Madrid'],
        ['0005', 'Javier', 'González', 'Barcelona'],
        ['0006', 'Ana', 'López', 'Barcelona'],
        ['0007', 'Ana', 'López', 'Madrid'],
        ['0008', 'Ana', 'López', 'Barcelona']
    ]

    cursor.executemany("INSERT OR IGNORE INTO Clientes VALUES (:dni, :nombre, :apellidos, :ciudad)", clients);


def setupDistributionTable(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Distribucion (Cifc TEXT, codcoche TEXT, cantidad INTEGER, PRIMARY KEY (Cifc,codcoche))")

    distribution = [
        ['0001', '0001', 3],
        ['0001', '0002', 7],
        ['0001', '0003', 7],
        ['0002', '0006', 5],
        ['0002', '0007', 10],
        ['0002', '0008', 10],
        ['0003', '0010', 5],
        ['0003', '0011', 3],
        ['0003', '0012', 5],
        ['0004', '0013', 10],
        ['0004', '0014', 5]
    ]
    cursor.executemany("INSERT OR IGNORE INTO Distribucion VALUES (:cifm, :codcoche, :cantidad)", distribution)


def setupBrandsTable(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Marcas (Cifm TEXT PRIMARY KEY, Nombre TEXT, Ciudad TEXT)")

    distribution = [
        ['0001', 'seat', 'Madrid'],
        ['0002', 'renault', 'Barcelona'],
        ['0003', 'citroen', 'Valencia'],
        ['0004', 'audi', 'Madrid'],
        ['0005', 'opel', 'Bilbao'],
        ['0006', 'bmw', 'Barcelona']
    ]
    cursor.executemany("INSERT OR IGNORE INTO Marcas VALUES (?,?,?)", distribution)


def setupCarsTable(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Coches (codcoche TEXT PRIMARY KEY,nombre TEXT, modelo TEXT)")

    distribution = [
        ['0001', 'ibiza', 'glx'],
        ['0002', 'ibiza', 'gti'],
        ['0003', 'ibiza', 'gtd'],
        ['0004', 'toledo', 'gtd'],
        ['0005', 'cordoba', 'gti'],
        ['0006', 'megane', '1.6'],
        ['0007', 'megane', 'gti'],
        ['0008', 'laguna', 'gtd'],
        ['0009', 'laguna', 'td'],
        ['0010', 'zx', '16v'],
        ['0011', 'zx', 'td'],
        ['0012', 'xantia', 'gtd'],
        ['0013', 'a4', '1.8'],
        ['0014', 'a4', '2.8'],
        ['0015', 'astra', 'caravan'],
        ['0016', 'astra', 'gti'],
        ['0017', 'corsa', '1.4']
    ]
    cursor.executemany("INSERT OR IGNORE INTO Coches VALUES (?,?,?)", distribution)


def setupMarcoTable(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Marco (Cifm TEXT,codcoche TEXT, PRIMARY KEY(Cifm,codcoche))")

    distribution = [
        ['0001', '0001'],
        ['0001', '0002'],
        ['0001', '0003'],
        ['0001', '0004'],
        ['0001', '0005'],
        ['0002', '0006'],
        ['0002', '0007'],
        ['0002', '0008'],
        ['0002', '0009'],
        ['0003', '0010'],
        ['0003', '0011'],
        ['0003', '0012'],
        ['0004', '0013'],
        ['0004', '0014'],
        ['0005', '0015'],
        ['0005', '0016'],
        ['0005', '0017']
    ]
    cursor.executemany("INSERT OR IGNORE INTO Marco VALUES (?,?)", distribution)


def setupConcesionariosTable(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Concesionarios (Cifc TEXT PRIMARY KEY, Nombre TEXT, Ciudad TEXT)")

    distribution = [
        ['0001', 'acar', 'Madrid'],
        ['0002', 'bcar', 'Madrid'],
        ['0003', 'ccar', 'Barcelona'],
        ['0004', 'dcar', 'Valencia'],
        ['0005', 'ecar', 'Bilbao']
    ]
    cursor.executemany("INSERT OR IGNORE INTO Concesionarios VALUES (?,?,?)", distribution)


def setup(db: sqlite3.Connection):
    cursor = db.cursor()

    setupDistributionTable(cursor)
    setupClientsTable(cursor)
    setupSalesTable(cursor)
    setupBrandsTable(cursor)
    setupCarsTable(cursor)
    setupMarcoTable(cursor)
    setupConcesionariosTable(cursor)

    cursor.close()


def ejecutarConsultas(db: sqlite3.Connection):
    from prettytable import PrettyTable

    cursor = db.cursor()

    print()
    print('Obtener el nombre y el apellido de los clientes que han comprado como mínimo un coche de color ‘verde’ o un coche de color ‘azul’,:')
    cursor.execute("SELECT DISTINCT nombre,apellidos FROM Clientes C JOIN Ventas V "
                   "ON C.dni = V.dni WHERE V.color = 'azul' OR V.color = 'verde'")
    t = PrettyTable(['Nombre', 'Apellidos'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)
    print()

    print('Obtener el nombre de los concesionarios que sólo han vendido coches al cliente con dni igual a 0001:')
    cursor.execute(
        "SELECT C.Nombre FROM Concesionarios C JOIN Ventas V "
        "ON C.cifc = V.cifc "
        "GROUP BY V.cifc "
        "HAVING COUNT(DISTINCT V.dni) = 1 AND V.dni = '0001'")

    t = PrettyTable(['Nombre concesionario'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)
    print()

    print('Obtener los codcoche y la media de los valores del atributo cantidad para cada codcoche que aparece en la relación distribucion para los casos en que la media sea menor que 15:')
    cursor.execute("SELECT AVG(cantidad),codcoche FROM Distribucion "
                   "GROUP BY codcoche "
                   "HAVING AVG(cantidad) < 15")
    t = PrettyTable(['Cantidad media', 'Codcoche'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)
    print()

    print('Obtener para cada valor de dni de los clientes el número de veces que aparece en la relación ventas: ')
    cursor.execute("SELECT dni,Count(*) FROM Ventas GROUP BY dni")
    t = PrettyTable(['Cliente', 'Ventas realizadas'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)
    print()

    print('Obtener el dni de los clientes de nombre ‘pepe’ o de nombre ‘luis’ (no se admiten valores repetidos): ')
    cursor.execute("SELECT DISTINCT dni FROM Clientes WHERE nombre LIKE 'pepe' OR nombre LIKE 'luis'")
    t = PrettyTable(['DNI'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)
    print()

    print('Obtener el cifc de todos los concesionarios cuyo atributo cantidad en la relación distribucion no está comprendido entre 10 y 18 ambos inclusive (es decir, los valores menores que 10 y mayores que 18): ')
    cursor.execute("SELECT DISTINCT C.cifc FROM Concesionarios C JOIN Distribucion D "
                   "ON C.cifc = D.cifc "
                   "GROUP BY C.cifc "
                   "HAVING SUM(cantidad) < 10 OR SUM(cantidad) > 18")
    t = PrettyTable(['Cifc'])
    rows = cursor.fetchall()

    for row in rows:
        t.add_row(row)

    print(t)

    cursor.close()


db = open("vehiculos.sqlite")
setup(db)
ejecutarConsultas(db)
db.commit()
db.close()
