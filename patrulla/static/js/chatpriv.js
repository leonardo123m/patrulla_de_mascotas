$(document).ready(function(){
    const socket=io(); // esta constante sirve para mantener la conexion en tiempo real con el servidor

    const formmsgpriv = $('#formmsgpriv'); // obtenemos el formulario de los mensajes mediante su id
    const msgpriv = $('#msgpriv'); // obtenemos el valor de la caja de texto para enviar mensajes mediante su id
    const chatpriv = $('#chatpriv'); // obtenemos el cuerpo del chat mediante su id


    formmsgpriv.submit (e=>{ // creamos una funcion que nos detecta el momento en el que un mensaje es enviado meddiante su tipo de input submit
        e.preventDefault();
        socket.emit('envmsgpriv', {mensajepriv: msgpriv.val(), destinatario: destinatario}); // Esta funcion sirve para enviar el mensaje y el destinatario desde el cliente al servidor para que este sepa a donde/quien enviar el mensaje
        msgpriv.val('');
    })


    socket.on('nuevo mensaje privado', function(data){
        if  (data.mensaje && data.remitente){
            console.log('mensaje: ', data.mensaje, ' enviado por: ', data.remitente, ' a: ', data.destinatario);
            chatpriv.append(`<p><strong>${data.remitente}:</strong> ${data.mensaje}</p>`);
            chatpriv.append(`<p><strong>${data.desinatario}:</strong> ${data.mensaje}</p>`);
        }
        else{
            console.log('error falta informacion de usuarios')
        }
    })




});