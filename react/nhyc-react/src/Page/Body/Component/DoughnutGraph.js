import React, { Component } from 'react'
import { Doughnut } from 'react-chartjs-2';
import './DoughnutGraph.css';
var options = {
    legend: {
        display: true,
        position: 'left'
    }
};


class DoughnutGraph extends Component {

    constructor(props) {
        super(props);

    };


    

    render() {

    

        
        
        const data = {
            datasets: [{
                data: this.props.data,
                backgroundColor: this.props.color,

            }],

        
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: this.props.label,

        };



        

        return (
            
            <div className="doughnutContainer">
            <div className="line-graph">
                <div className="line-graph-title">
                    <form>

                     <span className="line" /><div className="title">{this.props.dongName}</div><span></span>

                    

                    </form>


                </div>
                <Doughnut data={data}
                    width={200} 
                    height={200}
                    options = {options}/>
            </div>
            </div>
        );
    }
}

export default DoughnutGraph;