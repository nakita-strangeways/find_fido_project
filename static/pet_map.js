function initMap() {
    // Specify where the map is centered
    // Defining this variable outside of the map optios markers
    // it easier to dynamically change if you need to recenter
    // Centered on San Francisco 
    let myLatLng = {lat: 37.731304, lng: -122.433121};

    // Create a map object and specify the DOM element for display.
    let map = new google.maps.Map(document.getElementById('pet-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 17,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    // Define global infoWindow
    // If you do this inside the loop where you retrieve the json,
    // the windows do not automatically close when a new marker is clicked
    // and you end up with a bunch of windows opened at the same time.
    // What this does is create one infowindow and we replace the content
    // inside for each marker.
    let infoWindow = new google.maps.InfoWindow({
        width: 150
    });

    // Retrieving the information with AJAX
    $.get('/lost.json', function (lost_pets) {
      // Attach markers to each pet location in returned JSON
      let animal, marker, html;

      for (let key in lost_pets) {

            animal = lost_pets[key];

        const dog_icon = {
            url:"/static/icons/dog-pin.png",
            scaledSize: new google.maps.Size(50,75),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(0,0)
        };

        const cat_icon = {
            url:"/static/icons/cat-pin.png",
            scaledSize: new google.maps.Size(50,75),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(0,0)
        };

    // Define the marker - add if statement to use cat or dog pin
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.seen_at_lat, animal.seen_at_long),
            map: map,
            title: 'Seen: ' + animal.species_id,
            icon: dog_icon
        });
        
      // if (animal.species_id=='1'){
      //   marker = new google.maps.Marker({
      //       position: new google.maps.LatLng(animal.seen_at_lat, animal.seen_at_long),
      //       map: map,
      //       title: 'Seen: ' + animal.species_id,
      //       icon: cat_icon
      //   });
      // }

      // if (animal.species_id=='2'){
      //   marker = new google.maps.Marker({
      //       position: new google.maps.LatLng(animal.seen_at_lat, animal.seen_at_long),
      //       map: map,
      //       title: 'Seen: ' + animal.species_id,
      //       icon: dog_icon
      //   });
      // }

            // Define the content of the infoWindow - add individual photos to marker
            html = (
              '<div class="window-content">' +
                    '<img src="/static/seed_photos/' + animal.photo + '" alt="photo" style="width:150px;" class="thumbnail">' +
                    '<p><b>Species: </b>' + animal.species_id + '</p>' +
                    '<p><b>Size: </b>' + animal.size_id + '</p>' +
                    '<p><b>Time seen at: </b>' + animal.timestamp_seen_at + '</p>' +
                    '<p><b>Notes: </b>' + animal.notes + '</p>' +
              '</div>');


            // Inside the loop we call bindInfoWindow passing it the marker,
            // map, infoWindow and contentString
            bindInfoWindow(marker, map, infoWindow, html);
      }

    });

    // This function is outside the for loop.
    // When a marker is clicked it closes any currently open infowindows
    // Sets the content for the new marker with the content passed through
    // then it open the infoWindow with the new content on the marker that's clicked
    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initMap);
