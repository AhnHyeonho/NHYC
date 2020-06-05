import React from 'react';
import './Recommand.css'

import KakaoMap from './KakaoMap';
import DataBoard from './DataBoard';

class Recommand extends React.Component {
    render() {
        return (

            <div className="recommand-page-container">

                {/* 타이틀 */}
                <div className="recommand-page-section-title">
                    <div className="decorate-bar" />
                    <span className="blank" />
                    <span className="title"> <span className="accent-name">사용자</span> <span className="blank" />님에게 적합한 거주 지역 추천</span>
                </div>


                {/* 카카오 맵 */}
                <KakaoMap className="kakao" latitude={37.652560} logitude={127.075252} zoom={'7'} />

                <DataBoard />

            </div>
        )
    }
}

export default Recommand;