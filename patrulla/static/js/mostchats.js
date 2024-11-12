document.addEventListener('DOMContentLoaded', function() {
    var contenedorchat = document.getElementById('contenedorchat');
    var nom_us = contenedorchat.getAttribute('data-nomus');

    console.log("usuario:", nom_us);

    if (nom_us !== "None" || nom_us !== Null || nom_us !== undefined) {
        console.log('usuario encontrado', nom_us)
        contenedorchat.style.display = "block";
    }
});
