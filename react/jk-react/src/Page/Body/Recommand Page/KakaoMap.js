/* global kakao */
import React, { useEffect } from "react";

class KakaoMap extends React.Component{
    constructor(props){
        super(props);
        
    }

    map;
    markers = []
    infowindows = []

    componentDidMount(){
        
        var latitude = this.props.latitude;
        var logitude = this.props.logitude;
        var zoom = this.props.zoom;
        var container = document.getElementById('recommand-map');
        var options={
            center : new kakao.maps.LatLng(latitude, logitude),
            level : zoom
        };
        
        this.map = new kakao.maps.Map(container,options);
    }
    
    render(){
        return( 
                <div id ='recommand-map' style={{width:"60vw",height: "70vh"}}></div>
        )
    }

}

export default KakaoMap;
