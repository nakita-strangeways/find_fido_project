//for filter option
var markers = []
// var filters = {Cat:false, Dog:false}


// Get map on webpage
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
        streetViewControl: false
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

        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            $('#current_location').data('current_location',pos)
 

            infoWindow.setPosition(pos);
            infoWindow.setContent('Click where you saw the animal');
            infoWindow.open(map);
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());

        }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        }

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
            anchor: new google.maps.Point(25,80)
        };

        const cat_icon = {
            url:"/static/icons/cat-pin.png",
            scaledSize: new google.maps.Size(50,75),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(25,80)
        };


      if (animal.species_id=='Cat'){
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: cat_icon
        });
      }

      if (animal.species_id=='Dog'){
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: dog_icon
        });
      }

            // Define the content of the infoWindow - add individual photos to marker
            html = (
              '<div class="window-content">' +
                    '<img src="/static/seed_photos/' + animal.photo + '" alt="photo" style="width:150px;" class="thumbnail">' +
                    '<p><b>Species: </b>' + animal.species_id  + '<br>' +
                    '<b>Size: </b>' + animal.size_id  + '<br>' +
                    '<b>Colors: </b>' + animal.colors.join(', ') + '<br>' +
                    '<b>Notes: </b>' + animal.notes + '<br>' + '</p>' +
                    '<p><b>Seen By: </b>' + animal.user_id + '<br>' +
                    '<b>Time seen at: </b>' + animal.timestamp  +
                    // '<p><b>Seen at: </b>' + animal.seen_at_lat + ' ' + animal.seen_at_long + '</p>' +
              '</div>');


            // Inside the loop we call bindInfoWindow passing it the marker,
            // map, infoWindow and contentString
            bindInfoWindow(marker, map, infoWindow, html);
            if (marker) {markers.push(marker)}
      }

    });

// Filter Form Click Events
let filtered_species = []
let filtered_colors = []
let filtered_sizes = []
let filtered_breeds = []

  //All checkbox
    $( '#speciesBox-all' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.species_id == "Cat") {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.species_id == "Cat") {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});
  //Cat checkbox
    $( '#speciesBox-cat' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.species_id == "Cat") {
                filtered_species.push(this);
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.species_id == "Cat") {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Dog checkbox
    $( '#speciesBox-dog' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.species_id == "Dog") {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.species_id == "Dog") {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});
  //Colors checkboxes
  //Black
    $( '#colorBox-black' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            console.log(marker)
            if(this.checked === true){
                if (marker.animal.colors.includes("Black")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Black")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Blue
    $( '#colorBox-blue' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Blue")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Blue")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Brown
    $( '#colorBox-brown' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Brown")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Brown")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Cream
    $( '#colorBox-cream' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Cream")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Cream")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Gray
    $( '#colorBox-gray' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Gray")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Gray")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Orange
    $( '#colorBox-orange' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Orange")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Orange")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Red
    $( '#colorBox-red' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Red")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Red")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //White
    $( '#colorBox-white' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("White")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("White")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});

  //Yellow
    $( '#colorBox-yellow' ).on( 'change', function(){
        for (i = 0; i < markers.length; i++) {
            marker = markers[i];
            if(this.checked === true){
                if (marker.animal.colors.includes("Yellow")) {
                marker.setVisible(true)
            }
            else {
                marker.setVisible(false)
            }
        }
            if(this.checked != true){
                if (marker.animal.colors.includes("Yellow")) {
                marker.setVisible(true)

            }
            else {
                marker.setVisible(true)
            }
        }
    }

});





    //drop a new marker on right click 
    let pin_on = false;
    let marker = null;

    google.maps.event.addListener(map, 'click', function(event) {
        if (marker) {
            marker.setMap(null)

        }
    

    marker = new google.maps.Marker({
        position: event.latLng, //map Coordinates where user clicked
        map: map,
        draggable:true, //set marker draggable 
        // animation: google.maps.Animation.DROP, //bounce animation
        title:"Drag me to change location!"
    });


    function updatePosition() {
        const pos = {
            lat: marker.position.lat(),
            lng: marker.position.lng() 
        };
        $('#current_location').data('current_location',pos);
        console.log($('#current_location').data('current_location'));
    };

    updatePosition();
    marker.addListener('drag', updatePosition);
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
    };
    window.myMap = map
};

google.maps.event.addDomListener(window, 'load', initMap);
