
import { Radar } from "react-chartjs-2"

import React, { useState, useEffect } from 'react';
import axios from 'axios';


const radarData = {

  labels: [],

  datasets: [
    {
      label: 'a',
      backgroundColor: 'rgba(255, 255, 153, 0.2)',
      borderColor: 'rgba(255, 255, 153, 1)',
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




export default function RadarChart(props) {

  const [labels, setLabels] = useState(null);
  const [values, setValues] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  useEffect(() => {

    const fetchLabels = async () => {
      try {

        // 요청이 시작 할 때에는 error 와 users 를 초기화하고
        setError(null);
        setLabels(null);

        // loading 상태를 true 로 바꿈
        setLoading(true);

        let url;

        if (props.name == "prefer") {
          url = "https://jsonplaceholder.typicode.com/users"
        }

        else if (props.name == "localStatus") {
          url = "https://jsonplaceholder.typicode.com/users"
        }

        const response = await axios.get(url);


        const responseLabels = response.data.map(resData => resData.name);
        const valuelist=response.data.map(resData=>resData.id);
        
        // console.log(valuelist);

        // let responseLabels = []
        // response.data.map((resData, index) => (
        //   responseLabels[index] = resData.name

        // ))

        setLabels(responseLabels);
        setValues(valuelist)
        // console.log(url)
        // console.log(response)

        // console.log(props.data)

      } catch (e) {
        setError(e);
      }

      setLoading(false);
    };


    fetchLabels();
  }, []);

  if (loading) return <div>로딩중..</div>;
  if (error) return <div>에러가 발생했습니다</div>;
  if (!labels) return null;

  // 데이터 삽입 
  {
    radarData.labels = labels
    radarData.datasets[0].data = values
  }

  
  return (
    <div>    

      <Radar data={radarData} />

    </div>
  )

}

