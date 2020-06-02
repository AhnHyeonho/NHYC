/*global kakao*/
import React, { Fragment } from 'react';


class Maps extends React.Component{
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
        var container = document.getElementById('myMap');
        var options={
            center : new kakao.maps.LatLng(latitude, logitude),
            level : zoom
        };
        
        this.map = new kakao.maps.Map(container,options);
    }
    
    render(){
        return( 
            <div className="seoulMap mapImg-container">
                <div id ='myMap' style={{height: "52.4vh", width:"51.8vw"}}>
                <a href="/map" style={{position:"absolute", left:"0.4em", top:"0.4em", zIndex:10}}><i className="fas fa-arrow-circle-left fa-2x" style={{color:"orangered"}}></i></a>
                </div>
            </div>

        )
    }

}

export default Maps;