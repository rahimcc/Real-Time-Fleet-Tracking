  
import { createMap } from "./map";



    const markers = {};  // vehicle_id -> {marker, inner}


    function upsertVehicle(d) {
      if (!markers[d["vehicle-id"]]) {
        const el = document.createElement('div');
        el.className = 'vehicle-dot';
        const inner = document.createElement('div');
        inner.className = 'vehicle-dot-inner';
        inner.textContent = '🚌';
        el.appendChild(inner);
        const marker = new maplibregl.Marker({ element: el }).setLngLat([d.lon, d.lat]).addTo(map);
        markers[d["vehicle-id"]] = { marker, inner };
       // console.log(markers)
    }
     const { marker, inner } = markers[d["vehicle-id"]];
     marker.setLngLat([d.lon, d.lat]);
     inner.style.transform = `rotate(${d.heading}deg)`;
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