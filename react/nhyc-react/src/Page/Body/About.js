import React from 'react';
import backImg from '../../Img/Background4.jpg';
import ranking from '../../Img/ranking.png';
import recommend from '../../Img/recommend.png';

import Carousel from 'react-bootstrap/Carousel'



import './About.css';
import { Link } from 'react-router-dom';

class About extends React.Component{



    render(){





        return (
            <div>
            <Carousel>  
                {/*1*/}
                <Carousel.Item style={{'height':"100vh"}}>  
                <div className="app-body-about">

                    <div className ="logo-image-wrapper-wrapper">
                        <div className = "logo-image-wrapper"><div className="logoAbout">HanBang</div></div>
                    </div>

                    <div className ="middle-bar-image-wrapper-wrapper">
                        <div className = "middle-bar-image-wrapper"><div className="barAbout"></div></div>
                    </div>
                    
                    <div className ="content-wrapper">
                        <div className ="cotent">대학생들을 위한 월세 실거래가 추이 제공 및 거주 지역 및 매물 추천</div>
                    </div>
                    
                    <img className ="background-image" src={backImg}/>
                </div> 
                </Carousel.Item >  
                
                {/*2*/}
                <Carousel.Item style={{'height':"100vh"}}>  
                <div className="app-body-about">
                    <div className ="logo-image-wrapper-wrapper">
                        <div className = "logo-image-wrapper">
                            <img src={ranking} className="rankingImg"/>

                        </div>

                        <div className = "logo-image-wrapper">
                            <div className="comentAbout"> 가격 순위 및 추이 조회 </div>
                        </div>

                        <div className = "coment-wrapper">
                            <div className="comentAbout_c"> " 서울시의 25개 구와 각 구별 동의 월세/보증금 실거래가 평균, 월세 가격 순위 및 추이 조회해보세요 " </div>
                        </div>
                    </div>

                    
                    <img alt=""  className ="background-image2" src={backImg}/>
                </div> 

                </Carousel.Item  >  




                {/*3*/}
                <Carousel.Item style={{'height':"100vh"}}>  
                <div className="app-body-about">
                    <div className ="logo-image-wrapper-wrapper">
                        <div className = "logo-image-wrapper">
                            <img src={recommend} className="rankingImg"/>

                        </div>

                        <div className = "logo-image-wrapper">
                            <div className="comentAbout"> 추천 지역 제공</div>
                        </div>

                        <div className = "coment-wrapper">
                            <div className="comentAbout_c"> " 관심 지표 시각화 하여 추천 지역 리스트 제공해드립니다 " </div>
                        </div>
                    </div>

                    
                    <img alt=""  className ="background-image2" src={backImg}/>
                </div> 

                </Carousel.Item  >  



            </Carousel>  
   
            <div className="containerAbout"><Link to ="/map" className="linktest"><button className="btn expand-on-hover blue"><span className="textAbout">한방에 보기</span></button></Link> </div> 

                



            </div>




            
     
        )
    }
}
      
export default About;



