
import { Radar } from "react-chartjs-2"

import React, { useState, useEffect } from 'react';
import axios from 'axios';


const radarData = {

  // labels: ["교통", "치안", "문화", "생활", "기타"],

  options: {
    legend: {
      display: true,
      position: 'left',
    }
  },

  datasets: []



}




export default function RadarChart(props) {

  const [labels, setLabels] = useState(null);
  const [values, setValues] = useState(null);

  // 지역별 월세/보증금 및 시설 현황 차트 데이터 
  const [status, setStatus] = useState([])

  // 각 추천 지표에 대한 사용자 선호도 데이터
  const [prefer, setPrefer] = useState([])

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);



  var generateRandom = function (min, max) {
    var ranNum = Math.floor(Math.random() * (max - min + 1)) + min;
    return ranNum;
  }
  
  
  function generateDatasets(name) {
    const datalist = status;
  
    const dataset = []
    for (let i = 0; i < 5; i++) {
      const d = datalist[i]
  
  
  
      const r = generateRandom(0, 255);
      const g = generateRandom(0, 255);
      const b = generateRandom(0, 255);
  
      const r2 = generateRandom(0, 255);
      const g2 = generateRandom(0, 255);
      const b2 = generateRandom(0, 255);
  
  
      dataset[i] = {
        label: d.address,
        data: [d.trafic, d.police, d.culture, d.monthly, d.deposit],
        backgroundColor: `rgba(${r}, ${g}, ${b}, 0.2)`,
        bolderColor: `rgba(${r}, ${g}, ${b}, 1)`,
        pointBorderColor: `rgba(${r2}, ${g2}, ${b2}, 1)`,
        pointBackgrounColor: `rgba(${r2}, ${g2}, ${b2}, 1)`,
        pointRadius: 1,
      };
    }
  
    return dataset
  
  }
  
  


  useEffect(() => {

    const fetchLabels = async () => {
      try {

        // 요청이 시작 할 때에는 error 와 users 를 초기화하고
        setError(null);
        setLabels(null);

        // loading 상태를 true 로 바꿈
        setLoading(true);

        let url;


        if (props.name == "localStatus") {
          url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/dummyData/2"
        }

        else if (props.name == "prefer") {
          url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/dummyData/2"
        }


        // request
        const response = await axios.get(url);

        // request data - labels
        const responseLabels = response.data[0].labels;

        // ======= 그래프 종류에 따라 받아오는 데이터 다르게 ======

        // *** 지역별 월세/보증금 및 시설 현황 차트 ***
        if (props.name == "localStatus" || props.name == "prefer") {
          const rawData = response.data[0].status

          rawData.map(data => {
            setStatus(status => [
              ...status, {
                rank: data.rank,
                address: data.address,
                trafic: data.traffic,
                culture: data.culture,
                deposit: data.deposit,
                monthly: data.monthly,
                police: data.police
              }]
            )
          })

        }

        // *** 각 추천 지표에 대한 사용자 선호도 ***
        // else if (props.name == "prefer") {
        //   // rawData = response.data[0].dataset;
        // }

        // ======= 그래프 종류에 따라 받아오는 데이터 다르게 ======

        setLabels(responseLabels);

      } catch (e) {
        setError(e);
        console.log(e)
      }

      setLoading(false);
    };


    fetchLabels();


  }, []);


  if (loading) return <div>로딩중..</div>;
  if (error) return <div>에러가 발생했습니다</div>;
  if (!labels) return null;


  // 데이터 삽입 
  // {
  //   radarData.labels = labels
  //   radarData.datasets = generateDatasets("localStatus")
  // }

  console.log(status)
  radarData.labels = labels
  radarData.datasets = generateDatasets("localStatus")
  

  return (
    <div>

      <Radar data={radarData} />

    </div>
  )

}

