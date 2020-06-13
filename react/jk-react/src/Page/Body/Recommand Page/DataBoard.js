/*global kakao */
import React from 'react';

import RecommandTable from './RecommandTable';
import RadarChart from './RadarChart';
import TrafficSection from './TrafficSection';

import './DataBoard.css';



class DataBoard extends React.Component {


    constructor(props) {
        super(props)

        this.state = {
            placeName: "",
            selectedPlace: null
        };

        this.changeMap = this.changeMap.bind(this)
        this.getTrafficData = this.getTrafficData.bind(this)
    }


    changeMap(lat, lon) {
        this.props.onChange(lat, lon)
    }

    getTrafficData(data, obj){
        this.setState({
            placeName: data,
            selectedPlace: obj        
        })

        console.log(this.state.selectedPlace)
    }




    render() {

        return (

            // 데이터보드
            <div className="recommand-databoard">


                {/* 데이터보드 타이틀 */}
                <div className="recommand-databoard-title"> 데이터 보드 </div>


                {/* 데이터보드 아이템 리스트  */}
                {/* 1. 추천지역 리스트  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 추천지역 리스트 </div>
                    <RecommandTable changeMap={this.changeMap} />
                </div>

                {/* 2. 추천 지표 그래프  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 지역별 월세/보증금 및 시설 현황 </div>
                    {/* 타이틀 옆에 아이콘 추가해서 마우스 오버시 팝업으로 설명 확인할 수 있도록 하기 */}
                    <RadarChart width={500} height={500} name="localStatus" />
                </div>

                {/* 3. 추천 지표에 대한 사용자 선호도  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title" > 각 추천 지표에 대한 사용자 선호도 </div>
                    <RadarChart width={500} height={500} name="prefer" />
                </div>

                {/* 4. 대중 교통 추천 섹션 */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 추천지역 접근성 비교 </div>
                    <div className="traffic-subtitle-section">
                        <div className="decorate-bar-databoard" />
                        <span className="recommand-databoard-item-subtitle">자주가는 장소 등록</span>
                       
                        <span className="detail-comment">자주가는 장소와 추천 지역간의 교통을 한눈에 확인하세요!</span>
                    </div>

                    <div className="traffic-search-result">
                        <div className="recommand-databoard-item-subtitle">목적지 <span className="destination-label">{this.state.placeName}</span></div>
                    </div>


                    <TrafficSection getTrafficData={this.getTrafficData}/>
                    

                </div>



            </div >
        )
    }
}
export default DataBoard;