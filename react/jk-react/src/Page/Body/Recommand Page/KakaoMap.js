/* global kakao */
import React, { useEffect } from "react";
import RecommandTable from './RecommandTable'

import './KakaoMap.css'



class KakaoMap extends React.Component {
    
    constructor(props) {
        super(props);
        this.state={
            lat:0,
            lon:0
        }
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
            center: new kakao.maps.LatLng(37.579424, 126.984057),
            level: zoom,
        };

        this.map = new kakao.maps.Map(container, options);

        
    }


    setCenter() {            
        // 이동할 위도 경도 위치를 생성합니다 
        var moveLatLon = new kakao.maps.LatLng(this.props.latitude, this.props.longitude);
        
        // 지도 중심을 이동 시킵니다
        this.map.setCenter(moveLatLon);
    }

    componentDidUpdate(){

        console.log(this.props.longitude)

        this.setCenter()

    }

    render() {

        return (
            <div id='recommand-map' style={{width: "65%", height: "70vh", position: "relative", display:"inline-block"}}>
            </div>
        )
    }

}

export default KakaoMap;
