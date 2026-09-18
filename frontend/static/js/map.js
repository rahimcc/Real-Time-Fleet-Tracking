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

  const popup = new maplibregl.Popup({offset: 20, closeButton: true })

  const marker = new maplibregl.Marker({ element: el })
                .setLngLat([lon, lat])
                .setPopup(popup)
                .addTo(map);
  return { marker, inner, popup };
}


export function createTrainMarker(map, lon, lat) {
  const trainEl = document.createElement('div');
  trainEl.className = 'train-marker'
  
  const inner = document.createElement('img');
  inner.className = 'train-icon';
  inner.src = '/static/css/train.png';

  trainEl.appendChild(inner);
  

  const popup = new maplibregl.Popup({offset: 20, closeButton: true })

  const marker = new maplibregl.Marker({ element: trainEl })
                .setLngLat([lon, lat])
                .setPopup(popup)
                .addTo(map);
  return { marker, inner, popup };
}