
import { Radar } from "react-chartjs-2"

import React, { useState, useEffect } from 'react';
import axios from 'axios';

import "./RadarChart.css"


const radarData = {

  labels: [],
  datasets: [],
  
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
    
    console.log(datalist)

    const dataset = []

    const r = [241, 242, 188, 103, 165]
    const g = [95, 203, 229, 153, 102]
    const b = [95, 97, 92, 255, 255]

    for (let i = 0; i < 5; i++) {
      const d = datalist[i]

      // const r = generateRandom(0, 255);
      // const g = generateRandom(0, 255);
      // const b = generateRandom(0, 255);


      dataset[i] = {
        label: d.address,
        data: [d.budget, d.safety, d.life, d.culture, d.traffic],
        backgroundColor: `rgba(${r[i]}, ${g[i]}, ${b[i]}, 0.2)`,
        bolderColor: `rgba(${r[i]}, ${g[i]}, ${b[i]}, 1)`,
        pointBorderColor: `rgba(${r[i]}, ${g[i]}, ${b[i]}, 1)`,
        pointBackgrounColor: `rgba(${r[i]}, ${g[i]}, ${b[i]}, 1)`,
        pointRadius: 2,
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

        let url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/dummyData/2";

        // request
        const response = await axios.get(url);

        // request data - labels
        const responseLabels = response.data[0].labels;
        const rawData = response.data[0].status;

        console.log(rawData);


        rawData.map(data => {
          console.log("맵핑 데이터"+data)
          setStatus(status => [
            ...status, {
              address: data.address,
              budget: data.budget,
              safety: data.safety,
              life: data.life,
              culture: data.culture,
              traffic: data.traffic,
            }]
          )
        })


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


  console.log(status)
  radarData.labels = labels
  radarData.datasets = generateDatasets("localStatus")


  return (
    <div>
     
      <Radar data={radarData} options={{legend:{ display: true, position: "left"}}} />

    </div>
  )

}

