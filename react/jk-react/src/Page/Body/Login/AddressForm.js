/* global kakao */
import React, { useState } from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import { Button } from '@material-ui/core';

export default function AddressForm() {

    const [inputPlace, setInputPlace] = useState(null);
    const [pagi, setPagi] = useState(null);


    /* ========== 카카오맵 검색 관련 function 시작 ========== */

    // 1. 키워드 검색을 요청하는 함수
    function searchPlaces(event) {

        event.preventDefault();

        // 장소 검색 객체를 생성
        var ps = new kakao.maps.services.Places();

        // input태그에 입력한 정보 받아옴
        var keyword = document.getElementById('frequent').value;

        if (!keyword.replace(/^\s+|\s+$/g, '')) {
            alert('키워드를 입력해주세요!');
            return false;
        }

        // 장소검색 객체를 통해 키워드로 장소검색을 요청
        ps.keywordSearch(keyword, placesSearchCB);

    }

    function placesSearchCB(data, status, pagination) {
        
        setPagi(pagination);

        if (status === kakao.maps.services.Status.OK) {

            console.log(pagination)

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
            menuEl = document.getElementById('search_wrap'),
            fragment = document.createDocumentFragment(),
            bounds = new kakao.maps.LatLngBounds(),
            listStr = '';

        // 검색 결과 목록에 추가된 항목들을 제거합니다
        removeAllChildNods(listEl);


        for (var i = 0; i < places.length / 3; i++) {

            var itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다


            (function (title, selectedListItem) {

                // 리스트 아이템 리스너
                itemEl.onmousedown = function () {

                    // 장소명, 장소 전체정보 담은 객체, 장소 좌표(위도, 경도)
                    // setSelectedPlace(title)
                    // setDestinationInfo(selectedListItem)
                    // setSelectedLocation({
                    //     x: selectedListItem.x,
                    //     y: selectedListItem.y
                    // })

                    // sendData(title, selectedListItem, selectedListItem.x, selectedListItem.y)

                    setInputPlace(title)

                    // 리스트 아이템 삭제
                    removeAllChildNods(listEl)
                    
                    // 페이지 인덱스 삭제
                    var paginationEl = document.getElementById('pagination')

                    removeAllChildNods(paginationEl)


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
        <React.Fragment>

            <br />
            <Typography variant="h6" gutterBottom>자주가는 장소를 입력하세요.</Typography>

            <Grid container >
                <div className="map_wrap" id="change-section">
                    <div id="search_wrap" className="bg_white">
                        <div className="option">
                            <div>
                                <form onSubmit={searchPlaces}>
                                    <Grid item xs={12} sm={12}>
                                        <TextField
                                            focused
                                            required
                                            id="frequent"
                                            name="frequent-place"
                                            label="거주 지역 추천에 사용됩니다! "
                                            fullWidth
                                            autoComplete="given-name"

                                            // 기능 조작을 위한 attribute
                                            type="text"
                                            value={inputPlace || ''}
                                            onChange={e => { setInputPlace(e.target.value) }}
                                        />
                                    </Grid>

                                    <Grid item xs={3} sm={12}>

                                        <Button type="submit">
                                            select
                                    </Button>
                                    </Grid>
                                </form>
                            </div>
                        </div>
                    </div>
                    <hr />
                    <ul id="placesList"></ul>
                    <div id="pagination"></div>
                </div>
            </Grid>
        </React.Fragment>
    );
}