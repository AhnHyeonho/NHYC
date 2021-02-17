
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





export default function PreferRadar(props) {

    const [labels, setLabels] = useState(null);

    // 각 추천 지표에 대한 사용자 선호도 데이터
    const [prefer, setPrefer] = useState([])

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);



    var generateRandom = function (min, max) {
        var ranNum = Math.floor(Math.random() * (max - min + 1)) + min;
        return ranNum;
    }


    function generateDatasets() {
        const datalist = prefer;

        const r = 241;
        const g = 95;
        const b = 95;

        const dataset = [{
            data: [
                datalist.budget, 
                datalist.safety, 
                datalist.life, 
                datalist.culture, 
                datalist.traffic
            ],
            backgroundColor: `rgba(${r}, ${g}, ${b}, 0.3)`,
            bolderColor: `rgba(${r}, ${g}, ${b}, 1)`,
            pointBorderColor: `rgba(${r}, ${g}, ${b}, 1)`,
            pointBackgrounColor: `rgba(${r}, ${g}, ${b}, 1)`,
            pointRadius: 1,
        }];


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

                let url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/dummyData/3";

                // request
                const response = await axios.get(url);

                const responseLabels = response.data.labels
                const rawDataset = response.data.dataset[0]


                setPrefer({

                    budget: rawDataset.budget,
                    safety: rawDataset.safety,
                    life: rawDataset.life,
                    culture: rawDataset.culture,
                    traffic: rawDataset.traffic

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


    radarData.labels = labels
    radarData.datasets = generateDatasets()

    return (
        <div>

            <Radar data={radarData} options={{legend:{ display: false }}} />

        </div>
    )

}

