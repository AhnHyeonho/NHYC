/*global kakao*/
import React from 'react';
import './SearchBar.css'

class SearchBar extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
//        var placeSearchObj = new kakao.maps.services.Places();

    }

    render() {
        return (
            <div className="search-group"> {/* 클릭시 리스트 뜨는 것 까지 묶어줌 */}
                <div> {/* input, btn 묶어줌 */}
                    <input type="text" className="search-input" placeholder="건물명을 입력해주세요!" />
                    <button onClick={this.clickSearchBtn} type="submit" className="btn-search" />
                </div>
            </div>
        )
    }

    // 버튼 눌렀을 때 동작 
    clickSearchBtn = ()=> {
        var keyword = document.getElementsByClassName("search-input").value;
        // placesSearchCB.keywordSearch(keyword,placesSearchCB);
    }

    
}

// // 키워드 검색 완료 시 호출되는 콜백함수 입니다
// function placesSearchCB (data, status, pagination) {
//     if (status === kakao.maps.services.Status.OK) {

//         // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
//         // LatLngBounds 객체에 좌표를 추가합니다
//         var bounds = new kakao.maps.LatLngBounds();

//         for (var i=0; i<data.length; i++) {
//             displayMarker(data[i]);    
//             bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
//         }       

//         // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
//         map.setBounds(bounds);
//     } 
// }
export default SearchBar;