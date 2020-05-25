import React, { Component } from 'react'
import { Bar } from 'react-chartjs-2';
import './BarGraph.css'

const data = {

	labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
	datasets: [
		{
			label: 'My First dataset',
			backgroundColor: 'rgba(41,181,189,1)',
			borderColor: 'rgba(41,181,189,1)',
			borderWidth: 1,
			hoverBackgroundColor: 'rgba(41,181,189,0.4)',
			hoverBorderColor: 'rgba(41,181,189,1)',
			data: [65, 59, 80, 81, 56, 55, 40, 100]
		}
	]
};

// Bar Graph 옵션값 
var options = {
	responsive:false, // true로 바꾸면 화면에 꽉차게끔 그래프가 그려짐 (default = true)

	tooltips: {
		callbacks: {
			label: function (tooltipItem) {
				return "$" + Number(tooltipItem.yLabel) + " and so worth it !";
			}
		}
	},

	title: {
		display: true,
		text: 'Ice Cream Truck',
		position: 'bottom'
	},

	hover:{
		onHover: function (e, element) {
			console.log(e);
		}
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

	componentWillMount() {

    }

	render() {
		return (
			<div>
				<h2 className="title"><span className="line"/>  {this.props.name}</h2>
				<Bar 
					data={data}
					width="500vh" // 그래프 전체의 width 
					height={300} // 그래프 전체의 Height
					options={options}
				/>
			</div>
		);
	}

}


export default BarGraph;