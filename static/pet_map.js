//for filter option
var markers = []

// Get map on webpage
function initMap() {
  // Specify where the map is centered
  // Defining this variable outside of the map optios markers
  // it easier to dynamically change if you need to recenter
  // Centered on San Francisco 
  let myLatLng = {lat: 37.728648, lng: -122.430740};

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

  //Assigning keys to ajax information
  for (let key in lost_pets) {
        animal = lost_pets[key];

  //Assigning variables to my pin icons for easy use
  let dog_icon = {
      url:"/static/icons/dog-pin.png",
      scaledSize: new google.maps.Size(50,75),
      origin: new google.maps.Point(0,0),
      anchor: new google.maps.Point(25,80)
  };

  let cat_icon = {
      url:"/static/icons/cat-pin.png",
      scaledSize: new google.maps.Size(50,75),
      origin: new google.maps.Point(0,0),
      anchor: new google.maps.Point(25,80)
  };

  let found_pin = {
      url:"/static/icons/found_pin.png",
      scaledSize: new google.maps.Size(45,60),
      origin: new google.maps.Point(0,0),
      anchor: new google.maps.Point(15,70)
  };

  //Making the markers with if statments to assign correct icons
  if (animal.species_id=='Cat' && animal.found==false){ 
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(animal.latitude, animal.longitude),
        map: map,
        title: 'Seen: ' + animal.species_id,
        animal:animal,
        icon: cat_icon
    })
  } else if (animal.species_id=='Cat' && animal.found==true){ 
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(animal.latitude, animal.longitude),
        map: map,
        title: 'Seen: ' + animal.species_id,
        animal:animal,
        icon: found_pin
    })
  };

  if (animal.species_id=='Dog' && animal.found==false){ 
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(animal.latitude, animal.longitude),
        map: map,
        title: 'Seen: ' + animal.species_id,
        animal:animal,
        icon: dog_icon
    })
  } else if (animal.species_id=='Dog' && animal.found==true){ 
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(animal.latitude, animal.longitude),
        map: map,
        title: 'Seen: ' + animal.species_id,
        animal:animal,
        icon: found_pin
    })
  };

  //Filling in Window with HTML information using data from Ajax call
  let found_section = ""
  let found_title = ""
  if (animal.found == true) {
    found_title = 
    '<font size="3"><center>Returned Home: ' + animal.species_id  + '</center>' 
  } else {
    found_title = 
    '<font size="3"><center>Lost ' + animal.species_id  + '</center>' 
  }

  // Define the content of the infoWindow - add individual photos to marker
  html = (
    '<div class="window-content" style="cursor: pointer;">' +
    found_title +
    '<img src="/static/seed_photos/' + animal.photo + '" alt="photo" style="width:150px;" class="thumbnail">' + 
    '<b><font size="2">Size: </b>' + animal.size_id  + '<br>' +
    '<b>Colors: </b>' + animal.colors.join(', ') + '<br>' +
    '<b>Time seen at: </b>' + animal.timestamp   + '<br>' + '<br>' +
    '<b><center>Click photo for more info</b></center>' +
    '</div>');

  // Inside the loop we call bindInfoWindow passing it the marker,
  // map, infoWindow and contentString
  bindInfoWindow(marker, map, infoWindow, html, animal);
  if (marker) {markers.push(marker)}

  } // end of Assigning keys to ajax information
  }); // end of Retrieving the information with AJAX for markers



