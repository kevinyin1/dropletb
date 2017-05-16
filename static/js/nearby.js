var geocoder;
        var map;
        var infowindow;

        function initialize() {
        geocoder = new google.maps.Geocoder();
        var loca = new google.maps.LatLng(40.7714489, -73.7832526);

        map = new google.maps.Map(document.getElementById('map'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: loca,
            zoom: 12
        });

        }

        function callback(results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
                console.log(results[i].vicinity);


            }
        }
           listnames(results, status);
        }

        function listnames(results, status){
            document.getElementById('contPlace').innerHTML = "";
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                document.getElementById('contPlace').innerHTML = "";
                for (var i = 0; i < results.length; i++) {
                    var nli = document.createElement('li');
                    nli.innerHTML = results[i].name  + '<br>' + results[i].vicinity ;
                    nli.setAttribute('class', 'list-group-item');
                    document.getElementById("contPlace").appendChild(nli);
                }
                if (document.getElementById('contPlace').innerHTML != "")
                    document.getElementById('contPlace').setAttribute('class',"outGlow")  
            }
        }

//        function printnames(results, status){
//        var x;
//        if (status == google.maps.places.PlacesServiceStatus.OK) {
//            for (var i = 0; i < results.length; i++) {
//                x[i] = results[i].name;
//            }
//        }
//        console.log(x);
//        }

        function createMarker(place) {
        var placeLoc = place.geometry.location;
        var marker = new google.maps.Marker({
            map: map,
            position: place.geometry.location
        });

        google.maps.event.addListener(marker, 'mouseover', function() {
            infowindow.setContent(place.name);
            infowindow.open(map, this);
        });
        }

        function codeAddress() {
        var address = document.getElementById("zip").value;
        geocoder.geocode({
            'address': address
        }, function(results, status) {

            if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
            var request = {
                location: results[0].geometry.location,
                radius: 5000,
                name: 'Hospital',
                keyword: 'hospital',
                type: ['hospital']
            };
            infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(map);
            service.nearbySearch(request, callback);
            } else {
            alert("Geocode was not successful for the following reason: " + status);
            }
        });
        }

        google.maps.event.addDomListener(window, 'load', initialize);

      function createMarker(place) {
        var placeLoc = place.geometry.location;
        var marker = new google.maps.Marker({
          map: map,
          position: place.geometry.location
        });

        google.maps.event.addListener(marker, 'mouseover', function() {
          infowindow.setContent(place.name);
          infowindow.open(map, this);
        });
      }

      google.maps.event.addDomListener(window, 'load', initialize);
