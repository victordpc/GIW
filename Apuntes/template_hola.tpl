<!DOCTYPE html>
<html lang="es">
<head>
<title>Bienvenido {{nombre}}</title>
<meta charset="utf-8" />
</head>
 
<body>
    <header>
       <h1>Este es mi sitio web</h1>
       <p>Esta creado con tecnolog&iacute;a bottle</p>
    </header>
    <h2>Bienvenido</h2>
    % if nombre=="Mundo":
      <p> &iexcl;Hola <strong>{{nombre}}!</strong></p>
    %else:
      <h1>&iexcl;Hola {{nombre.title()}}!</h1>
      <p>&iquest;C&oacute;mo est&aacute;s?</p>
    %end
</body>
</html>