//Filter Checkboxes
const $filterCheckboxes = $('input[type="checkbox"]');
$filterCheckboxes.on('change', function() {

  const selectedFilters = {};
  $filterCheckboxes.filter(':checked').each(function() {

    if (!selectedFilters.hasOwnProperty(this.name)) {
      selectedFilters[this.name] = [];
    }

    if (this.value == "true") {
      this.value = true
    }

    if (this.value == "false") {
      this.value = false
    }
    
    selectedFilters[this.name].push(this.value);
  });

  // create a collection containing all of the filterable elements
  let filteredResults = markers.slice(); 

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
      if (filterValues.indexOf(String(markerValue)) >= 0){
        return true;
      }
    });
  }); // end of loop over the selected filter name -> (array) values pairs

  markers.forEach(function(marker) {
    marker.setVisible(false)
  });

  filteredResults.forEach(function(marker) {
    marker.setVisible(true)
  });
  }); //end of Filter Checkboxes

  //drop a new marker on right click 
  let pin_on = false;
  let marker = null;

  google.maps.event.addListener(map, 'click', function(event) {
    if (marker) {
      marker.setMap(null)
    }

    // GET DRAWER TO OPEN WHEN YOU CLICK MAP
    if($('#seen_form_div').hasClass("my-hide")){
      $('#seen_form_div').toggleClass("my-hide")
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
    };

  updatePosition();
  marker.addListener('drag', updatePosition);
  }); //End of drop a new marker on right click 

  //This holds the Modal for more information!
  function bindInfoWindow(marker, map, infoWindow, html, animal) {
    google.maps.event.addListener(marker, 'click', function () {
      infoWindow.close();
      infoWindow.setContent(html);
      infoWindow.open(map, marker);


    setTimeout(function(){
      $('.window-content').on( 'click', function(){

        // Does the modal thing for my map markers
        var modal = document.getElementById('myModal');

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks the button, open the modal 
        modal.style.display = "block";

        animal_photo = (
            '<img src="/static/seed_photos/' + animal.photo + '"style="width:400px; max-height: 500px;">'
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
          '<b>Assumed Breed: </b>' + animal.breed_id + '<br>' +
          '<b>Colors: </b>' + animal.colors.join(', ') + '<br>' +
          '<b>Notes: </b>' + animal.notes + '<br>' + '</p>' +
          found_by +
          '<p><b>Seen By: </b>' + animal.user_id + '<br>' +
          '<b>Time seen at: </b>' + animal.timestamp +
          '<p id="animal_id" hidden>' + animal.animal_id + '</p><br>' +
          '<p id="found" hidden>' + animal.found + '</p><br>' 
          );
        $('#seen_animals_modal_html').html(animal_info); 

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
          $(".map_filter_button").attr("disabled",false)
          $(".animal_form_drawer-button").attr("disabled",false)
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.display = "none";
            $(".map_filter_button").attr("disabled",false)
            $(".animal_form_drawer-button").attr("disabled",false)
            $('#seen_form_div').toggleClass("my-hide")
            $('#filter_form_container').toggleClass("my-hide")
          }
        }

        $(".map_filter_button").attr("disabled",true)
        $(".animal_form_drawer-button").attr("disabled",true)


        if($('#seen_form_div').hasClass("my-hide") == false){
        $('#seen_form_div').toggleClass("my-hide")
        }

        if($('#filter_form_container').hasClass("my-hide") == false){
        $('#filter_form_container').toggleClass("my-hide")
        }
      }); // End of window content function - start line 
    },300); // this is the end of the setTimeout fuction - start line 260
    }); //end of google maps listener - start line 254
  }; // End of the Modal for more information - start line 253

  window.myMap = map

};
google.maps.event.addDomListener(window, 'load', initMap);


// Needed to run click actions
$(document).ready(function() {

// When species is chosen on lost_pets_form, the breeds are filtered to particular species 
$( '#dog_species' ).on( 'click', function(){
  $( '.cat_breed' ).hide();
  $( '.dog_breed' ).show();
});

$( '#cat_species' ).on( 'click', function(){
  $( '.cat_breed' ).show();
  $( '.dog_breed' ).hide();
});

// sorts breeds list on missing pet posters page
$('#species_select').change(function() {
  if ($(this).val() === '1') {
      $( '.cat_breed' ).show();
      $( '.dog_breed' ).hide();
  } else {
      $( '.cat_breed' ).hide();
      $( '.dog_breed' ).show();        
  }
});

// Get Lat/Long when using current location
$('#current_location' ).on('click', function(){
  $( '#current_location' ).data( 'current_location' );
});

// Move map to address using address bar
$('#submit_lost_poster_form').on('submit', function(evt){
  evt.preventDefault();
  var formData = new FormData(this); 
  const addressValue = $('#address').val()
  const key = "AIzaSyD52RrA9gfZqgo8twZNm92r0bxMIT9poR4"
  const googleMapsUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${addressValue}&key=${key}`
  $.get( googleMapsUrl, function( data ) {
    var pos = data.results[0].geometry.location;
    formData.set('lat', pos.lat);
    formData.set('lng', pos.lng);

    $.ajax({
      url: '/lost_poster_form',
      type: 'POST',
      data: formData,
      success: function (data){
          window.location="/lost_pet_posters"
      },
      cache: false,
      contentType: false,
      processData: false
    }); //end of ajax - start line 384
  }); // end of google get function - start line 377
}); // end of submit lost poster form fuction - start line 369

//Makes address bar work
$('#address_bar').on('submit', function(evt){
  evt.preventDefault();
  const addressValue = $('#address').val()
  const key = "AIzaSyD52RrA9gfZqgo8twZNm92r0bxMIT9poR4"
  const googleMapsUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${addressValue}&key=${key}`
  $.get( googleMapsUrl, function( data ) {
    var pos = data.results[0].geometry.location;
    window.myMap.setCenter(pos)
  });
}); // end of address bar fuction - start line 397

// get information from lost pets form to database
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
}); // end of get information from lost pets form function - start line 407

