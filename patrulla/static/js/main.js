//Conexion de socket del cliente
var contenedorchat = document.getElementById('contenedorchat');
$(document).ready(function() { // nos agrega una funcion para hacer nuestro codigo en el que podremos mandar los mensajes
    const socket = io(); // Esta constante se encarga de mantener la conexion en tiempo real con el servidor 

    const formmsg = $('#form-msg'); // obtenemos el formulario de los mensajes mediante su id en el html
    const msg = $('#msg'); // obtenemos la caja de texto del mensaje mediante su id
    const chat = $('#chat'); // obtenemos el cuerpo del chat mediante su id
    const usuario = contenedorchat.getAttribute('data-nomus');


    formmsg.submit( e =>{ // creamos una funcion que nos detecta el momento en el que se envia el mensaje
        e.preventDefault(); // esta linea evita que se reinicia la pagina despues de enviar el mensaje, ya que normalmente cuando se envia un formulario la pagina debe reiniciarse para manda rlos datos
        console.log(msg.val()); // Obtenemos el valor que hay dentro de la caja de texto(el mensaje)
        socket.emit('envmsg', {mensaje:msg.val(), usuario:usuario});   // Captura un valor de la caja de mensaje y el usuario para enviarlo a traves del evento envmsg al python
        msg.val(''); // Reinicia el valor de la caja del mensaje cuando se envia el mensaje

    })

    socket.on('nuevo mensaje', function(data){ // Recibimos el valor del mensaje, pero no el valor del mensaje desde lo que mando el cliente, sino el valor que guardo el servidor para poder enviarlo a los demas usuarios
        console.log('mensaje enviado por: ', data.usuario)
        chat.append(data.usuario, ': ', data.mensaje + '<br/>') // Usamos la constante chat, que es el cuerpo del chat:,c y usamos append para agregarle al cuerpo del chat los datos recogidos por el servidor
    })



    

  });