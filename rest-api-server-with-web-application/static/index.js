var ledSwitch = document.querySelector("#ledSwitch");

ledSwitch.addEventListener("change", function () {
  var objectId = this.dataset.objectid;
  var commandStatus = this.checked ? "HIGH" : "LOW";

  // data to be sent to the PUT request
  let _data = {
    status: commandStatus,
  };
  let updateSensorURL =
    "http://" + window.location.host + "/api/sensors/" + objectId;

  fetch(updateSensorURL, {
    method: "PUT",
    body: JSON.stringify(_data),
    headers: { "Content-type": "application/json; charset=UTF-8" },
  })
    .then((response) => response.json())
    .then((json) => console.log(json))
    .catch((err) => console.log(err));
});

document.querySelectorAll(".relay-switch").forEach((relaySwitch) => {
  relaySwitch.addEventListener("change", (e) => {
    var objectId = e.target.dataset.objectid;

    // data to be sent to the PUT request
    let _data = {
      values: {},
    };
    document.querySelectorAll(".relay-switch").forEach((relayPin) => {
      var key = relayPin.dataset.key;
      _data.values[key] = relayPin.checked ? "LOW" : "HIGH";
    });
    let updateSensorURL =
      "http://" + window.location.host + "/api/sensors/" + objectId;

    fetch(updateSensorURL, {
      method: "PUT",
      body: JSON.stringify(_data),
      headers: { "Content-type": "application/json; charset=UTF-8" },
    })
      .then((response) => response.json())
      .then((json) => console.log(json))
      .catch((err) => console.log(err));
  });
});

function updateSensorReadings(jsonResponse) {
  var temperature = document.querySelector("#dht-temp-value");
  var humidity = document.querySelector("#dht-humidity-value");

  console.log(jsonResponse);
  if (jsonResponse) {
    temperature.innerHTML = jsonResponse[0].readings.temperature.toFixed(2);
    humidity.innerHTML = jsonResponse[0].readings.humidity.toFixed(2);
  }
}
function retrieveDHTReadings() {
  var dhtSensorId = "dht22_1";
  var url = `/api/sensors?sensor_id=${dhtSensorId}`;
  fetch(url)
    .then((response) => response.json())
    .then((jsonResponse) => {
      updateSensorReadings(jsonResponse);
    });
}

// Continuos loop that runs evry 5 seconds to update our web page with the latest sensor readings
(function loop() {
  setTimeout(() => {
    retrieveDHTReadings();
    loop();
  }, 5000);
})();
