

import { Radar } from "react-chartjs-2"

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Route } from "react-router-dom";


function createData(time, route, station) {

    return { time, route, station };
}

let temp = []
const data = []

export default function RecommandTraffic(props) {

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);



    const [route, setRoute] = useState({ route: '', name: '' });
    const [route1, setRoute1] = useState({ route: '', name: '' });
    const [route2, setRoute2] = useState({ route: '', name: '' });
    const [route3, setRoute3] = useState({ route: '', name: '' });
    const [route4, setRoute4] = useState({ route: '', name: '' });




    const firstUrl = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/recommend"
    const url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getRoute"

    const config = {
        headers: {
            "memberId": "dhdh3311"
        },

    }



    const timeArrTag = [];
    let routeArrTag = null;
    let stationArrTag = null;



    let tmp = null;


    useEffect(() => {

        const fetchLabels = async () => {

            try {

                // 요청이 시작 할 때에는 error 와 users 를 초기화하고
                setError(null);

                // 추천 관련데이터 받기 전에 요청
                let res = await axios.get(firstUrl, config);
                let response = await axios.get(url, config);

                const rawData = response.data

                const resRouteArr = rawData.map(data => data.route[0]);

                tmp = resRouteArr
                // 경로 전체 들어있음
                console.log(resRouteArr)

                const timeArr = resRouteArr.map(place => place.소요시간)
                const routeArr = resRouteArr.map(place => place.경로)
                const stationArr = resRouteArr.map(place => place.역정보)


                resRouteArr.forEach(function (element, i, array) {

                    data[i] = createData(timeArr[i], routeArr[i], stationArr[i])
                });


                console.log(timeArr);
                console.log(routeArr);
                console.log(stationArr);

                setRoute({
                    time: resRouteArr[0].소요시간,
                    route: resRouteArr[0].경로,
                    station: resRouteArr[0].역정보
                })

                setRoute1({
                    time: resRouteArr[1].소요시간,
                    route: resRouteArr[1].경로,
                    station: resRouteArr[1].역정보
                })

                setRoute2({
                    time: resRouteArr[2].소요시간,
                    route: resRouteArr[2].경로,
                    station: resRouteArr[2].역정보
                })

                setRoute3({
                    time: resRouteArr[3].소요시간,
                    route: resRouteArr[3].경로,
                    station: resRouteArr[3].역정보
                })

                setRoute4({
                    time: resRouteArr[4].소요시간,
                    route: resRouteArr[4].경로,
                    station: resRouteArr[4].역정보
                })
            }
            catch (e) {
                console.log(e)
            };
        }


        fetchLabels();

    }, []);

    var listItems = data.map(function (item, index) {

        const stationInfo = item.station

        var routeArr = item.route.split("->")
        var arriveLabel = routeArr[routeArr.length-1].split("(")

        console.log(routeArr)

        return (

            <div key={index} className="traffic-section">
                <div className="traffic-subtitle-section">

                    <span className="recommand-databoard-item-subtitle2"> 추천지역 {index + 1} </span>
                    <span className="detail-comment" >{routeArr[0]} → {arriveLabel} | 소요시간 <b>{item.time}</b></span>

                    {/* 들어갈 것  */}
                    {/* <span className="detail-comment">출발지 -{'>'} 경유지 -{'>'} 도착지</span> */}

                </div>

                <div className="recommand-route">

                    {
                        <div>
                            <div><b className="traffic-bold">출발</b> {routeArr[0]}</div>
                            {
                                routeArr
                                    .slice(1, routeArr.length-1)
                                    .map((station, i) => (

                                        <div key={"trans"+i}><b key={i}>환승</b> {station}</div>
                                    ))
                            }

                            <div><b className="traffic-bold">도착</b> {routeArr[routeArr.length-1]}</div>
                            
                            <button >지도로 보기</button>
                            
                            <br />
                            <hr/>
                        </div>

                    }
                </div>
            </div>

        )
    });

    return (

        <div>



            <div className="recommand-route">

                {
                    <div>


                        {listItems}

                    </div>
                }

            </div>

        </div>
    )
}

