document.addEventListener("DOMContentLoaded", function() {
    var elements = document.getElementsByTagName("INPUT");
    for (var i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function(e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity("Wpisz poprawną wartość!");
            }
        };
        elements[i].oninput = function(e) {
            e.target.setCustomValidity("");
        };
    }
});

var isMapVisible = false;

var deliveryMap;
var deliveryMarker;
var pickupMap;
var pickupMarker;

function showPickupMap() {
  showMap(pickupMap, pickupMarker, "mapPickup", "mapPickupHide", "pickupLocation", "pickupMapConfirmed");
}

function showDeliveryMap() {
  showMap(deliveryMap, deliveryMarker, "mapDelivery", "mapDeliveryHide", "deliveryLocation", "deliveryMapConfirmed");
}


function showMap(mymap, marker, mapId, mapHiderId, locationFieldId, confirmationFieldId) {
	if (!isMapVisible) {
		// showing map div
		document.getElementById(mapId).style.display = "block";
		document.getElementById(mapHiderId).style.display = "block";
		isMapVisible = true;

		if (!mymap) {
			mymap = L.map(mapId).setView([52.230, 21.01], 12);

			L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibXNsYXBlayIsImEiOiJja2dsb3VqOTEwNTIwMnRqb3lrZDB3Y3FzIn0.Py4FiVVIH1OpX-PteW0UBg', {
				attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
				maxZoom: 18,
				id: 'mapbox/streets-v11',
				tileSize: 512,
				zoomOffset: -1,
				accessToken: 'pk.eyJ1IjoibXNsYXBlayIsImEiOiJja2dsb3VqOTEwNTIwMnRqb3lrZDB3Y3FzIn0.Py4FiVVIH1OpX-PteW0UBg'
			}).addTo(mymap);
		}

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