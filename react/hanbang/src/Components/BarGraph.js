import React, { Component } from 'react'
import {Bar} from 'react-chartjs-2';
 
const data = {
	labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
	datasets: [
	  {
		label: 'My First dataset',
		backgroundColor: 'rgba(244,98,58,1)',
		borderColor: 'rgba(244,98,58,1)',
		borderWidth: 1,
		hoverBackgroundColor: 'rgba(255,99,132,0.4)',
		hoverBorderColor: 'rgba(255,99,132,1)',
		data: [65, 59, 80, 81, 56, 55, 40]
	  }
	]
  };
  

  class BarGraph extends Component {
	render() {
		return (
		  <div>
			<h2>Bar Example (custom size)</h2>
			<Bar
			  data={data}
			  width={100}
			  height={50}
			  options={{
				maintainAspectRatio: true
			  }}
			/>
		  </div>
		);
	  }

  }


  export default BarGraph;