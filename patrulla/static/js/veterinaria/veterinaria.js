function iniciarMap() {

    const latitud = parseFloat(document.getElementById('latitud').textContent);
    const longitud = parseFloat(document.getElementById('longitud').textContent);

    console.log('Latitud:', latitud);
    console.log('Longitud:', longitud);

 
    if (!isNaN(latitud) && !isNaN(longitud)) {
        var coord = {lat:latitud,lng:longitud};

       
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            center: coord
        });

       
        var marker = new google.maps.Marker({
            position: coord,
            map: map,
            title: "Ubicación"
        });
    } else {
        console.error("Las coordenadas no son válidas");
    }
}

window.onload = iniciarMap; 