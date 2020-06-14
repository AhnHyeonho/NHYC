/* global kakao */
import React, { useState, useEffect } from 'react';


export default function TrafficSection(props) {

    const [inputPlace, setInputPlace] = useState(null);

    // 목적지 이름
    const [selectedPlace, setSelectedPlace] = useState(null);

    // 목적지 전체 정보 
    const [destinationInfo, setDestinationInfo] = useState(null);

    
    function sendData(title, obj) {
        props.getTrafficData(title, obj);
    }



    /* ========== 카카오맵 검색 관련 function 시작 ========== */


    // 1. 키워드 검색을 요청하는 함수
    function searchPlaces(event) {

        event.preventDefault();

        // 장소 검색 객체를 생성
        var ps = new kakao.maps.services.Places();

        // input태그에 입력한 정보 받아옴
        var keyword = document.getElementById('keyword').value;

        if (!keyword.replace(/^\s+|\s+$/g, '')) {
            alert('키워드를 입력해주세요!');
            return false;
        }

        // 장소검색 객체를 통해 키워드로 장소검색을 요청
        ps.keywordSearch(keyword, placesSearchCB);

    }

    function placesSearchCB(data, status, pagination) {
        if (status === kakao.maps.services.Status.OK) {

            // 정상적으로 검색이 완료됐으면
            // 검색 목록과 마커를 표출합니다
            displayPlaces(data);

            // 페이지 번호를 표출합니다
            displayPagination(pagination);

        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

            alert('검색 결과가 존재하지 않습니다.');
            return;

        } else if (status === kakao.maps.services.Status.ERROR) {

            alert('검색 결과 중 오류가 발생했습니다.');
            return;

        }
    }


    // 3. 검색 결과 목록과 마커를 표출하는 함수
    function displayPlaces(places) {

        var listEl = document.getElementById('placesList'),
            menuEl = document.getElementById('menu_wrap'),
            fragment = document.createDocumentFragment(),
            bounds = new kakao.maps.LatLngBounds(),
            listStr = '';

        // 검색 결과 목록에 추가된 항목들을 제거합니다
        removeAllChildNods(listEl);

        // // 지도에 표시되고 있는 마커를 제거합니다
        // removeMarker();

        for (var i = 0; i < places.length; i++) {

            var itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다


            (function (title, selectedListItem) {

                // 리스트 아이템 리스너
                itemEl.onmousedown = function () {
                    setSelectedPlace(title)
                    setDestinationInfo(selectedListItem)

                    console.log(selectedListItem)
                    sendData(title, selectedListItem)

                };

            })(places[i].place_name, places[i]);

            fragment.appendChild(itemEl);
        }

        // 검색결과 항목들을 검색결과 목록 Elemnet에 추가
        listEl.appendChild(fragment);
        menuEl.scrollTop = 0;

    }


    // 검색결과 항목을 Element로 반환하는 함수
    function getListItem(index, places) {

        var el = document.createElement('li'),
            itemStr = '<span class="markerbg marker_' + (index + 1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

        if (places.road_address_name) {
            itemStr += '    <span>' + places.road_address_name + '</span>' +
                '   <span class="jibun gray">' + places.address_name + '</span>';
        } else {
            itemStr += '    <span>' + places.address_name + '</span>';
        }

        itemStr += '  <span class="tel">' + places.phone + '</span>' +
            '</div>';

        el.innerHTML = itemStr;
        el.className = 'item';

        return el;
    }


    // 검색결과 목록 하단에 페이지번호를 표시는 함수
    function displayPagination(pagination) {
        var paginationEl = document.getElementById('pagination'),
            fragment = document.createDocumentFragment(),
            i;

        // 기존에 추가된 페이지번호를 삭제
        while (paginationEl.hasChildNodes()) {
            paginationEl.removeChild(paginationEl.lastChild);
        }

        for (i = 1; i <= pagination.last; i++) {
            var el = document.createElement('a');
            el.href = "#";
            el.innerHTML = i;

            if (i === pagination.current) {
                el.className = 'on';
            } else {
                el.onclick = (function (i) {
                    return function () {
                        pagination.gotoPage(i);
                    }
                })(i);
            }

            fragment.appendChild(el);
        }
        paginationEl.appendChild(fragment);
    }

    // 검색결과 목록의 자식 Element를 제거하는 함수
    function removeAllChildNods(el) {
        while (el.hasChildNodes()) {
            el.removeChild(el.lastChild);
        }
    }


    /* ========== 카카오맵 검색 관련 function 끝 ========== */



    return (
        <div className="map_wrap">

            <div id="menu_wrap" className="bg_white">
                <div className="option">
                    <div>
                        <form onSubmit={searchPlaces}>
                            키워드 : <input type="text" value={inputPlace || ''} id="keyword" size="15" onChange={e => { setInputPlace(e.target.value) }} />
                            <button type="submit">검색하기</button>
                        </form>
                    </div>
                </div>
                <hr />
                <ul id="placesList"></ul>
                <div id="pagination"></div>
            </div>
        </div>
    )

}