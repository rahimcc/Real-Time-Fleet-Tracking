  
import { createMap, createVehicleMarker } from "./map.js";


    const m = createMap()
    const markers = {};  // vehicle_id -> {marker, inner}


    function upsertVehicle(d) {
      if (!markers[d["vehicle-id"]]) {

       const { marker, inner , popup } = createVehicleMarker(m,d.lon,d.lat)
        console.log(marker, inner)
        markers[d["vehicle-id"]] = { marker, inner , popup};
       // console.log(markers)
    } 
   const { marker, inner , popup} = markers[d["vehicle-id"]];
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
    
  fetch('/api/state').then(r => r.json()).then(state => {
    Object.values(state.vehicles).forEach(upsertVehicle);
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
         const d = JSON.parse(event.data);
         upsertVehicle(d);
         console.log(markers)
      

      document.getElementById('speed').textContent = d.speed_kmh;
      document.getElementById('updated').textContent = new Date(d.timestamp * 1000).toLocaleTimeString();
    };