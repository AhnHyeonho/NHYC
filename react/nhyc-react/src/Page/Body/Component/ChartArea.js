import React  from 'react';
import BarGraph from './BarGraph';
import LineGraph from './LineGraph';
import RankGraph from './TableGraph';
import BubbleGraph from './BubbleGraph';
import BarGraphC from './BarGraphC';
import BarGraphL from './BarGraphL';
import BarGraphT from './BarTraffic';



import './ChartArea.css';
import BarTraffic from './BarTraffic';

class ChartArea extends React.Component{


    constructor(props) {
        super(props);
        this.setDataBind =this.setDataBind.bind(this);
        this.setCCTVDataBind = this.setCCTVDataBind.bind(this);
        this.setPoliceDataBind = this.setPoliceDataBind.bind(this);
        this.setLightDataBind = this.setLightDataBind.bind(this);

        this.setCultureDataBind = this.setCultureDataBind.bind(this);

        this.setLifeDataBind = this.setLifeDataBind.bind(this);

        

        this.state = {
            Jlabel : [],
            cctvData : [],
            policeData : [],
            lightData : [],

            libraryData:[],
            sportsData:[],
            artData:[],
            concertData : [],

            parkData : [],
            pharmacyData : [],
            marketData : []
        }

    }

    componentDidMount(){
        if(this.props.name == "서울시"){
            this.setDataBind();
        }
       
        this.setCCTVDataBind(this.props.name);
        this.setPoliceDataBind(this.props.name);
        this.setLightDataBind(this.props.name);
        
        this.setCultureDataBind(this.props.name);
        this.setLifeDataBind(this.props.name);
        

    }










    setDataBind(){  //--->/admin/서울시 ---> getGu
        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getGu/')
        .then(res => res.json())
        .then(json => this.setState({ Jlabel :json}))
      
    }


    setCCTVDataBind(guName){  //getCCTVCnt
            if(guName =="서울시"){
                fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCCTVCnt/')
                .then(res => res.json())
                .then(json => this.setState({cctvData :json}))
            }else{
                
                fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCCTVCnt/'+guName)
                .then(res => res.json())
                .then(json => this.setState({cctvData :json}))

            }
    }

    setPoliceDataBind(guName){  
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPoliceOfficeCnt/')
            .then(res => res.json())
            .then(json => this.setState({policeData :json}))
        }else{
            
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPoliceOfficeCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({policeData :json}))

        }
    }

    setLightDataBind(guName){  
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSecurityLightCnt/')
            .then(res => res.json())
            .then(json => this.setState({lightData :json}))
        }else{
            console.log(guName)
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSecurityLightCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({lightData :json}))

        }
    }


     

    setCultureDataBind(guName){
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getLibraryCnt/')
            .then(res => res.json())
            .then(json => this.setState({libraryData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getGymCnt/')
            .then(res => res.json())
            .then(json => this.setState({sportsData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCulturalFacilityCnt/')
            .then(res => res.json())
            .then(json => this.setState({artData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getConcertHallCnt/')
            .then(res => res.json())
            .then(json => this.setState({concertData :json}))

        }else{
            console.log(guName)
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getLibraryCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({libraryData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getGymCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({sportsData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCulturalFacilityCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({artData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getConcertHallCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({concertData :json}))

        }

    }






    setLifeDataBind(guName){
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getParkCnt/')
            .then(res => res.json())
            .then(json => this.setState({parkData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPharmacyCnt/')
            .then(res => res.json())
            .then(json => this.setState({pharmacyData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getMarketCnt/')
            .then(res => res.json())
            .then(json => this.setState({marketData:json}))


        }else{
            console.log(guName)
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getParkCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({parkData :json}))
            
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPharmacyCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({pharmacyData :json}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getMarketCnt/'+guName)
            .then(res => res.json())
            .then(json => this.setState({marketData:json}))

        }
    }

    


    render() {

        var guName = this.props.name;
        var dongName = this.props.dongName;
        var label = this.props.listData;
        
        var cctvData;
        var policeData;
        var lightData;

        var libraryData;
        var sportsData;
        var artData;
        var concertData;

        var parkData;
        var pharmacyData;
        var marketData;
        
        


        if(guName == '서울시'){        
            label = this.state.Jlabel;
        }

        cctvData = this.state.cctvData;
        policeData = this.state.policeData;
        lightData = this.state.lightData;
        
        libraryData = this.state.libraryData;
        sportsData = this.state.sportsData;
        artData = this.state.artData;
        concertData = this.state.concertData;

        parkData =this.state.parkData;
        pharmacyData = this.state.pharmacyData;
        marketData = this.state.marketData;
        
        
    

        return (
            <div className="graph-area" >
                <div className="blank"></div>
                <div>
                <div className="RankChart_ChartArea"><RankGraph  name ={guName}/></div>
                <div className="middle"></div>
                <div className="BubbleChart_ChartArea"><BubbleGraph name ={guName}/></div>
                </div>

                <div className="blank"></div>
                <LineGraph name={guName}/>


                {/* 교통 데이터 연결해야함   */}
                <div className="blank"></div>
                <BarTraffic name={guName} labelData={label}/>


                <div className="blank"></div>
                <BarGraph name={ guName + " 보안 현황"} labelData={label} dataValue={cctvData} PdataValue={policeData} LdataValue={lightData}/>

                <div className="blank"></div>
                <BarGraphC name={ guName + " 문화 시설"} labelData={label} dataValue_library = {libraryData} dataValue_sports = {sportsData} dataValue_art={artData} dataValue_concert={concertData}/>
            
                <div className="blank"></div>
                <BarGraphL name={ guName + " 생활 시설"} labelData={label} parkData = {parkData} pharmacyData = {pharmacyData} marketData = {marketData}/>
            </div>
        );
    }

}

export default ChartArea;



