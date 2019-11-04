<html lang="es">

<head>
    <title>Buscar Usuario</title>
    <meta charset="utf-8">
</head> 

<body>
    <header>
       <h1>El número de resultado esncontrados es: %len(msg)</h1>
    </header>
    <div class="contenido">
        <ul>
            % for elemento in msg:
            <li>{{elemento}}</li>
            % end
        </ul>
    </div>
</body>

</html>