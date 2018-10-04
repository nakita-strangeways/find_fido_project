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


// Get Lat/Long when using current location AND hides address bar if showing
console.log("get current location ready")
$('#current_location' ).on('click', function(){
   $( '#current_location' ).data( 'current_location' );
   $( '.user_entered_address' ).hide();

   console.log($('#current_location').data('current_location'))
});

// Move map to address using address bar
console.log("address bar ready")
$('#address_bar').on('submit', function(evt){
    evt.preventDefault();
    const addressValue = $('#address').val()
    const key = "GOOGLE_API_KEY"
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


// Shows address bar when not using current location
$( '#enter_location' ).on( 'click', function(){
        $( '.user_entered_address' ).show();
        console.log("Address bar showing")
});

// end of document.ready function
});


