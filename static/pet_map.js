//for filter option
var markers = []

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


    // Retrieving the information with AJAX for markers
    $.get('/.json', function (lost_pets) {
      // Using information from the Json file, place makers using Lat/Lng, use correct pin for dog/cat, and populate info window
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

        const found_pin = {
            url:"/static/icons/foundPin.svg",
            scaledSize: new google.maps.Size(50,75),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(25,80)
        };

      if (animal.species_id=='Cat' && animal.found==false){ //and found == false
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: cat_icon
        })
      } else if (animal.species_id=='Cat' && animal.found==true){ //and found == false
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: found_pin
        })
      };

      if (animal.species_id=='Dog' && animal.found==false){ //and found == false
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: dog_icon
        })
      } else if (animal.species_id=='Dog' && animal.found==true){ //and found == false
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(animal.latitude, animal.longitude),
            map: map,
            title: 'Seen: ' + animal.species_id,
            animal:animal,
            icon: found_pin
        })
      };
        let found_section = ""
        let found_title = ""
        if (animal.found == true) {
            found_title = 
            '<font size="3"><center>Found ' + animal.species_id  + '</center>' 
        } else {
            found_title = 
            '<font size="3"><center>Lost ' + animal.species_id  + '</center>' 
        }

            // Define the content of the infoWindow - add individual photos to marker
            html = (
              '<div class="window-content">' +
                    found_title +
                    '<img src="/static/seed_photos/' + animal.photo + '" alt="photo" style="width:150px;" class="thumbnail">' + 
                    '<b><font size="2">Size: </b>' + animal.size_id  + '<br>' +
                    '<b>Colors: </b>' + animal.colors.join(', ') + '<br>' +
                    '<b>Time seen at: </b>' + animal.timestamp   + '<br>' + '<br>' +
                    '<b><center>Click photo for more info</b></center>' +
                    

                    // '<p><b>Seen at: </b>' + animal.seen_at_lat + ' ' + animal.seen_at_long + '</p>' +
              '</div>');

            // Inside the loop we call bindInfoWindow passing it the marker,
            // map, infoWindow and contentString
            bindInfoWindow(marker, map, infoWindow, html, animal);
            if (marker) {markers.push(marker)}
      }

    });



//Filter Checkboxes
const $filterCheckboxes = $('input[type="checkbox"]');

$filterCheckboxes.on('change', function() {

  const selectedFilters = {};
  
  $filterCheckboxes.filter(':checked').each(function() {

    if (!selectedFilters.hasOwnProperty(this.name)) {
      selectedFilters[this.name] = [];
      console.log("selectedFilters: ", selectedFilters)
    }

    if (this.value == "true") {
        console.log("made it here:true")
        console.log("value: ", this.value)
        this.value = true
    }

    if (this.value == "false") {
    console.log("made it here:false")
    console.log("value: ", this.value)
    this.value = false
    }
    

    selectedFilters[this.name].push(this.value);
    console.log("selectedFilters: ", selectedFilters)
  });

  // create a collection containing all of the filterable elements
  let filteredResults = markers.slice(); 
  console.log(markers)

  // loop over the selected filter name -> (array) values pairs
  $.each(selectedFilters, function(filterName, filterValues) {

    // filter each element
    filteredResults = filteredResults.filter(function(marker) {
        
        let markerValue = marker.animal[filterName]
        // If value is an array == True
        if (Array.isArray(markerValue)) {

            for (let filterValue of filterValues){
                if(markerValue.includes(filterValue)){
                    return true;
                }
            };
        };

        //if not an array, just check if markerValue is there by checking its index. If no index == false
        if (filterValues.indexOf(markerValue) >= 0){
            return true;
        }
    });
  });

  markers.forEach(function(marker) {
    marker.setVisible(false)
  });

  filteredResults.forEach(function(marker) {
    marker.setVisible(true)
  });
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
    function bindInfoWindow(marker, map, infoWindow, html, animal) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);

            setTimeout(function(){
                $('.window-content').on( 'click', function(){
                    $( '.moreInfo_class' ).show();

                    animal_photo = (
                        '<img src="/static/seed_photos/' + animal.photo + '"style="width:500px;">'
                    );
                    $('#animal_photo').html(animal_photo);  


                    let found_by = ""
                    if (animal.found == true) {
                        found_by = 
                        '<b>Found by: </b>' + animal.found_by_user_id + '<br>'
                    } 


                    animal_info = (
                        '<p><b>Species: </b>' + animal.species_id  + '<br>' +
                        '<b>Size: </b>' + animal.size_id  + '<br>' +
                        '<b>Colors: </b>' + animal.colors.join(', ') + '<br>' +
                        '<b>Notes: </b>' + animal.notes + '<br>' + '</p>' +
                        found_by +
                        '<p><b>Seen By: </b>' + animal.user_id + '<br>' +
                        '<b>Time seen at: </b>' + animal.timestamp +
                        '<p id="animal_id" hidden>' + animal.animal_id + '</p><br>' +
                        '<p id="found" hidden>' + animal.found + '</p><br>' 
                        );


                    $('#animal_info').html(animal_info); 

                    if (animal.found == false) {
                        $( '#found_button_div' ).show();
                        $('#found_button' ).on('click', function(evt){
                            let animal_id = $('#animal_id').html()

                            found_pet = {
                                "found_animal_id" : animal_id
                            }

                            $.post('/found_animal', found_pet, function (data) {window.location.reload()});
                        });
                    } else {
                        $( '#found_button_div' ).hide();
                    }

                    // document.getElementById("moreInfo").onclick = function() {scrollToTop()};

                    // var elmnt = document.getElementById("moreInfo");

                    // function scrollToTop() {
                    //     console.log("Im gonna scroll!")
                    //     elmnt.scrollIntoView(true); // Scroll to the top of the element
                    // }
                })
            },300);
        });
    };

    window.myMap = map
};

google.maps.event.addDomListener(window, 'load', initMap);


// Needed to run click actions
$(document).ready(function() {

// When species is chosen on lost_pets_form, the breeds are filtered to particular species 
console.log("filter dog/cat breeds ready")
$( '#dog_species' ).on( 'click', function(){
        $( '.cat_breed' ).hide();
     $( '.dog_breed' ).show();
});

$( '#cat_species' ).on( 'click', function(){
        $( '.cat_breed' ).show();
     $( '.dog_breed' ).hide();
});

// Get Lat/Long when using current location
console.log("get current location ready")
$('#current_location' ).on('click', function(){
   $( '#current_location' ).data( 'current_location' );

   console.log($('#current_location').data('current_location'))
});

// Move map to address using address bar
console.log("address bar ready")
$('#address_bar').on('submit', function(evt){
    evt.preventDefault();
    const addressValue = $('#address').val()
    const key = "googleapikey"
    const googleMapsUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${addressValue}&key=${key}`
    $.get( googleMapsUrl, function( data ) {
        var pos = data.results[0].geometry.location;

        window.myMap.setCenter(pos)

    });
});

// get information from lost pets form to database
console.log("information from lost pets form to database ready")
$('#lost_form').submit(function(e) {
    e.preventDefault();    
    $( '.submitted_form_class' ).show();
    $( '.seen_form_class' ).hide();

    var formData = new FormData(this);

    formData.set('lat', $('#current_location').data( 'current_location').lat);
    formData.set('lng', $('#current_location').data( 'current_location').lng);

    $.ajax({
        url: '/add_lost_animal',
        type: 'POST',
        data: formData,
        success: function (data) {
            window.location.reload()
        },
        cache: false,
        contentType: false,
        processData: false
    });
});


// end of document.ready function
});
