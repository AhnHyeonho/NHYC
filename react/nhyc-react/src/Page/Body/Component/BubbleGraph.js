import React, { Component } from 'react'
import { Bubble } from 'react-chartjs-2';


var options = {
    legend: {
        display: false
    },

    responsive: false, // true로 바꾸면 화면에 꽉차게끔 그래프가 그려짐 (default = true)

    tooltips: {


        callbacks: { // 툴팁에 나타나는 문구 수정 해줄 수 있음
            label: function (tooltipItem) {
                return  Number(tooltipItem.yLabel)+"개";
            }
        }
    },

};







class BubbleGraph extends React.Component{
    constructor(props) {
        super(props);
        this.getBubbleData = this.getBubbleData.bind(this);
        
        this.state = {
            test:[],
            data : [{x:'10', y: '20', r: '5'}]
        }
    }







    getBubbleData(guName){
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getBubbleChartData')
            .then(res => res.json())
            .then(json => this.setState({test:json}))
            

        }else{
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getBubbleChartData/'+guName)
            .then(res => res.json())
            .then(json => this.setState({test:json}))


        }

    }

    componentDidMount(){
        this.getBubbleData(this.props.name);       
    }


    
    render(){
        let newArray = [];
        let oldArray = []
        
        if(this.props.name=="서울시"){
            for(let i =0; i<this.state.test.length; i++){
           
                const d = {x:this.state.test[i][0], y:this.state.test[i][1],r:this.state.test[i][2]/1000};
               
                newArray = oldArray.concat(d); 
                 oldArray = newArray;
             }

        }else{
            for(let i =0; i<this.state.test.length; i++){
           
                const d = {x:this.state.test[i][0], y:this.state.test[i][1],r:this.state.test[i][2]/50};
               
                newArray = oldArray.concat(d); 
                 oldArray = newArray;
             }
            
        }


        
        
        var dataValue = newArray;


        const data = {
            labels: ['January'],
            datasets: [
              {
                label: 'My First dataset',
                fill: true,
                lineTension: 0.1,
                backgroundColor: 'rgba(107, 219, 140, 0.842)',
                borderColor: 'rgba(107, 219, 140,1)',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: 'rgba(83, 35, 160, 0.603)',
                pointBackgroundColor: '#fff',
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: 'rgba(83, 35, 160, 0.603))',
                pointHoverBorderColor: 'rgba(83, 35, 160, 0.603)',
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 2,
                data: dataValue
              }
            ]
          };


        return(
            <div className="graph">
                <div className="graph-title">
                    <span className="line" /><div className="title">{this.props.name}</div>
                    <Bubble data={data} options={options} width={500} height={330}/>
                </div>
            </div>
        )
    }


}



export default BubbleGraph;