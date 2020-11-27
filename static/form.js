
var isMapVisible = false;

var deliveryMap;
var deliveryMarker;

var pickupMap;
var pickupMarker;



function initMap(mymap, mapId, marker, locationFieldId, confirmationFieldId) {
	mymap = L.map(mapId).setView([52.230, 21.01], 12);

	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibXNsYXBlayIsImEiOiJja2dsb3VqOTEwNTIwMnRqb3lrZDB3Y3FzIn0.Py4FiVVIH1OpX-PteW0UBg', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1,
		accessToken: 'pk.eyJ1IjoibXNsYXBlayIsImEiOiJja2dsb3VqOTEwNTIwMnRqb3lrZDB3Y3FzIn0.Py4FiVVIH1OpX-PteW0UBg'
	}).addTo(mymap);

	function onMapClick(e) {
		if (marker) {
			marker.setLatLng(e.latlng);
		} else {
			marker = L.marker(e.latlng);
			marker.addTo(mymap);
		}
		var locationField = document.getElementById(locationFieldId);

		document.getElementById(locationFieldId).value = e.latlng;
		document.getElementById(confirmationFieldId).style.visibility = "visible";
		locationField.dispatchEvent(new Event("change"));
	}

	mymap.on('click', onMapClick);

	document.getElementById(locationFieldId).addEventListener('change', function () {
        var strs1 = document.getElementById(locationFieldId).value.split(",");
        var x1 = parseFloat((strs1[0].split("("))[1]);
        var y1 = parseFloat((((strs1[1].split(")"))[0]).split(" "))[1]);
		if (marker) {
			marker.setLatLng([x1, y1]);
		} else {
			marker = L.marker([x1, y1]);
			marker.addTo(mymap);
		}
		mymap.flyTo(new L.LatLng(x1, y1), 12);
	});

}

function showPickupMap() {
  showMap("mapPickup", "mapPickupHide");
}

function showDeliveryMap() {
  showMap("mapDelivery", "mapDeliveryHide");
}

function showMap(mapId, mapHiderId) {
	if (!isMapVisible) {
		document.getElementById(mapId).style.display = "block";
		document.getElementById(mapHiderId).style.display = "block";
		isMapVisible = true;
	}
}

function hideMap(mapId, mapHiderId) {
    if (isMapVisible) {
  	  	document.getElementById(mapId).style.display = "none";
      	document.getElementById(mapHiderId).style.display = "none";
      	isMapVisible = false;
    }
}

function hidePickupMap() {
  hideMap("mapPickup", "mapPickupHide")
}

function hideDeliveryMap() {
  hideMap("mapDelivery", "mapDeliveryHide")
}

function geocode(address, city, postal, locationFieldId, confirmationFieldId, marker, map) {
	if (address && city && postal) {
		L.esri.Geocoding.geocode().address(address).city(city).postal(postal)
			.run(function (err, results, response) {
    		if (err) {
      			console.log(err);
      			window.alert("There was problem with finding given location. Enter different address or pick it on map.");
      			return;
    		}

    		var latlng = results.results[0].latlng;
			var locationField = document.getElementById(locationFieldId);
			var confirmationField = document.getElementById(confirmationFieldId);
    		locationField.value = latlng;
			confirmationField.style.visibility = "visible";
			locationField.dispatchEvent(new Event("change"));
		});
	}
}

function geocodeDelivery() {
	var address = document.getElementById("delAddress").value;
	var city = document.getElementById("delCity").value;
	var postal = document.getElementById("delZip").value;

	geocode(address, city, postal, "deliveryLocation", "deliveryMapConfirmed",
		deliveryMarker, deliveryMap);
}

function geocodePickup() {
	var address = document.getElementById("pickupAddress").value;
	var city = document.getElementById("pickupCity").value;
	var postal = document.getElementById("pickupZip").value;

	geocode(address, city, postal, "pickupLocation", "pickupMapConfirmed",
		pickupMarker, pickupMap);
}


function reverseGeocode(addressField, cityField, postalField, locationFieldId) {
	var strs1 = document.getElementById(locationFieldId).value.split(",");

	var x1 = parseFloat((strs1[0].split("("))[1]);
	var y1 = parseFloat((((strs1[1].split(")"))[0]).split(" "))[1]);
	var geocodeService = L.esri.Geocoding.geocodeService();


	geocodeService.reverse().latlng([x1, y1]).run(function (error, result) {
      	if (error) {
      		window.alert("There was problem with finding given location. Enter different address or pick it on map.");
        	return;
      	}
      	document.getElementById(addressField).value = result.address.Address;
      	document.getElementById(cityField).value = result.address.City;
      	document.getElementById(postalField).value = result.address.Postal;
	});

}

function reverseGeocodeDelivery() {
	reverseGeocode('delAddress', 'delCity', 'delZip', "deliveryLocation");
}


function reverseGeocodePickup() {
	reverseGeocode('pickupAddress', 'pickupCity', 'pickupZip', "pickupLocation");
}



window.addEventListener("load", function(){
	initMap(deliveryMap, "mapDelivery", deliveryMarker, "deliveryLocation",
		"deliveryMapConfirmed");
	initMap(pickupMap, "mapPickup", pickupMarker, "pickupLocation",
		"pickupMapConfirmed");
	document.getElementById("deliveryLocation").addEventListener(
		"change", reverseGeocodeDelivery
	);

	document.getElementById("pickupLocation").addEventListener(
		"change", reverseGeocodePickup
	);
});


