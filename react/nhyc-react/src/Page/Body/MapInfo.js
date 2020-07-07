import React from 'react';

import GuListComponent from './Component/GuList';
import DGuListComponent from './Component/GuList/DGuList';
import './MapInfo.css';


import ChartArea from './Component/ChartArea';
import DongArea from './Component/DongArea';

import MapSection from './Component/MapSection';
import Maps from './Component/Maps';

import Header from '../Header';

class MapInfo extends React.Component{
    constructor(props){
      super(props);
      this.handleChange = this.handleChange.bind(this);
      this.handleDongNum = this.handleDongNum.bind(this);
      
      this.setGuDataBind = this.setGuDataBind.bind(this);

      this.state = {gu_name :'서울시' ,
                    dong_num : 0,
                    dong_name : ' ',
                    Jlabel : []


                  };
    }


    /*여기부터  /test/ ----- /getDong/구이름*/
    /* 강남구 노원구 등 구의 포함된 동 리스트 받아오는 메소드 */
    setGuDataBind(guName){
        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getDong/'+guName+'/')
        .then(res => res.json())
        .then(json => this.setState({ Jlabel :json}))
        console.log(1)
    }

    /*여기까지*/





    handleChange(name){
      if(this.state.gu_name == name){
        this.setState({gu_name: '서울시'})
      }else{
        this.setState({gu_name: name});
        this.setGuDataBind(name);
      } 
    }


    handleDongNum(num,dongName){
      if(this.state.dong_num == num){
        this.setState({dong_num : 0});
        this.setState({dong_name: ' '});
      }else{
        this.setState({dong_num :num})
        this.setState({dong_name : dongName})
      }
    }





    render(){



      
      function ListSelect(props){
        const name = props.guName;
        if(name =='서울시'){
          return <GuListComponent handleChange = {props.handleChange} guName = {props.guName} />;
        }
        else{
          return <DGuListComponent handleDongNum ={props.handleDongNum} listData={props.listData} />;
        }

      }




      function ChartSelect(props){
        const name = props.guName;
        const dongNum = props.dongNum;
        
        
        if(name =='서울시'){
          return <ChartArea name = {props.guName}/>
        }else{
          if(dongNum == 0){
            return <ChartArea name = {props.guName} dongName ={props.dongName} listData={props.listData}/> 
          }else{
            return <DongArea name = {props.guName} dongNum={props.dongNum} dongName ={props.dongName}/>   
          }
            
        }
      }




      function MapSectionSelect(props){
        const name = props.guName;
        
        if(name =='서울시'){
          return <MapSection handleChange = {props.handleChange}/>;
        }else{
          return <Maps guName = {props.guName} dongName={props.dongName}/>;
        }

      }





        return (
          <div>
          <div className = "App-Header">
            <Header />
          </div>
          <div className="app-body-mapinfo-wrapper" >
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
                <MapSectionSelect guName={this.state.gu_name} dongNum = {this.state.dong_num} dongName={this.state.dong_name} handleChange = {this.handleChange} />
                {/* 구 리스트 */}
                <div className="seoulMap guList">
                  <div className="guList-label">
                     <div className="guList-label-content">{this.state.gu_name}</div>
                  </div>

                  <div className="guList-container">
                    <ListSelect guName={this.state.gu_name} handleChange = {this.handleChange}  handleDongNum = {this.handleDongNum} listData={this.state.Jlabel}/>
                  </div>
                </div>
              </div>
              {/* 서울 지도 섹션 끝*/}
  



              {/* 서울시 cctv 설치 현황 차트 */}
              <div className="chart-section-container">
                <ChartSelect guName ={this.state.gu_name} dongNum = {this.state.dong_num} dongName={this.state.dong_name} listData={this.state.Jlabel}/>
              </div> {/*서울시 cctv 설치 현황 차트 끝*/}







            </div>
          </div>
          </div>
          
        );
    }
}






      
export default MapInfo;