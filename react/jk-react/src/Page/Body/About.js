import React from 'react';
import backImg from '../../Img/backgroundImg.jpg';
import logo from '../../Img/logo1.png';
import middleBar from '../../Img/middle-bar.png';
import button1 from '../../Img/button1.png';

import Carousel from 'react-bootstrap/Carousel'
import LineGraph from './Component/LineGraph'


import './About.css';

class About extends React.Component{
    render(){
        return (
 
            <Carousel>  
                <Carousel.Item style={{'height':"90vh"}}>  
                <div className="app-body-about">

                    <div className ="logo-image-wrapper-wrapper">
                        <div className = "logo-image-wrapper"><LineGraph/><img className="logo1" src={logo}/><div className="middle-bar" /></div>
                    </div>

                    <div className ="middle-bar-image-wrapper-wrapper">
                        <div className = "middle-bar-image-wrapper"><img className="middle-bar" src={middleBar}/></div>
                    </div>
                    
                    <div className ="content-wrapper">
                        <div className ="cotent">대학생들을 위한 월세 실거래가 추이 제공 및 거주 지역 및 매물 추천</div>
                    </div>
                    
                    <div className ="button1-image-wrapper-wrapper">
                        <div className = "button1-image-wrapper"><img className="button1" src={button1}/></div>
                    </div>
                    
                    <img className ="background-image" src={backImg}/>
                </div> 
                </Carousel.Item >  
                
                <Carousel.Item style={{'height':"90vh"}}>  
                <div className="app-body-about">

                    <div className ="logo-image-wrapper-wrapper">
                        <div className = "logo-image-wrapper"><img className="logo1" src={logo}/><div className="middle-bar" /></div>
                    </div>

                    <div className ="middle-bar-image-wrapper-wrapper">
                        <div className = "middle-bar-image-wrapper"><img className="middle-bar" src={middleBar}/></div>
                    </div>
                    
                    {/* 여기에 carousel 넣어야함*/}

                    <div className ="content-wrapper">
                        <div className ="cotent">대학생들을 위한 월세 실거래가 추이 제공 및 거주 지역 및 매물 추천</div>
                    </div>
                    
                    <div className ="button1-image-wrapper-wrapper">
                        <div className = "button1-image-wrapper"><img className="button1" src={button1}/></div>
                    </div>
                    
                    <img className ="background-image" src={backImg}/>
                </div> 
                    <Carousel.Caption>  
                        <h3>First Demo </h3>  
                    </Carousel.Caption>  
                </Carousel.Item  >  

                <Carousel.Item style={{'height':"90vh"}}>  
                <div className="app-body-about">


                    
                    <img className ="background-image" src={backImg}/>
                </div> 
                <Carousel.Caption>  
                    <h3>First Demo </h3>  
                </Carousel.Caption>  
                </Carousel.Item  >   

            </Carousel>  
   
  






            
     
        )
    }
}
      
export default About;
