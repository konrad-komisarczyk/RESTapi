
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

		document.getElementById(locationFieldId).value = e.latlng;
		document.getElementById(confirmationFieldId).style.visibility = "visible";
	}

	mymap.on('click', onMapClick);
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

function geocode(address, city, postal, locationFieldId, confirmationFieldId, marker, mymap) {
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

			// Error here \/ says that marker and mymap are undefined, seems impossible to make it work
			// if (marker) {
			// 	marker.setLatLng(latlng);
			// } else {
			// 	marker = L.marker(latlng);
			// 	marker.addTo(mymap);
			// }

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

window.addEventListener("load", function(){
    initMap(deliveryMap, "mapDelivery", deliveryMarker, "deliveryLocation",
		"deliveryMapConfirmed");
	initMap(pickupMap, "mapPickup", pickupMarker, "pickupLocation",
		"pickupMapConfirmed");
});


