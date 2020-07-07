import React, { Component } from 'react'
import { Bar } from 'react-chartjs-2';
import './BarGraph.css'

// 너무 많은 mousemove 때문에 최초의 mouseover만 구하기 위한 flag값 
let mouseEventFlag = true;
let mouseOverTime = 0; // 마우스 올라간 시간 저장
let mouseOutTime = 0;  // 마우스 내려온 시간 저장

		// Bar Graph 옵션값 
		var options = {
			legend: {
				display: false
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
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}]
			},

			maintainAspectRatio: true
		};




class BarGraph extends Component {

	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);

		this.state = {
			data : 'cctv'
		}
	};
	

	handleClick(e) {
		e.preventDefault();
		console.log(e.target.value);
		
		if(e.target.value == "cctv"){
			this.setState(state => ({
				data:'cctv'
			}));
		}

		if(e.target.value == "police"){
			this.setState(state => ({
				data:'police'
			}));
		}

		if(e.target.value == "light"){
			this.setState(state => ({
				data:'light'
			}));
		}
	  }




	render() {
		var dataVal;
		var dataLabel;
		var databackgroundColor;
		var databackgroundHoverColor;
		if(this.state.data == 'cctv'){
			dataVal = this.props.dataValue;
			dataLabel = "CCTV";
			databackgroundColor = "rgba(41,181,189,0.6)";
			databackgroundHoverColor = "rgba(41,181,189,0.4)";
		}

		if(this.state.data == 'police'){
			dataVal = this.props.PdataValue;
			dataLabel = "경찰서";
			databackgroundColor = "rgba(41, 88, 189, 0.6)";
			databackgroundHoverColor = "rgba(41, 88, 189,0.4)";
		}

		if(this.state.data == 'light'){
			dataVal = this.props.LdataValue;
			dataLabel = "보안등";
			databackgroundColor = "rgba(41, 189, 103, 0.6)";
			databackgroundHoverColor = "rgba(41, 189, 103, 0.4)";
		}

		

		const data = {
			// 상위 컴포넌트에서 
			labels: this.props.labelData,
			
			datasets: [
				{
					label: 'Count',
					labelColor : databackgroundColor,
					backgroundColor: databackgroundColor,
					borderColor: databackgroundColor,
					borderWidth: 1,
					hoverBackgroundColor: databackgroundHoverColor,
					
					data: dataVal // 수정 요함 
				}
			]
		};



		return (
			<div className="graph">
				<div className="graph-title">
				<span className="line" /><div className="title">{this.props.name} - {dataLabel}</div>
				<div className="btn-group-sm" role="group" aria-label="Basic example">
					<button type="button" className="btn btn-sm c" value ="cctv" onClick={this.handleClick}  >CCTV</button>
					<button type="button" className="btn btn-sm c" value ="police" onClick={this.handleClick} >경찰서</button>
					<button type="button" className="btn btn-sm c" value ="light" onClick={this.handleClick}>보안등</button>
				</div>
				</div>
                
				<Bar 
					data={data}
					options={options}
					width={1130}
					height={300}
				/>

			</div>
		);
	}
}

export default BarGraph;