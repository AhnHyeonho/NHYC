import React from 'react';
import './Recommand.css'

import KakaoMap from './KakaoMap';
import DataBoard from './DataBoard';

class Recommand extends React.Component {
    
    constructor(props){
        super(props);

        this.state = {
            lati : '',
            long : '',
        }

        this.receiveData = this.receiveData.bind(this);
    }
    
    receiveData(lat, lon){
        console.log("최상위 컴포넌트")

        this.setState({
            lati:lat,
            long:lon
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
                <KakaoMap className="kakao" latitude={this.state.lati} longitude={this.state.long} zoom={'7'} />

                <DataBoard onChange={this.receiveData} sival="zz"/>

            </div>
        )
    }
}

export default Recommand;