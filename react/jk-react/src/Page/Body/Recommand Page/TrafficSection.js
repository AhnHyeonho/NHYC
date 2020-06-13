/*global kakao*/
import React, { useState, useEffect } from 'react';

import './TrafficSection.css';


export default function TrafficSection(props) {
    //input 태그
    const [place, setPlace] = useState(null);

    // 검색 결과에서 선택된 장소
    const [selectedPlace, setSelectedPlace] = useState({
        title: "",
    });

    function sendData(title, obj) {
        props.getTrafficData(title, obj);
    }

    // 키워드 검색을 요청하는 함수입니다
    function searchPlaces(e) {
       
        var ps = new kakao.maps.services.Places();  
        var keyword = document.getElementById('keyword').value;

        if (!keyword.replace(/^\s+|\s+$/g, '')) {
            alert('키워드를 입력해주세요!');
            return false;
        }
    
        // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
        ps.keywordSearch( keyword, placesSearchCB); 

    }


    // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
    function displayPagination(pagination) {
        var paginationEl = document.getElementById('pagination'),
            fragment = document.createDocumentFragment(),
            i;

        // 기존에 추가된 페이지번호를 삭제합니다
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


    // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
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


    // 검색 결과 목록과 마커를 표출하는 함수
    function displayPlaces(places) {

        var listEl = document.getElementById('placesList'),
            menuEl = document.getElementById('menu_wrap'),
            fragment = document.createDocumentFragment(),
            bounds = new kakao.maps.LatLngBounds(),
            listStr = '';

        // 검색 결과 목록에 추가된 항목들을 제거합니다
        // removeAllChildNods(listEl);

        // 지도에 표시되고 있는 마커를 제거합니다
        // removeMarker();

        for (var i = 0; i < places.length; i++) {

            // 마커를 생성하고 지도에 표시합니다
            // var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            //     marker = addMarker(placePosition, i), 
            var itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

            console.log(places[i].place_name);
            // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
            // LatLngBounds 객체에 좌표를 추가합니다
            // bounds.extend(placePosition);

            // 마커와 검색결과 항목에 mouseover 했을때
            // 해당 장소에 인포윈도우에 장소명을 표시합니다
            // mouseout 했을 때는 인포윈도우를 닫습니다
            (function (title, obj) {
                // kakao.maps.event.addListener(marker, 'mouseover', function() {
                //     displayInfowindow(marker, title);
                // });

                // kakao.maps.event.addListener(marker, 'mouseout', function() {
                //     infowindow.close();
                // });

                itemEl.onmousedown = function () {
                    console.log(title)
                    sendData(title, obj);
                };

                // itemEl.onmouseout = function () {
                //     infowindow.close();
                // };
            })(places[i].place_name, places[i]);

            fragment.appendChild(itemEl);
        }

        // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
        listEl.appendChild(fragment);
        menuEl.scrollTop = 0;

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
        // map.setBounds(bounds);
    }


    // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
    // 인포윈도우에 장소명을 표시합니다
    // function displayInfowindow(marker, title) {
    //     var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    //     infowindow.setContent(content);
    //     infowindow.open(map, marker);
    // }


    // 검색결과 항목을 Element로 반환하는 함수입니다
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



    return (
        <div className="map_wrap">
            <div id="menu_wrap" className="bg_white">
                <div className="option">
                    <div>
                        <form onSubmit={() => { searchPlaces(); }}>
                            키워드 : <input type="text" value={place || ""} onChange={e => setPlace(e.target.value)} id="keyword" size="15" />
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