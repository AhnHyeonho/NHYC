/* global kakao */
import React, { useEffect } from "react";
import RecommandTable from'./RecommandTable'

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
            level: zoom
        };

        this.map = new kakao.maps.Map(container, options);
    }

    render() {
        
        return (
            <div>
                <div id='recommand-map' style={{ width: "60vw", height: "70vh", display: "inline-block", position:"relative" }}></div>

                {/* 데이터 보드 */}
                <div className="recommand-databoard">

                    {/* 데이터보드 타이틀 */}
                    <div className="recommand-databoard title">데이터 보드</div>

                    {/* 데이터보드 아이템 리스트  */}
                    {/* 1. 추천지역 리스트  */}
                    <div className="recommand-databoard list">
                        <div> 추천지역 리스트 </div>
                        <RecommandTable id="1" name="hi" id2="2" name2="hello"/>
                    </div>
                </div>
            </div>
        )
    }
}

export default KakaoMap;
