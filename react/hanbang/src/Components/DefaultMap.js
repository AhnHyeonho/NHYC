/*global kakao*/
import React from 'react';
import './DefaultMap.css'

class DefaultMap extends React.Component {

    constructor(props) {
        super(props);	
    }

    componentDidMount(){
        var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
        var options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(35.157588, 129.058822), //지도의 중심좌표.
            level: 5 //지도의 레벨(확대, 축소 정도)
        };
	    var map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
        this.map = map 
    }

    render() {
        return (
            <div id='map' className='map'>
            </div>
        )
    }
}
export default DefaultMap;