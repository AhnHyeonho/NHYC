import React, { Component } from 'react'
import { Bar } from 'react-chartjs-2';
import './BarGraph.css'

// 너무 많은 mousemove 때문에 최초의 mouseover만 구하기 위한 flag값 
let mouseEventFlag = true;

let mouseOverTime = 0; // 마우스 올라간 시간 저장
let mouseOutTime = 0;  // 마우스 내려온 시간 저장

		// Bar Graph 옵션값 
		var options = {

			responsive: false, // true로 바꾸면 화면에 꽉차게끔 그래프가 그려짐 (default = true)

			tooltips: {
				custom: function (tooltip) {

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
						return "$" + Number(tooltipItem.yLabel) + " and so worth it !";
					}
				}
			},

			title: {
				display: true,
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

		// this.handlerMouseOverOut = this.handlerMouseOverOut.bind(this)
		this.state = {
			list: []
		};
	};

	
	componentWillMount() {


	}

	componentDidMount() {

		// Test API
		fetch('https://jsonplaceholder.typicode.com/posts')
			.then(res => {
				console.log(res.json()[0]['userId']);

			})
			// .then(data => title = data["0"]["title"])
			// .then(data => console.log(data))
			// .then(data => options["title"]["text"] = title)
			// .then()

	}

	render() {

		const data = {
			// 상위 컴포넌트에서 
			labels: this.props.labelData,
			// labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
			datasets: [
				{
					label: 'My First dataset',
					backgroundColor: 'rgba(41,181,189,1)',
					borderColor: 'rgba(41,181,189,1)',
					borderWidth: 1,
					hoverBackgroundColor: 'rgba(41,181,189,0.4)',
					hoverBorderColor: 'rgba(41,181,189,0)',
					data: [65, 59, 80, 81, 56, 55, 40, 100] // 수정 요함 
				}
			]
		};

		return (
			<div
				className="graph"
			>
				<div className="graph-title">
					<h2 className="title"><span className="line" />  {this.props.name}</h2>

				</div>
				<Bar
					data={data}
					options={options}
					width={500}
					height={300}
				/>
			</div>
		);
	}
}

export default BarGraph;