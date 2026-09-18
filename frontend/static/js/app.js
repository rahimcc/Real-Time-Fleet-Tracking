  
import { createMap, createVehicleMarker, createTrainMarker } from "./map.js";


    const m = createMap()
    const VehicleMarkers = {};  // vehicle_id -> {marker, inner}
    const TrainMarkers = {}; 

    function updateVehiclePosition(d) {
      if (!VehicleMarkers[d["vehicle-id"]]) {

       const { marker, inner , popup } = createVehicleMarker(m,d.lon,d.lat)
        console.log(marker, inner)
        VehicleMarkers[d["vehicle-id"]] = { marker, inner , popup};
       // console.log(markers)
    } 
   const { marker, inner , popup} = VehicleMarkers[d["vehicle-id"]];
     marker.setLngLat([d.lon, d.lat]);
     inner.style.transform = `rotate(${d.heading}deg)`;
     popup.setHTML(`
                <div class="vehicle-popup">
                <div class="vehicle-popup-header">🚌 ${d.vehicle_id}</div>
                <div class="vehicle-popup-row"><span>Trip</span><strong>${d.trip || '-'}</strong></div>
                <div class="vehicle-popup-row"><span>Speed</span><strong>${d.speed_kmh ?? '-'} km/h</strong></div>
                <div class="vehicle-popup-row"><span>Updated</span><strong>${new Date(d.timestamp * 1000).toLocaleTimeString()}</strong></div>
  </div>
`);
  }

  function updateTrainPosition(d) {
      console.log(d)
      if (!TrainMarkers[d.train_id]) {

       const { marker, inner , popup } = createTrainMarker(m,d.lon,d.lat)
        console.log(marker, inner)
        TrainMarkers[d.train_id] = { marker, inner , popup};
        
    }
    console.log(d.train_id)
   const { marker, inner , popup} = TrainMarkers[d.train_id];
     marker.setLngLat([d.lon, d.lat]);
     inner.style.transform = `rotate(${d.heading}deg)`;
     popup.setHTML(`
                <div class="vehicle-popup">
                <div class="vehicle-popup-header">🚌 ${d.vehicle_id}</div>
                <div class="vehicle-popup-row"><span>Trip</span><strong>${d.trip || '-'}</strong></div>
                <div class="vehicle-popup-row"><span>Speed</span><strong>${d.speed_kmh ?? '-'} km/h</strong></div>
                <div class="vehicle-popup-row"><span>Updated</span><strong>${new Date(d.timestamp * 1000).toLocaleTimeString()}</strong></div>
  </div>
`);
  }

    
  fetch('/api/vehicle/state').then(r => r.json()).then(state => {
    Object.values(state.vehicles).forEach(updateVehiclePosition);
  });
    // separate markers for start/end, distinct color from the bus
  //  const startMarker = new maplibregl.Marker({ color: '#22c55e' }); // green
  //  const endMarker = new maplibregl.Marker({ color: '#ef4444' });   // red

    const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:" ;

    const ws = new WebSocket(`${wsProtocol}//${location.host}/ws`);

    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (e) => console.log("received:", e.data);
    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("WebSocket closed");


    ws.onmessage = (event) => {
         // console.log("RAW: ", event.data)
          const msg = JSON.parse(event.data);
         // console.log(msg.data
          const data = JSON.parse(msg.data)
            if (msg.channel === "train:update") {
            console.log(data)
            updateTrainPosition(data);
             } else if (msg.channel === "vehicle:update") {
            updateVehiclePosition(data);
  }
};
      document.getElementById('speed').textContent = 100;
      document.getElementById('updated').textContent = new Date().toLocaleTimeString();