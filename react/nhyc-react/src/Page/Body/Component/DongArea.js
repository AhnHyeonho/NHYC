import React from 'react';
import './DongArea.css';
// import PoliceImg from '../../../Img/police.png';
// import CCTVImg from '../../../Img/cctv.png';
// import LightImg from '../../../Img/light.png';
// import BluePin from '../../../Img/bluePin.png';
// import RedPin from '../../../Img/redPin.png';
// import YellowPin from '../../../Img/yellowPin.png';

import DoughnutGraph from './DoughnutGraph';
import BarDongTotal from './BarDongTotal';


class DongArea extends React.Component{
    constructor(props){
        super(props);
        this.getCountData = this.getCountData.bind(this);

        this.state = {
            cctvCount :'',
            policeCount : '',
            lightCount : '',
            libraryCount : '',
            sportsCount : '',
            artCount : '',
            concertCount : '',
            parkCount : '',
            pharmacyCount: '',
            marketCount : '',
            busCount:'',
            subwayCount:''
            

        }
    }


    componentDidMount(){
    
        this.getCountData(this.props.name, this.props.dongName);
    
    }


    getCountData(gu,dong){


        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getMarketCnt/'+gu+'/'+dong)
        .then(res => res.json())
        .then(json => this.setState({ marketCount:json}))

        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPieChartData/'+gu+'/'+dong)
        .then(res => res.json())
        .then(json => this.setState({cctvCount:json.치안.CCTV, policeCount : json.치안.경찰시설, lightCount:json.치안.보안등,

            libraryCount:json.문화.도서관, sportsCount:json.문화.체육시설, artCount : json.문화.전시회관, concertCount:json.문화.공연장,  

            parkCount:json.생활.공원, pharmacyCount:json.생활.약국, marketCount:json.생활.시장,

            busCount:json.교통.버스, subwayCount:json.교통.지하철
        
        }))


        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getDongPoint/'+gu+'/'+dong)
        .then(res => res.json())
        .then(json => console.log(json))







    }







    

    render(){
        var guName = this.props.name;
        var dongNum = this.props.dongNum;
        var dongName = this.props.dongName;

        var Security_label = ['CCTV', '경찰시설', '보안등'];
        var Security_data = [this.state.cctvCount, this.state.policeCount, this.state.lightCount];
        var Security_color = ['#ff6b6b','#feca57','#48dbfb']


        var Life_label =['약국', '공원','마켓'];
        var Life_data = [this.state.pharmacyCount, this.state.parkCount, this.state.marketCount];
        var Life_color = ['#1dd1a1','#5f27cd','#ff9ff3']

        var Culture_label =['도서관','체육시설','박물관/미술관','공연장']
        var Culture_data=[this.state.libraryCount,this.state.sportsCount,this.state.artCount,this.state.concertCount]
        var Culture_color = ['#4169E1','#7FFF00','#F0FFF0','#FFA500']

        var Traffic_label =['버스','지하철']
        var Traffic_data=[this.state.busCount,this.state.subwayCount]
        var Traffic_color = ['#87CEFA','#FFDEAD']
        



        return(

            <div> 
                <div className="blank"></div>

             	{/* <div className="dong-show">
                    <div className="title-wrapper">
                    <span className="line_dong" /><div className="title_dong">{dongName} 시설 설치 현황</div>
                    </div>
                    <div className="card-wrapper">
                        <div className = "card1">
                            <div className = "card-background">
                                <div className="Rectangle">
                                    <p className ="texting">경찰 시설 현황</p>
                                    <img src={PoliceImg} className="policeImg"></img>
                                    <img src={BluePin} className="pinImg"></img>
                                    <div className="content1-background">
                                        <p className="content-text">전체 경찰 시설 현황</p>
                                        <p className="content-count">{this.state.policeCount}개</p>
                                    </div>
                                </div>
                            </div>
                        </div>


                        <div className = "card1">
                            <div className = "card-background">
                                <div className="Rectangle">
                                    <p className ="texting">CCTV 설치 현황</p>
                                    <img src={CCTVImg} className="policeImg"></img>
                                    <img src={RedPin} className="pinImg"></img>
                                    <div className="content1-background">
                                        <p className="content-text">총 CCTV 개수</p>
                                        <p className="content-count">{this.state.cctvCount}개</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className = "card1">
                            <div className = "card-background">
                                <div className="Rectangle">
                                    <p className ="texting">보안등 설치 현황</p>
                                    <img src={LightImg} className="policeImg"></img>
                                    <img src={YellowPin} className="pinImg"></img>
                                    <div className="content1-background">
                                        <p className="content-text">전체 보안등 개수</p>
                                        <p className="content-count">{this.state.lightCount}개</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        

                        



                    </div>
                    <div className="blank"></div>
			    </div>    */}

                <BarDongTotal guName={guName} dongName ={dongName}/>
                <div className="horizonLine-section" style={{width:'1350vw',height:'1vh'}}></div>
                <DoughnutGraph className="securityDouhnut" dongName ='보안 시설' label = {Security_label} data={Security_data} color={Security_color}/>
                <DoughnutGraph className="lifeDouhnut"  dongName ='생활 시설' label = {Life_label} data={Life_data} color={Life_color}/>
                <DoughnutGraph className="cultureDouhnut" dongName ='문화 시설' label = {Culture_label} data={Culture_data} color={Culture_color}/>
                <DoughnutGraph className="trafficDouhnut"  dongName ='교통 시설' label = {Traffic_label} data={Traffic_data} color={Traffic_color}/>

                
             </div>
        )
    }

}


export default DongArea;