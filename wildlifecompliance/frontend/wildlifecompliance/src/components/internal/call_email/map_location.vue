<template lang="html">
    <div class="container">
        <div id="map"></div>
    </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

module.exports = {
    data: function(){
        return {
            map: null,
            tileLayer: null,
            layers: [],
            popup: null,
        }
    },
    mounted(){
        this.initMap();
        this.initLayers();
    },
    methods: {
        onClick(e){
            this.popup
            .setLatLng(e.latlng)
            .setContent(e.latlng.toString())
            .openOn(this.map);
        },
        initMap(){
            console.log('Start initMap()');

            this.map = L.map('map').setView([-31.9505, 115.8605], 4);
            this.tileLayer = L.tileLayer(
                'https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png',
                {
                    maxZoom: 18,
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
                }
            );
            this.tileLayer.addTo(this.map);
            this.popup = L.popup();
            this.map.on('click', this.onClick);
        },
        initLayers(){

        },
    },
}
</script>

<style lang="css">
#map {
    height: 400px;
    border: solid 1px #666;
}
</style>
