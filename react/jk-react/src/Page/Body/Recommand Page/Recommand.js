import React from 'react';
import './Recommand.css'

import KakaoMap from './KakaoMap';
import DataBoard from './DataBoard';

import axios from 'axios';

class Recommand extends React.Component {
    
    constructor(props){
        super(props);

        this.state = {
            station: null,
            name: '',
            lati: 0,
            long: 0,
            level: 7
        }

        this.receiveData = this.receiveData.bind(this);
        this.receiveStation = this.receiveStation.bind(this);

    }




    requestRecommand(){

        const url = 'http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/recommend';

        const res = axios({
            method: 'get',     //put
            url: url,
            data: ''
          });

    }

    // 테이블에서 쓰이는 함수 - 지도 위치 변경 시 
    receiveData(stationInfo, lat, lon, level){
        console.log("최상위 컴포넌트")

        console.log(level)

        this.setState({
            lati:lat,
            long:lon,
            level: level
        })

    }

    // 경로 정보 받는 함수 - 지도 보기 버튼 클릭했을 때
    receiveStation(stationInfo, departName, lat, lon, level){
        console.log("최상위 컴포넌트 - 스테이션")
        console.log(level)
        console.log(stationInfo)
        console.log(departName)
        console.log("=====")
        

        this.setState({
            station: stationInfo,
            name: departName,
            lati: lat,
            long: lon,
            level: 11
        })
    }

    render() {
        return (

            <div className="recommand-page-container">

                {/* 타이틀 */}
                <div className="recommand-page-section-title">
                    <div className="decorate-bar" />
                    <span className="blank" />
                    <span className="title"> <span className="accent-name">김다현</span> <span className="blank" />님에게 적합한 거주 지역 추천</span>
                </div>


                {/* 카카오 맵 */}
                <KakaoMap className="kakao" 
                    latitude={this.state.lati} 
                    longitude={this.state.long} 
                    zoom={this.state.level} 
                    station={this.state.station}  
                    name={this.state.name}    
                />

                <DataBoard onChange={this.receiveStation} />

            </div>
        )
    }
}

export default Recommand;