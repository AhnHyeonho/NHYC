import React from 'react';
import './Recommand.css'

import Maps from './KakaoMap'
import KakaoMap from './KakaoMap';

import DataBoard from './DataBoard'

class Recommand extends React.Component {
    render() {
        return (


            <div className="recommand-page container">

                {/* 타이틀 */}
                <div className="recommand-page section title">
                    <div className="decorate-bar" />
                    <span className="blank" />
                    <span className="title"> <span className="accent-name">사용자</span> <span className="blank" />님에게 적합한 거주 지역 추천</span>
                </div>

                {/* 지도 구역 감싸주는 컨테이너  */}
                <div className="recommand-page section map">

                    {/* 지도 */}
                    <KakaoMap className="recommand-page map" latitude={37.652560} logitude={127.075252} zoom={'7'}/>

                    {/* 데이터보드 */}
                    <DataBoard className="recommand-page databoard" />

                </div>

            </div>
        )
    }
}

export default Recommand;