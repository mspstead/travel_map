function createMap(photos) {

    var mymap = L.map('mapid').setView([22, 18], 2);
    L.tileLayer('https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=5b73157d181c49b8b9ac3a6961d27e7b', {
    attribution: 'Maps &copy; <a href="https://www.thunderforest.com/">thunderforest</a> data &copy;, <a href="https://www.openstreetmap.org/copyright">OpenStreetMap Contributors</a>',
    maxZoom: 18,
    minZoom: 2,
    tileSize: 256
    }).addTo(mymap);

    var cameraIcon = L.divIcon({
        html: '<i class="fa fa-camera fa-3x"></i>'//, // size of the icon
    });

    var markerClusters = L.markerClusterGroup();

    for (var i = 0; i < photos.length; i++) {

        var url = photos[i].URL;
        var lat = photos[i].Lat;
        var lon = photos[i].Lon;
        var date = photos[i].Date;

        var markerHtml = '<a href='+url+' target="_blank" style="height:100%; width:100%"><img src='+url+'/></a><p>Time of visit:<br>'+ date +'</p>'
        var marker = L.marker([lat,lon],
            {icon: cameraIcon})
            .bindPopup(markerHtml,{Height:"50px",Width:"50px"});

        markerClusters.addLayer(marker);

    }

    mymap.addLayer(markerClusters);
}
