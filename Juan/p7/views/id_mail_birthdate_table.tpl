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
                 <td>Fecha de nacimiento</td>
             </tr>
             % for coincidence in coincidences:
             <tr>
                 <td>{{coincidence['_id']}}</td>
                 <td>{{coincidence['email']}}</td>
                 <td>{{coincidence['birthdate']}}</td>
             </tr>
             % end
         </table>
    </body>
</html>