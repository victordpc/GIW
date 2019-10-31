<html lang="es">

<head>
    <title>Gestor de plantas medicinales</title>
    <meta charset="utf-8">
</head> 

<body>
    <header>
       <h1>Servicio1</h1>
    </header>
    <div class="contenido">
        <form action="/servicio11" method="post">
            <p>
                <select name="plantas">
                % for elemento in lista:
                    <option>{{elemento}}</option>
                % end
                </select>
                <input type="submit" value=">>">
            </p>
        </form>
    </div>
</body>

</html>