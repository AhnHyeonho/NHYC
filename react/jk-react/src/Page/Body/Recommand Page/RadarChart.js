import React from "react"
import {Radar} from "react-chartjs-2"

const radarData = {

    labels: ['보안', '월세', '보증금', '시설', 'Sp. Def', 'Speed'],

    datasets: [
      {
        label: 'a',
        backgroundColor: 'rgba(255, 255, 153, 0.2)',
        borderColor:  'rgba(255, 255, 153, 1)',
        pointBorderColor: 'rgba(255, 255, 153, 1)',
        pointBackgrounColor: 'rgba(255, 255, 153, 1)',
        pointRadius: 1,
        data: [39, 52, 43, 60, 50, 65]
      },
      {
        label: 'b',
        backgroundColor: 'rgba(255, 153, 51, 0.2)',
        borderColor: 'rgba(255, 153, 51, 1)',
        pointBorderColor: 'rgba(255, 153, 51, 1)',
        pointBackgrounColor: 'rgba(255, 153, 51, 1)',
        pointRadius: 1,
        data: [58, 64, 58, 80, 65, 80]
      },
      {
        label: 'c',
        backgroundColor: 'rgba(255, 0, 0, 0.2)',
        borderColor: 'rgba(255, 0, 0, 1)',
        pointBorderColor: 'rgba(255, 0, 0, 1)',
        pointBackgrounColor: 'rgba(255, 0, 0, 1)',
        pointRadius: 1,
        data: [78, 84, 78, 109, 85, 100]
      }
    ]

  }
  
  const RadarChart = (props) => {
  
    return (
      <div>
          <Radar data={radarData} />
      </div>
    )

  }
  
export default RadarChart;