//Ajax calls all the lost pets info to be used on missing pet posters
$.get('/lost_pet_posters.json', function (missing_pet) {
  // Does the modal thing for my pet posters
  let pet ;
  for (let key in missing_pet) {
        pet = missing_pet[key];
  }

  $( "#pet_posters" ).on("click",'.pet-list', function(evt) {
    // Get the modal
    pet = missing_pet[this.id]
    let modal = document.getElementById('myModal');

    // Get the <span> element that closes the modal
    let span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal 
    modal.style.display = "block";

    pet_photo = (
        '<img src="/static/seed_photos/' + pet.photo + '"style="width: 400px;">'
    );
    $('#pet_photo').html(pet_photo); 

    pet_info = (
    '<b>PetID: </b>' + pet.pet_id  + '<br>' +
    '<b>Name: </b>' + pet.pet_name + '<br>' +
    '<b>Breed: </b>' + pet.breed_id + '<br>' +
    '<b>Colors: </b>' + pet.colors.join(', ') + '<br>' +
    '<b>Notes: </b>' + pet.notes + '<br>' + 
    '<b>Owner: </b>' + pet.user_id + '<br>' +
    '<b>Missing Since: </b>' + pet.date_lost + '<br>'
    );

    $('#lost_pet_modal_html').html(pet_info);

    // let pet_lat = pet.latitude
    // let pet_lng = pet.longitude
    let map;
    function initMap() {
      map = new google.maps.Map(document.getElementById('lost_pet_mapbox'), {
        center: new google.maps.LatLng(pet.latitude, pet.longitude),
        zoom: 17
      });
    }
    initMap()

    let dog_icon = {
      url:"/static/icons/dog-pin.png",
      scaledSize: new google.maps.Size(50,75),
      origin: new google.maps.Point(0,0),
      anchor: new google.maps.Point(25,80)
    };

    let cat_icon = {
      url:"/static/icons/cat-pin.png",
      scaledSize: new google.maps.Size(50,75),
      origin: new google.maps.Point(0,0),
      anchor: new google.maps.Point(25,80)
    };

    if (pet.species_id=='Cat'){ 
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(pet.latitude, pet.longitude),
        map: map,
        title: 'Last Seen Here',
        icon: cat_icon
      })
    }

    if (pet.species_id=='Dog'){ 
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(pet.latitude, pet.longitude),
        map: map,
        title: 'Last Seen Here',
        icon: dog_icon
      })
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
    }
  }); // end of pet posters modal - start line 438
}); // end of Ajax calls all the lost pets info + modal function - start line 431

// Sends search bar selections to server.py to reload posters
$('#searchBar_btn').click(function(e){
  e.preventDefault();   
  $.ajax({
    data: $('#search_pet_posters').serialize(),
    url: "/lost_pet_posters_searchbox",
    type: "POST",
    success: function(resp){
        $('#pet_posters').html(resp.data)
    }
  })
});

// Sends data from seen pet modal page to datatables and updates found to true
$('.found_button_class').click(function(e) {
  e.preventDefault();    
  let found_animal = document.querySelector('#animal_id')

  $.ajax({
      url: '/found_animal',
      headers: {
          "Content-Type":"application/json"
      },
      type: 'POST',
      data: JSON.stringify({'found_animal_id': found_animal.innerHTML}),
          success: function (data) {
          window.location.reload()
      },
      cache: false,
      contentType: false,
      processData: false
  }); // end of ajax call
}); // end of found button function - start line 537


// TO DO LATER!!!
// Finds zipcode from Lat/Long of Pet Posters Page
// console.log("Find Zipcode Ready")
// $('#address_bar').on('submit', function(evt){
//     evt.preventDefault();
//     const addressValue = $('#address').val()
//     const key = "AIzaSyD52RrA9gfZqgo8twZNm92r0bxMIT9poR4"
//     const googleMapsUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${addressValue}&key=${key}`
//     $.get( googleMapsUrl, function( data ) {
//         var pos = data.results[0].geometry.location;

//         window.myMap.setCenter(pos)

//     });
// });

// form drawer on homepage TOGGLE HORIZONTALLY 
$('#seen_form_drawer-button').on('click', function(target){
    $('#seen_form_div').toggleClass("my-hide")
});

// map filter on homepage TOGGLE HORIZONTALLY 
$('#map_filter_drawer').on('click', function(target){
    $('#filter_form_container').toggleClass("my-hide")
});

}); // end of document.ready function - start line 337
