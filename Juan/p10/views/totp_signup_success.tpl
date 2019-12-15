<!DOCTYPE html>
<html lang="en">
<head>
    <title>Success</title>
    <style>
        h1 {
           color: green;
        }
    </style>
</head>
<body>
 <h1>Datos para proceso manual</h1>

 <p>Nombre de usuario: {{ nickname }}</p>
 <p>Semilla: {{ totp_secret }}</p>

 <h1>Código QR</h1>
 <p>
     <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={{ google_auth_uri }}">
 </p>
</body>
</html>
