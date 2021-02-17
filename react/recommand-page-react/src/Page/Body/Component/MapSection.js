import React from 'react';
import SeoulMap from '../../../Img/map.gif';
import Inform from '../../../Img/mapAlt.png';

import '../Component/Map.css'

class MapSection extends React.Component {
    
    render(){

        return (
            <div className="seoulMap mapImg-container">
            <img src={Inform} className="mapImg info"></img>
            <img src={SeoulMap} className="mapImg" alt="서울시지도" border="0" useMap="#Map" ></img>
            <map name="Map">
                <area shape="poly" coords="276,30,284,29,287,22,297,33,307,32,300,41,307,53,304,68,306,84,315,88,320,99,312,102,312,110,295,115,285,118,270,104,276,93,280,66,274,55" href="#nowon" alt="노원" onClick={()=>this.props.handleChange('노원구')} />
                <area shape="poly" coords="236,25,250,23,251,32,267,33,271,41,272,53,277,69,268,100,251,81,234,68" href="#dobong" alt="도봉" />
                <area shape="poly" coords="222,42,231,40,229,66,240,82,253,92,263,113,250,124,237,122,233,104,211,94,212,66" href="#gangbuk" alt="강북"/>
                <area shape="poly" coords="204,98,211,97,231,109,240,129,261,128,266,117,274,124,282,130,258,141,244,154,238,158,223,144,213,140,218,125" href="#sungbuk" alt="성북"/>
                <area shape="poly" coords="289,124,312,118,325,125,319,133,322,146,309,162,294,172" href="#jungrang" alt="중랑"/>
                <area shape="poly" coords="249,159,260,152,263,141,284,137,287,172,284,185,267,178,262,170,245,174" href="#dongdaemun" alt="동대문" />
                <area shape="poly" coords="191,102,202,100,212,125,207,137,212,144,231,164,241,166,218,173,201,171,188,163,191,146,186,132" href="#jongno" alt="종로" />
                <area shape="poly" coords="149,81,156,84,177,75,190,94,182,107,178,128,138,155,132,145,145,124" href="#eunpyeong" alt="은평"/>
                <area shape="poly" coords="150,154,162,154,165,146,172,143,178,135,186,148,181,169,190,176,174,183,146,163" href="#seodaemun" alt="서대문" />
                <area shape="poly" coords="193,181,205,176,240,176,229,196,209,193,192,193" href="#jungu" alt="중구" />
                <area shape="poly" coords="244,179,259,176,281,190,273,220,257,211,240,213,233,199" href="#seongdong" alt="성동" />
                <area shape="poly" coords="292,176,310,170,308,184,314,196,295,221,278,220" href="#gwangjin" alt="광진" />
                <area shape="poly" coords="324,200,334,184,369,171,376,181,376,202,349,212,342,233,327,224" href="#gangdong" alt="강동" />
                <area shape="poly" coords="103,160,115,154,121,147,158,185,187,189,173,215,125,195" href="#mapo" alt="마포" />
                <area shape="poly" coords="189,197,209,196,227,203,233,214,205,236,191,237,177,219" href="#yongsan" alt="용산"/>
                <area shape="poly" coords="50,138,109,196,101,198,94,215,81,210,66,197,50,202,26,192" href="#gangseo" alt="강서" />
                <area shape="poly" coords="70,210,80,217,100,221,106,202,113,201,119,213,114,237,95,234,88,239,73,235" href="#yangcheon" alt="양천" />
                <area shape="poly" coords="121,200,147,211,149,225,158,234,152,251,138,266,135,270,128,267,125,240,119,237" href="#yeongdungpo" alt="영등포" />
                <area shape="poly" coords="67,243,61,261,66,270,66,282,80,285,93,277,97,261,108,261,117,270,129,266,121,257,122,249,118,241,108,248,91,243,95,238,81,248,73,245" href="#guro" alt="구로" />
                <area shape="poly" coords="164,235,174,233,195,252,205,256,205,280,191,284,184,265,158,261,143,267" href="#dongjak" alt="동작" />
                <area shape="poly" coords="112,277,125,274,137,276,141,299,152,316,130,328" href="#geumcheon" alt="금천" />
                <area shape="poly" coords="142,272,157,267,180,270,189,285,201,289,210,301,168,327,149,305" href="#gwanak" alt="관악" />
                <area shape="poly" coords="206,248,230,230,240,255,247,275,258,293,267,302,287,294,297,307,271,335,253,330,249,297,228,306,207,291" href="#seocho" alt="서초" />
                <area shape="poly" coords="241,222,275,234,275,254,307,266,327,297,307,305,293,286,281,286,267,292,255,272,247,270,234,229" href="#gangnam" alt="강남" />
                <area shape="poly" coords="285,234,307,229,320,208,322,229,338,236,334,245,353,260,345,274,335,288,329,291,311,264,286,253" href="#songpa" alt="송파" />
            </map>
            <p className="map-point" id="">지도포인트</p>
        </div>

        );
    }
}

export default MapSection;