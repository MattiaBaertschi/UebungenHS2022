import React from 'react';
import ReactDOMServer from 'react-dom/server';
import "./App.css";

import "leaflet/dist/leaflet.css";

import L, {Point, DivIcon} from 'leaflet';
import { MapContainer, TileLayer, Marker, Popup, Map , Polyline, Circle} from 'react-leaflet';

import marker from './data/Nuclear_symbol.svg';
//import Icon from './Icon';





function App() {

  const icon = L.divIcon({
        iconUrl: './data/Nuclear_symbol.svg',
        iconRetinaUrl: './data/Nuclear_symbol.svg',
        iconSize: new Point(80, 80),
        className: 'custom-icon',
        //html: ReactDOMServer.renderToString(<Icon perc={12}/>)
        
  });



var osm = (<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
/>)


return (
  <>
  <MapContainer center={[46.801111, 8.226667]} zoom={8} scrollWheelZoom={true}>
  {osm}
  <Circle
    center={[46.96887277, 7.268042402]}
    radius={50000}>
  </Circle>
  <Circle
    center={[47.36607556, 7.966750757]}
    radius={50000}>
  </Circle>
  <Circle
    center={[47.55201943, 8.228391684]}
    radius={50000}>
  </Circle>
  <Circle
    center={[47.60145537, 8.182823992]}
    radius={50000}>
  </Circle>
  
  
        <Marker position={[46.9688, 7.2680]} icon={icon}>
          <Popup>
            <span>
              Marker 1 <br /> Easily customizable.
            </span>
          </Popup>
        </Marker>

  <Marker position={[46.96887277, 7.268042402]}>
    <Popup>
      Mühleberg
    </Popup>
  </Marker>

  <Marker position={[47.36607556, 7.966750757]} >
    <Popup>
      Däniken
    </Popup>
  </Marker>

  <Marker position={[47.55201943, 8.228391684]}>
    <Popup>
      Döttingen
    </Popup>
  </Marker>

  <Marker position={[47.60145537, 8.182823992]}>
    <Popup>
      Leibstadt
    </Popup>
  </Marker>



</MapContainer>
</>

  );
}

export default App;