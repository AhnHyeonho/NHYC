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
        
        var guName = this.props.guName;
        var dongName = this.props.dongName;
        var zoom;

        if(dongName.trim().length==0){
            zoom = 7;
        }else{
            zoom = 5;
        }
        

        var container = document.getElementById('myMap');
        var options={
            center : new kakao.maps.LatLng(217, 34),
            level : zoom
        };
        
        this.map = new kakao.maps.Map(container,options);
        const geocoder = new kakao.maps.services.Geocoder();




        geocoder.addressSearch(guName+dongName, async (result, status) => {

                // 정상적으로 검색이 완료됐으면 
            if (status === kakao.maps.services.Status.OK) {
                var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                console.log(coords);

                var marker = new kakao.maps.Marker({
                    map: this.map,
                    position: coords
                });

                /* 
                var infowindow = new kakao.maps.InfoWindow({
                    content: '<div style="width:150px;text-align:center;padding:6px 0;">우리회사</div>'
                });
                infowindow.open(this.map, marker);
                */

                // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
                
                this.map.setCenter(coords);
            } 

        });

    }
    
    render(){
        return( 
            <div className="seoulMap mapImg-container">
                <div id ='myMap' style={{height: "52.4vh", width:"51.8vw"}}>
                <a href="/map" style={{position:"absolute", left:"0.4em", top:"0.4em", zIndex:10}}><i className="fas fa-arrow-circle-left fa-2x" style={{color:"#568fd7"}}></i></a>
                </div>
            </div>

        )
    }

}

export default Maps;