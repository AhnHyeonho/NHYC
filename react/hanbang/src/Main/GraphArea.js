import React, { Component } from 'react'
import './GraphArea.css'

class GraphArea extends Component {

    constructor(props) {
        super(props);

        this.state = {
            // state attribute 추가 
        }
    }

    render() {

        const 
        switch(this.props.name){
            case "gu": 
            
        }

        if(this.props.name=="gu"){

        }

        const seoulGu = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구','금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구'];

        return (
            <div className="graph-area" >
                <BarGraph name="서울시 면적당 CCTV 설치 현황" labelData={seoulGu} />
                <BarGraph name="서울시 경찰서 / 파출소 / 지구대 현황" labelData={seoulGu} />
                <BarGraph name="서울시 가로등 설치 현황" labelData={seoulGu} />
            </div>
        );
    }
}

export default GraphArea;


