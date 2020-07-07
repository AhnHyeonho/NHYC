import React, { Component } from 'react'
import { Line } from 'react-chartjs-2';


import './LineGraph.css'


class LineGraph extends Component {

    constructor(props) {
        super(props);
        //this.getPriceDataBind = this.getPriceDataBind.bind(this);
        this.getRentBind = this.getRentBind.bind(this);

   

        this.state = {
            value: '6',
            priceBM : 'rent',
            data_list_RT_6 : [],
            data_list_RT_12 : [],
            data_list_DP_6 : [],
            data_list_DP_12 : [],
            dataRT_6 : [],
            dataRT_12 : [],
            dataDP_6 : [],
            dataDP_12 : []

            
        }


    };

    handleTermData = (event) =>
        this.setState({value: event.target.value});

    handleBMData = (event) =>
        this.setState({priceBM : event.target.value});



    getRentBind(guName){
        if(this.props.name == "서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/rent/6')
            .then(res => res.json())
            .then(json =>  this.setState({data_list_RT_6 : json.dateList, dataRT_6 : json.avgRentalFeeList }))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/rent/12')
            .then(res => res.json())
            .then(json =>  this.setState({data_list_RT_12 : json.dateList, dataRT_12 : json.avgRentalFeeList}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/depo/6')
            .then(res => res.json())
            .then(json =>  this.setState({data_list_DP_6 : json.dateList, dataDP_6 : json.avgDepositList }))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/depo/12')
            .then(res => res.json())
            .then(json =>  this.setState({data_list_DP_12 : json.dateList, dataDP_12 : json.avgDepositList }))

        }else{
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/rent/6/'+guName)
            .then(res => res.json())
            .then(json =>  this.setState({data_list_RT_6 : json.dateList, dataRT_6 : json.avgRentalFeeList }))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/rent/12/'+guName)
            .then(res => res.json())
            .then(json =>  this.setState({data_list_RT_12 : json.dateList, dataRT_12 : json.avgRentalFeeList}))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/depo/6/'+guName)
            .then(res => res.json())
            .then(json =>  this.setState({data_list_DP_6 : json.dateList, dataDP_6 : json.avgDepositList }))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getTrendChartData/depo/12/'+guName)
            .then(res => res.json())
            .then(json =>  this.setState({data_list_DP_12 : json.dateList, dataDP_12 : json.avgDepositList }))
        }
        
        
    }

    componentDidMount(){
        this.getRentBind(this.props.name);

    }


    


    

    render() {
        var data_result;
        var data_label;

        if(this.state.value ==6 && this.state.priceBM =='rent'){
            data_result = this.state.dataRT_6;
            data_label = this.state.data_list_RT_6;
        }
        if(this.state.value ==12 && this.state.priceBM =='rent'){
            data_result = this.state.dataRT_12;
            data_label = this.state.data_list_RT_12;
        }
        if(this.state.value ==6 && this.state.priceBM =='depo'){
            data_result = this.state.dataDP_6;
            data_label = this.state.data_list_DP_6;
        }

        if(this.state.value ==12 && this.state.priceBM =='depo'){
            data_result = this.state.dataDP_12;
            data_label = this.state.data_list_DP_12;
        }
    

        
        
        const data = {
            labels: data_label,
            datasets: [
                {
                    label: 'price',
                    backgroundColor: 'rgba(41,181,189, 0.3)',
                    borderColor: 'rgba(41,181,189,1)',
                    borderWidth: 1.5,
                    lineTension: 0,
                    data: data_result // 수정 요함 
                }
            ],
        };




        

        return (
            

            <div className="line-graph">
                <div className="line-graph-title">
                    <form>

                     <span className="line" /><div className="title">{this.props.name} 기간별 월세/보증금 가격 추이</div>

                     <select className="selection_LineGraph" onChange={this.handleTermData}>
                        <option value="6">최근 6개월</option>
                        <option value="12">최근 12개월</option>
                     </select>

                     <select className="selection_LineGraph2" onChange={this.handleBMData}>
                        <option value="rent">월세</option>
                        <option value="depo">보증금</option>
                     </select>
                    

                    </form>


                </div>
                <Line data={data}
                    width={1130} 
                    height={300} />
            </div>
        );
    }
}

export default LineGraph;