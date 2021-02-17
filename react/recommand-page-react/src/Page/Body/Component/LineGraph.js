import React, { Component } from 'react'
import { Line } from 'react-chartjs-2';

import './LineGraph.css'

const data = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'september', 'october'],
    datasets: [
        {
            label: '어떤 데이터인지',
            backgroundColor: 'rgba(41,181,189, 0.3)',
            borderColor: 'rgba(41,181,189,1)',
            borderWidth: 1.5,
            lineTension: 0,
            data: [65, 59, 80, 81, 56, 55, 40, 100, 95, 80] // 수정 요함 
        }
    ],
};

const styles = {
    graphContainer: {
        border: '1px solid black',
        padding: '15px'
    }
}

class LineGraph extends Component {
    render() {
        return (
            <div className="line-graph">
                <div className="line-graph-title">
                    <h2 className="line-title"><span className="vertical-line" /> title </h2>
                </div>
                <Line data={data}
                    width={500} 
                    height={300} />
            </div>
        );
    }
}

export default LineGraph;