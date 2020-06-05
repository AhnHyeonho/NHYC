import React from 'react';

import RecommandTable from './RecommandTable';
import RadarChart from './RadarChart';

import './DataBoard.css';


class DataBoard extends React.Component {
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
                    <RecommandTable id="1" name="hi" id2="2" name2="hello" />
                </div>

                {/* 2. 추천 지표 그래프  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 추천 지표 </div>
                    <RadarChart width={500} height={500}/>
                </div>

            </div >
        )
    }
}
export default DataBoard;