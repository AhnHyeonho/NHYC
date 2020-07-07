import React from 'react';
import './GuList.css';
import { MDBCol, MDBRow, MDBCard, MDBListGroup, MDBBtn,MDBCarousel, MDBScrollbar } from "mdbreact";

import { Scrollbars } from 'react-custom-scrollbars';

class DGuList extends React.Component {

  render(){
    const dongs = this.props.listData;
    
    
    const dongList = dongs.map(
    (dong,index) => (
       
    <MDBRow>
      <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleDongNum(index+1,dong)}>
        <div className="fo" key={index}>{dong}</div>
      </MDBBtn>
    </MDBRow>
    
    )
    );

    return (
      <MDBCol>
      <MDBCard className="guCard" style={{ height: "43vh", width:"21vw",border:"none"}}>
      <Scrollbars >

        {dongList} 
      </Scrollbars >
        
      </MDBCard>
      </MDBCol>

    );
  }
};

export default DGuList;