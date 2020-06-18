/* global kakao */
import React, { useEffect } from "react";
import RecommandTable from './RecommandTable'

import './KakaoMap.css'



class KakaoMap extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            lat: props.latitude,
            lon: props.longitude,
            level: props.level,
            name: props.name
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



    setCenter(map, obj) {
        map.setLevel(8)
        // 이동할 위도 경도 위치를 생성합니다 
        var moveLatLon = new kakao.maps.LatLng(this.props.latitude, this.props.longitude);

  
        if (obj.station) {
            // 시작
            var iwContent = '<div style="padding:5px;">' + obj.name + '</div>', // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
                iwPosition = new kakao.maps.LatLng(obj.station[0][0], obj.station[0][1]), //인포윈도우 표시 위치입니다
                iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

            // 인포윈도우를 생성하고 지도에 표시합니다
            var infowindow = new kakao.maps.InfoWindow({
                map: map, // 인포윈도우가 표시될 지도
                position: iwPosition,
                content: iwContent,
                removable: iwRemoveable
            });

            // 지도 중심을 이동 시킵니다
            this.map.setCenter(moveLatLon);


            console.log(obj.station)

            var linePath = obj.station.map(data => (new kakao.maps.LatLng(data[0], data[1])))


            // // 지도에 표시할 선을 생성합니다
            var polyline = new kakao.maps.Polyline({
                path: linePath, // 선을 구성하는 좌표배열 입니다
                strokeWeight: 5, // 선의 두께 입니다
                strokeColor: '#FF0000', // 선의 색깔입니다
                strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
                strokeStyle: 'solid' // 선의 스타일입니다
            });

            // // 지도에 선을 표시합니다 
            polyline.setMap(map);


            // var depart  = new kakao.maps.LatLng(obj.station[0][0], obj.station[0][1]); 

            // // 마커를 생성합니다
            // var departMarker = new kakao.maps.Marker({
            //     position: depart
            // });

            // // 마커가 지도 위에 표시되도록 설정합니다
            // departMarker.setMap(map);


            var arrive = new kakao.maps.LatLng(obj.station[obj.station.length - 1][0], obj.station[obj.station.length - 1][1]);

            // 마커를 생성합니다
            var arriveMarker = new kakao.maps.Marker({
                position: arrive
            });

            // 마커가 지도 위에 표시되도록 설정합니다
            arriveMarker.setMap(map);

        }


    }

    componentDidUpdate() {
        console.log(this.props.station)

        this.setCenter(this.map, this.props)
    }

    render() {

        return (
            <div id='recommand-map' style={{ width: "65%", height: "70vh", position: "relative", display: "inline-block" }}></div>
        )
    }

}

export default KakaoMap;
