<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
         <h1>{{title}}: {{len(coincidences)}} coincidencias</h1>
         <table>
             <tr>
                 <td>Nombre de usuario</td>
                 <td>E-mail</td>
                 <td>Página web</td>
                 <td>Tarjeta de crédito</td>
                 <td>Hash de contraseña</td>
                 <td>Nombre</td>
                 <td>Apellido</td>
                 <td>Dirección</td>
                 <td>Aficiones</td>
                 <td>Fecha de nacimiento</td>
             </tr>
             % for coincidence in coincidences:
             <tr>
                 <td>{{coincidence['_id']}}</td>
                 <td>{{coincidence['email']}}</td>
                 <td>{{coincidence['webpage']}}</td>
                 <td>{{coincidence['credit_card']['number']}} - {{coincidence['credit_card']['expire']['month']}}/{{coincidence['credit_card']['expire']['year']}}</td>
                 <td>{{coincidence['password']}}</td>
                 <td>{{coincidence['name']}}</td>
                 <td>{{coincidence['surname']}}</td>
                 <td>{{coincidence['address']['street']}},{{coincidence['address']['num']}}, {{coincidence['address']['country']}} ({{coincidence['address']['zip']}}) </td>
                 <td>{{', '.join(coincidence['likes'])}}</td>
                 <td>{{coincidence['birthdate']}}</td>
             </tr>
             % end
         </table>
    </body>
</html>