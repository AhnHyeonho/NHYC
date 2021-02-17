import React from 'react';
import './GuList.css';
import { MDBCol, MDBRow, MDBCard, MDBListGroup, MDBBtn,MDBCarousel, MDBScrollbar } from "mdbreact";

import { Scrollbars } from 'react-custom-scrollbars';

class NowonGuList extends React.Component {

  render(){


    return (
      <MDBCol>
      <MDBCard className="guCard" style={{ height: "43vh", width:"21vw",border:"none"}}>
      <Scrollbars >
                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(1)}>
                      <div className="fo">월계동</div>
                    </MDBBtn>               
                </MDBRow>

                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(2)}>
                      <div className="fo">공릉동</div>
                    </MDBBtn>              
                </MDBRow>

                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(3)}>
                      <div className="fo">하계동</div>
                    </MDBBtn>              
                </MDBRow>

                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(4)}>
                      <div className="fo">중계동</div>
                    </MDBBtn>              
                </MDBRow>

                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(5)}>
                      <div className="fo">상계동</div>
                    </MDBBtn>              
                </MDBRow>

                <MDBRow>
                    <MDBBtn color="orangered" size="lg" className="guName" style={{color:"white"}}>
                      <div className="fo"></div>
                    </MDBBtn>              
                </MDBRow>

              
          </Scrollbars >
        
      </MDBCard>
      </MDBCol>

    );
  }
};

export default NowonGuList;