export function createMap() { 
      return new maplibregl.Map({
      style: 'https://tiles.openfreemap.org/styles/liberty',
      container: 'map',
      center: [49.8671, 40.4093],
      zoom: 13
    });
}


export function createVehicleMarker(map, lon, lat) {
  const el = document.createElement('div');
  el.className = 'vehicle-dot';
 
  const inner = document.createElement('div');
  inner.className = 'vehicle-dot-inner';
  inner.textContent = '🚌';
 
  el.appendChild(inner);
  const marker = new maplibregl.Marker({ element: el }).setLngLat([lon, lat]).addTo(map);
  return { marker, inner };
}