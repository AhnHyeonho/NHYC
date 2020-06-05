/* global kakao */
import React, { useEffect } from "react";
import RecommandTable from './RecommandTable'

import './KakaoMap.css'

class KakaoMap extends React.Component {

    constructor(props) {
        super(props);

    }

    map;
    markers = []
    infowindows = []

    componentDidMount() {

        var latitude = this.props.latitude;
        var logitude = this.props.logitude;
        var zoom = this.props.zoom;
        var container = document.getElementById('recommand-map');
        var options = {
            center: new kakao.maps.LatLng(latitude, logitude),
            level: zoom,
        };

        this.map = new kakao.maps.Map(container, options);
    }

    render() {

        return (
            <div id='recommand-map' style={{width: "60%", height: "70vh", position: "relative", display:"inline-block"}}></div>
        )
    }
}

export default KakaoMap;
