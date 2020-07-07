import React, { Component } from 'react'
import { Bar } from 'react-chartjs-2';


//여기에 교통 연결하면됨


// 너무 많은 mousemove 때문에 최초의 mouseover만 구하기 위한 flag값 
let mouseEventFlag = true;
let mouseOverTime = 0; // 마우스 올라간 시간 저장
let mouseOutTime = 0;  // 마우스 내려온 시간 저장

		// Bar Graph 옵션값 
		var options = {
			legend: {
				display: true
			},

			responsive: false, // true로 바꾸면 화면에 꽉차게끔 그래프가 그려짐 (default = true)

			tooltips: {
				custom: function (tooltip) {
					// console.log(tooltip);  
					// console.log(options.title);

					// tooltip 보일 때
					if (tooltip.opacity > 0) {
						
						//console.log("Tooltip is showing");

						const date = new Date();

						// 마우스가 올라간 현재 시간 저장  
						mouseOverTime = date.getTime();

						// mouseover 한번만 인식 하도록 Flag 설정 
						mouseEventFlag = false;
					} 
					
					// tooltip 사라질 때
					else {
						//console.log("Tooltip is hidden");

						const date = new Date();

						// 마우스 내려온 현재 시간 저장
						mouseOutTime = date.getTime();
						
						// onMouseOver을 다시 인식할 수 있도록 Flag 설정 
						mouseEventFlag = true;
						
						// 마우스가 내려온시간에서 마우스가 올라간 시간을 빼서 머무른 시간 구하기 
						let trackedTime = mouseOutTime - mouseOverTime;
						console.log(options["title"]["text"]+ " Table " + trackedTime + " miliseconds");

						// 여기서 API 호출 함수 불러주면 될 듯
						// 
					}
					//return;
				},

				callbacks: { // 툴팁에 나타나는 문구 수정 해줄 수 있음
					label: function (tooltipItem) {
						return  Number(tooltipItem.yLabel)+"개";
					}
				}
			},

			title: {
				display: true,
				//text: 'Ice Cream Truck',
				position: 'bottom'
			},

			
			scales: {
				xAxes: [{
					stacked: true,
				}],
				yAxes: [{
					ticks: {
						beginAtZero: true
					},
					stacked: true
				}]
			},

			maintainAspectRatio: true
		};




class BarTraffic extends Component {

	constructor(props) {
		super(props);
		this.getTrafficDataBind = this.getTrafficDataBind.bind(this);


		this.state = {
			subwayData : [],
			busData:[]
		}

	};
	

	getTrafficDataBind(guName){
		if(this.props.name == "서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSubwayCnt/')
            .then(res => res.json())
			.then(json => this.setState({subwayData : json}))

			fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getBusCnt/')
            .then(res => res.json())
			.then(json => this.setState({busData : json}))
		}else{
			fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSubwayCnt/'+guName+'/')
            .then(res => res.json())
			.then(json => this.setState({subwayData : json}))

			fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getBusCnt/'+guName+'/')
            .then(res => res.json())
			.then(json => this.setState({busData : json}))


		}


	}


	componentDidMount(){
		this.getTrafficDataBind(this.props.name);
	}



	render() {




		const data = {
			// 상위 컴포넌트에서 
			labels: this.props.labelData,
			
			datasets: [
				{
					label: 'Bus',
					labelColor : 'rgba(255, 202, 104, 0.938)',
					backgroundColor: 'rgba(255, 202, 104, 0.938)',
					borderColor: 'rgba(248, 175, 38, 0.938)',
					borderWidth: 1,
					hoverBackgroundColor:'rgba(255, 202, 104, 0.3)',
					
					data: this.state.subwayData // 수정 요함 
				},
				{
					label: 'Subway',
					labelColor : 'rgba(179, 255, 128, 0.938)',
					backgroundColor: 'rgba(179, 255, 128, 0.938)',
					borderColor: 'rgba(130, 247, 52, 0.938)',
					borderWidth: 1,
					hoverBackgroundColor:'rgba(179, 255, 128, 0.3)',
					
					data: this.state.subwayData// 수정 요함 
				}
			]
		};



		return (
			<div className="graph">
				<div className="graph-title">
				<span className="line" /><div className="title">{this.props.name} 교통 현황 </div>   
				</div>             
				<Bar data={data} options={options} width={1130} height={300}/>
				
			</div>
		);
	}
}

export default BarTraffic;