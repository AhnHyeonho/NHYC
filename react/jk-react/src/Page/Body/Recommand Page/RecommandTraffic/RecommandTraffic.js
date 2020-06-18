

import { Radar } from "react-chartjs-2"

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Route } from "react-router-dom";
import './RecommandTraffic.css'

const dummy =
    [{"rank": 1, "route": [{"소요시간": "1시간 28분", "경로": "서초구 내곡동 -> 741번, 452번, 440번(서울특별시어린이병원.강동-송파예비군 ~ 신분당선강남역) -> 수도권2호선(강남 ~ 구로디지털단지) -> 51(대원아파트.구로디지털단지역환승센터)번, 1(숲속마을3.5단지.구로디지털단지역환승센터)번(구로디지털단지역환승센터 ~ 석수역) -> 보안등", "역정보": [{"type":
"walk", "name": "서초구 내곡동", "번호": "도보", "위도": 37.4581, "경도": 127.07668}, {"type": "bus", "name": "서울특별시어린이병원.강동-송파예비군",
"번호": "741번, 452번, 440번", "위도": 37.457611, "경도": 127.071669}, {"type": "walk", "name": "신분당선강남역", "번호": "도보", "위도":
37.494853, "경도": 127.029129}, {"type": "subway", "name": "강남", "번호": "수도권 2호선", "위도": 37.497949, "경도": 127.02763},
{"type": "walk", "name": "구로디지털단지", "번호": "도보", "위도": 37.485258, "경도": 126.90148}, {"type": "bus", "name":
"구로디지털단지역환승센터", "번호": "51(대원아파트.구로디지털단지역환승센터)번, 1(숲속마을3.5단지.구로디지털단지역환승센터)번", "위도": 37.484686, "경도": 126.902042},
{"type": "walk", "name": "석수역", "번호": "도보", "위도": 37.434894, "경도": 126.903041}, {"type": "end", "name": "보안등", "호선":
"도착", "위도": 37.43395234, "경도": 126.9064444}]}]}, {"rank": 2, "route": [{"소요시간": "1시간 33분", "경로": "강남구 세곡동 -> 강남06번,강남06-1번(대왕초등학교 ~ 수서역5번출구.이마트앞) -> 수도권 분당선(수서 ~ 선릉) -> 수도권 2호선(선릉 ~ 구로디지털단지) -> 51(대원아파트.구로디지털단지역환승센터)번,1(숲속마을3.5단지.구로디지털단지역환승센터)번(구로디지털단지역환승센터 ~ 석수역) -> 보안등", "역정보": [{"type": "walk", "name": "강남구 세곡동", "번호": "도보", "위도":
37.46436, "경도": 127.1046}, {"type": "bus", "name": "대왕초등학교", "번호": "강남06번, 강남06-1번", "위도": 37.464725, "경도": 127.106104},
{"type": "walk", "name": "수서역5번출구.이마트앞", "번호": "도보", "위도": 37.486855, "경도": 127.102551}, {"type": "subway", "name":
"수서", "번호": "수도권 분당선", "위도": 37.487727, "경도": 127.101161}, {"type": "walk", "name": "선릉", "번호": "도보", "위도": 37.504907,
"경도": 127.048814}, {"type": "subway", "name": "선릉", "번호": "수도권 2호선", "위도": 37.504484, "경도": 127.048955}, {"type":
"walk", "name": "구로디지털단지", "번호": "도보", "위도": 37.485258, "경도": 126.90148}, {"type": "bus", "name": "구로디지털단지역환승센터", "번호":
"51(대원아파트.구로디지털단지역환승센터)번, 1(숲속마을3.5단지.구로디지털단지역환승센터)번", "위도": 37.484686, "경도": 126.902042}, {"type": "walk", "name":
"석수역", "번호": "도보", "위도": 37.434894, "경도": 126.903041}, {"type": "end", "name": "보안등", "호선": "도착", "위도": 37.43395234,
"경도": 126.9064444}]}]}, {"rank": 3, "route": [{"소요시간": "1시간 2분", "경로": "종로구 신문로2가 -> 160번(서울역사박물관.경희궁앞 ~ 영등포역) -> 수도권 1호선(영등포 ~ 석수) -> 보안등", "역정보": [{"type": "walk", "name": "종로구 신문로2가", "번호": "도보", "위도": 37.570792, "경도": 126.968813},
{"type": "bus", "name": "서울역사박물관.경희궁앞", "번호": "160번", "위도": 37.569289, "경도": 126.970512}, {"type": "walk", "name":
"영등포역", "번호": "도보", "위도": 37.516603, "경도": 126.907085}, {"type": "subway", "name": "영등포", "번호": "수도권 1호선", "위도":
37.515759, "경도": 126.907425}, {"type": "walk", "name": "석수", "번호": "도보", "위도": 37.435166, "경도": 126.902246}, {"type":
"end", "name": "보안등", "호선": "도착", "위도": 37.43395234, "경도": 126.9064444}]}]}, {"rank": 4, "route": [{"소요시간": "0시간 49분",
"경로": "강남구 수서동 -> M5333번(수서역KT수서지점 ~ 석수역) -> 보안등", "역정보": [{"type": "walk", "name": "강남구 수서동", "번호": "도보", "위도":
37.4889102, "경도": 127.1049103}, {"type": "bus", "name": "수서역KT수서지점", "번호": "M5333번", "위도": 37.487219, "경도": 127.100703},
{"type": "walk", "name": "석수역", "번호": "도보", "위도": 37.434894, "경도": 126.903041}, {"type": "end", "name": "보안등", "호선":
"도착", "위도": 37.43395234, "경도": 126.9064444}]}]}, {"rank": 5, "route": [{"소요시간": "1시간 1분", "경로": "종로구 통인동 -> 7016번, 1711번, 7022번(통인시장종로구보건소 ~ 시청앞.덕수궁) -> 수도권 1호선(시청 ~ 석수) -> 보안등", "역정보": [{"type": "walk", "name": "종로구 통인동", "번호": "도보",
"위도": 37.5801426, "경도": 126.9701873}, {"type": "bus", "name": "통인시장종로구보건소", "번호": "7016번, 1711번, 7022번", "위도":
37.580376, "경도": 126.97105}, {"type": "walk", "name": "시청앞.덕수궁", "번호": "도보", "위도": 37.566407, "경도": 126.976924},
{"type": "subway", "name": "시청", "번호": "수도권 1호선", "위도": 37.565444, "경도": 126.97713}, {"type": "walk", "name": "석수",
"번호": "도보", "위도": 37.435166, "경도": 126.902246}, {"type": "end", "name": "보안등", "호선": "도착", "위도": 37.43395234, "경도":
126.9064444}]}]}];


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


    // 상위 컴포넌트로 좌표값 및 마커 위치 정보 전달 
    function drawMap(stationInfo, departName, centerLat, centerLon, level){
        console.log(centerLat, centerLon)

        props.drawMap(stationInfo, departName, centerLat, centerLon, level);

    }

    useEffect(() => {

        const fetchLabels = async () => {

            try {

                // 요청이 시작 할 때에는 error 와 users 를 초기화하고
                setError(null);

                // 추천 관련데이터 받기 전에 요청
                let res = await axios.get(firstUrl, config);
                // API =====
               //  let response = await axios.get(url, config);

                // const rawData = response.data

                // const resRouteArr = rawData.map(data => data.route[0]);
                // API =====
                
                const rawData = dummy
                const resRouteArr = dummy.map(data => data.route[0]);
                

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

        let routeArr = item.route.split("->")
        let arriveLabel = routeArr[routeArr.length-1].split("(")

        let centerLat = ( stationInfo[0].위도 + stationInfo[stationInfo.length-1].위도 )/2;
        let centerLon = ( stationInfo[0].경도 + stationInfo[stationInfo.length-1].경도 )/2;

        const stationAdd = stationInfo.map(station=>([station.위도,station.경도]))
        const departName = stationInfo[0].name

        console.log(stationAdd)

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
                            <br />
                            <button className="draw-line-btn" onClick={()=>drawMap(stationAdd, departName, centerLat, centerLon, 7)}>지도로 보기</button>
                            <br />
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
                        {listItems}
            </div>

        </div>
    )
}

