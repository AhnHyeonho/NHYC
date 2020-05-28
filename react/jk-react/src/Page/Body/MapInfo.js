import React from 'react';

import GuListComponent from './Component/GuList';
import NowonGuListComponent from './Component/NowonGu/NowonGuList';
import './MapInfo.css';

import SeoulCityCCTV from './Component/SeoulCity/SeoulCityCCTV';
import NowonGuCCTV from './Component/NowonGu/NowonGuCCTV';
import Nowon1DongCCTV from './Component/NowonGu/Nowon1DongCCTV';



import MapSection from './Component/MapSection';
import Maps from './Component/Maps';



class MapInfo extends React.Component{
    constructor(props){
      super(props);
      this.handleChange = this.handleChange.bind(this);
      this.handleDongNum = this.handleDongNum.bind(this);

      this.state = {gu_name :'서울시 (25)' ,
                    dong_num : 0,

                    coord: [    
                      
                      /*0강남*/ [{}],
                      /*1강동*/ [{}],
                      /*2강서*/ [{}],
                      /*3강북*/ [{}],
                      /*4관악*/ [{}],
                      /*5광진*/ [{}],
                      /*6구로*/ [{}],
                      /*7금천*/ [{}],
                      
                      /*8노원*/
                      [
                      {id : '0', latitude :'37.652560' , logitude :'127.075252', zoom : '7'}, //  노원구
                      {id : '1', latitude:'37.629114' , logitude :'127.056937', zoom : '5'}, // 월계동
                      {id : '2', latitude:'37.630618' , logitude :'127.087265', zoom : '5'}, // 공릉동
                      {id : '3', latitude:'37.637873' , logitude :'127.071660', zoom : '5'}, //하계동
                      {id : '4', latitude:'37.652405' , logitude :'127.078938', zoom : '5'}, //중계동
                      {id : '5', latitude:'37.674435' , logitude :'127.060167', zoom : '5'} //상계동
                      
                      ]
                      
                    ]

                  };
    }




    handleChange(name){
      if(this.state.gu_name == name){
        this.setState({gu_name: '서울시 (25)'})
      }else{
        this.setState({gu_name: name});
      } 
    }

    handleDongNum(num){
      if(this.state.dong_num == num){
        this.setState({dong_num : 0})
      }else{
        this.setState({dong_num :num})
      }
    }

    





    render(){
      
      function ListSelect(props){
        const name = props.guName;
        if(name =='서울시 (25)'){
          return <GuListComponent handleChange = {props.handleChange}/>;
        }
        if(name == '노원구 (5)'){
          return <NowonGuListComponent handleDongNum ={props.handleDongNum} />;
        }

      }




      function CCTVSelect(props){
        const name = props.guName;
        const dongNum = props.dongNum;

        if(name =='서울시 (25)'){
          return <SeoulCityCCTV/>;
        }
        if(name == '노원구 (5)'){
          if(dongNum == 0)
            return <NowonGuCCTV/>;
          if(dongNum == 1)
            return <Nowon1DongCCTV/>;

        }
      }




      function MapSectionSelect(props){
        const name = props.guName;
        const num = props.dongNum;

        if(name =='서울시 (25)'){
          return <MapSection handleChange = {props.handleChange}/>;
        }
        if(name == '노원구 (5)'){
          return <Maps latitude={props.coord[8][num].latitude} logitude ={props.coord[8][num].logitude} zoom = {props.coord[8][num].zoom}/>;
        }

      }




        return (
          <div className="app-body-mapinfo-wrapper">
            <div className="app-body-mapinfo">

              {/* header 제목*/}
              <div className="mapinfo-header">
                <div className="header bar" />
                <div className="header Seoul">서울시</div>
                <div className="header SeoulComent">
                  월세/보증금 실거래가 평균
                </div>
              </div> {/* header 제목 끝*/}



              {/* 서울 지도 섹션*/}
              <div className="map-section-container">
                {/* 지도*/}
                <MapSectionSelect guName={this.state.gu_name} dongNum = {this.state.dong_num} handleChange = {this.handleChange} coord = {this.state.coord} />
                {/* 구 리스트 */}
                <div className="seoulMap guList">
                  <div className="guList-label">
                     <div className="guList-label-content">{this.state.gu_name}</div>
                  </div>

                  <div className="guList-container">
                    <ListSelect guName={this.state.gu_name} handleChange = {this.handleChange}  handleDongNum = {this.handleDongNum}/>
                  </div>
                </div>
              </div>
              {/* 서울 지도 섹션 끝*/}
  




              {/* 월세 가격 순위 및 추이 섹션*/}
              <div className="monthly-section-container">
               
              </div> {/* 월세 가격 순위 및 추이 섹션 끝*/}







              {/* 서울시 cctv 설치 현황 차트 */}
              <div className="cctv-section-container">
                <CCTVSelect guName ={this.state.gu_name} dongNum = {this.state.dong_num}/>            
              </div> {/*서울시 cctv 설치 현황 차트 끝*/}


            </div>
          </div>
        );
    }
}
      
export default MapInfo;