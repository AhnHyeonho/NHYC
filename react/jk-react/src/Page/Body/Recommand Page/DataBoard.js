/*global kakao */
import React from 'react';

import RecommandTable from './RecommandTable';
import RadarChart from './RadarChart';
import PreferRadar from './PreferRadar';
import TrafficSection from './TrafficSection'; 

import './DataBoard.css';



class DataBoard extends React.Component {


    constructor(props) {
        super(props)

        this.state = {

            // placeName: "",

            selectedPlace: null,
            destinationInfo: null
        };

        this.changeMap = this.changeMap.bind(this)
        this.getTrafficData = this.getTrafficData.bind(this)
    }


    changeMap(lat, lon) {
        this.props.onChange(lat, lon)
    }

    getTrafficData(name, obj){

        console.log("목적지="+name);
        console.log(obj);
        
        this.setState({
            selectedPlace: name,
            destinationInfo: obj        
        })

        console.log(this.state.selectedPlace)
    }





    render() {


        // function setDestination(placeName, placeInfo) {

        //     console.log("목적지 = " + placeName);
        //     console.log(placeInfo)

        //     this.setState({
        //         selectedPlace: placeName,
        //         selectedListItem: placeInfo
        //     })
        // }

        // /* ========== 카카오맵 검색 관련 function 시작 ========== */


        // // 1. 키워드 검색을 요청하는 함수
        // function searchPlaces(event) {

        //     event.preventDefault();

        //     // 장소 검색 객체를 생성
        //     var ps = new kakao.maps.services.Places();

        //     // input태그에 입력한 정보 받아옴
        //     var keyword = document.getElementById('keyword').value;

        //     if (!keyword.replace(/^\s+|\s+$/g, '')) {
        //         alert('키워드를 입력해주세요!');
        //         return false;
        //     }

        //     // 장소검색 객체를 통해 키워드로 장소검색을 요청
        //     ps.keywordSearch(keyword, placesSearchCB);

        // }

        // function placesSearchCB(data, status, pagination) {
        //     if (status === kakao.maps.services.Status.OK) {

        //         // 정상적으로 검색이 완료됐으면
        //         // 검색 목록과 마커를 표출합니다
        //         displayPlaces(data);

        //         // 페이지 번호를 표출합니다
        //         displayPagination(pagination);

        //     } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        //         alert('검색 결과가 존재하지 않습니다.');
        //         return;

        //     } else if (status === kakao.maps.services.Status.ERROR) {

        //         alert('검색 결과 중 오류가 발생했습니다.');
        //         return;

        //     }
        // }


        // // 3. 검색 결과 목록과 마커를 표출하는 함수
        // function displayPlaces(places) {

        //     var listEl = document.getElementById('placesList'),
        //         menuEl = document.getElementById('menu_wrap'),
        //         fragment = document.createDocumentFragment(),
        //         bounds = new kakao.maps.LatLngBounds(),
        //         listStr = '';

        //     // 검색 결과 목록에 추가된 항목들을 제거합니다
        //     removeAllChildNods(listEl);

        //     // // 지도에 표시되고 있는 마커를 제거합니다
        //     // removeMarker();

        //     for (var i = 0; i < places.length; i++) {

        //         var itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다


        //         (function (title, selectedListItem) {

        //             // 리스트 아이템 리스너
        //             itemEl.onmousedown = function () {
        //                 console.log(title)

        //                 setDestination(title, selectedListItem)

        //             };

        //         })(places[i].place_name, places[i]);

        //         fragment.appendChild(itemEl);
        //     }

        //     // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
        //     listEl.appendChild(fragment);
        //     menuEl.scrollTop = 0;

        //     // // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
        //     // map.setBounds(bounds);
        // }


        // // 검색결과 항목을 Element로 반환하는 함수
        // function getListItem(index, places) {

        //     var el = document.createElement('li'),
        //         itemStr = '<span class="markerbg marker_' + (index + 1) + '"></span>' +
        //             '<div class="info">' +
        //             '   <h5>' + places.place_name + '</h5>';

        //     if (places.road_address_name) {
        //         itemStr += '    <span>' + places.road_address_name + '</span>' +
        //             '   <span class="jibun gray">' + places.address_name + '</span>';
        //     } else {
        //         itemStr += '    <span>' + places.address_name + '</span>';
        //     }

        //     itemStr += '  <span class="tel">' + places.phone + '</span>' +
        //         '</div>';

        //     el.innerHTML = itemStr;
        //     el.className = 'item';

        //     return el;
        // }


        // // 검색결과 목록 하단에 페이지번호를 표시는 함수
        // function displayPagination(pagination) {
        //     var paginationEl = document.getElementById('pagination'),
        //         fragment = document.createDocumentFragment(),
        //         i;

        //     // 기존에 추가된 페이지번호를 삭제
        //     while (paginationEl.hasChildNodes()) {
        //         paginationEl.removeChild(paginationEl.lastChild);
        //     }

        //     for (i = 1; i <= pagination.last; i++) {
        //         var el = document.createElement('a');
        //         el.href = "#";
        //         el.innerHTML = i;

        //         if (i === pagination.current) {
        //             el.className = 'on';
        //         } else {
        //             el.onclick = (function (i) {
        //                 return function () {
        //                     pagination.gotoPage(i);
        //                 }
        //             })(i);
        //         }

        //         fragment.appendChild(el);
        //     }
        //     paginationEl.appendChild(fragment);
        // }

        // // 검색결과 목록의 자식 Element를 제거하는 함수
        // function removeAllChildNods(el) {
        //     while (el.hasChildNodes()) {
        //         el.removeChild(el.lastChild);
        //     }
        // }


        // /* ========== 카카오맵 검색 관련 function 끝 ========== */



        return (

            // 데이터보드
            <div className="recommand-databoard">


                {/* 데이터보드 타이틀 */}
                <div className="recommand-databoard-title"> 데이터 보드 </div>


                {/* 데이터보드 아이템 리스트  */}
                {/* 1. 추천지역 리스트  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 추천지역 리스트 </div>
                    <RecommandTable changeMap={this.changeMap} />
                </div>

                {/* 2. 추천 지표 그래프  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 지역별 월세/보증금 및 시설 현황 </div>
                    {/* 타이틀 옆에 아이콘 추가해서 마우스 오버시 팝업으로 설명 확인할 수 있도록 하기 */}
                    <RadarChart width={500} height={500} name="localStatus" />
                </div>

                {/* 3. 추천 지표에 대한 사용자 선호도  */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title" > 각 추천 지표에 대한 사용자 선호도 </div>
                    <PreferRadar width={500} height={500} name="prefer" />
                </div>

                {/* 4. 대중 교통 추천 섹션 */}
                <div className="recommand-databoard-item">
                    <div className="recommand-databoard-item-title"> 추천지역 접근성 비교 </div>
                    <div className="traffic-subtitle-section">
                        <div className="decorate-bar-databoard" />
                        <span className="recommand-databoard-item-subtitle">자주가는 장소 등록</span>

                        <span className="detail-comment">자주가는 장소와 추천 지역간의 교통을 한눈에 확인하세요!</span>
                    </div>

                    <div className="traffic-search-result">
                        <div className="recommand-databoard-item-subtitle">목적지 <span className="destination-label">{this.state.selectedPlace}</span></div>
                    </div>

                    <TrafficSection getTrafficData={this.getTrafficData}/>

                    {/* ========== 카카오맵 ========== */}

                    {/* <div className="map_wrap">

                        <div id="menu_wrap" className="bg_white">
                            <div className="option">
                                <div>
                                    <form onSubmit={searchPlaces}>
                                        키워드 : <input type="text" value={this.state.placeName} id="keyword" size="15" onChange={e => { this.setState({ placeName: e.target.value }) }} />
                                        <button type="submit">검색하기</button>
                                    </form>
                                </div>
                            </div>
                            <hr />
                            <ul id="placesList"></ul>
                            <div id="pagination"></div>
                        </div>
                    </div> */}

                    {/* ========== 카카오맵 ========== */}


                </div>



            </div >
        )
    }
}
export default DataBoard;