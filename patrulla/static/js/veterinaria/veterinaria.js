
function iniciarMap(){
    var coord = {lat: 21.8822081,lng: -102.285564};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: coord
    });
    var marker = new google.maps.Marker({
        position:coord,
        map: map
    });
}