import React from 'react';
import './GuList.css';
import { MDBCol, MDBListGroupItem, MDBRow, MDBCard, MDBListGroup, MDBBtn} from "mdbreact";


import { Scrollbars } from 'react-custom-scrollbars';

class GuList extends React.Component{
  render(){
    return (
      <MDBCol>
      <MDBCard className="guCard" style={{ height: "43vh", width:"21vw",border:"none"}}>
        <Scrollbars >
              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{margin:0,color:"white"}} onClick={()=>this.props.handleChange('강남구')}>
                    <div className="fo">강남구</div>
                  </MDBBtn>               
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('강동구')}>
                    <div className="fo">강동구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('강서구')}>
                    <div className="fo">강서구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleChange('강북구')}>
                    <div className="fo">강북구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleChange('관악구')}>
                    <div className="fo">관악구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('광진구')}>
                    <div className="fo">광진구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('구로구')}>
                    <div className="fo">구로구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('금천구')}>
                    <div className="fo">금천구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue"  size="lg" className="guName" style={{color:"white"}} onClick={()=>this.props.handleChange('노원구')}>
                  <div className="fo">노원구</div>
                  </MDBBtn>               
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('동대문구')}>
                    <div className="fo">동대문구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('도봉구')}>
                    <div className="fo">도봉구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('동작구')}>
                    <div className="fo">동작구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('마포구')}>
                    <div className="fo">마포구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('서대문구')}>
                    <div className="fo">서대문구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('성동구')}>
                    <div className="fo">성동구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('성북구')}>
                    <div className="fo">성북구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('서초구')}>
                    <div className="fo">서초구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('송파구')}>
                    <div className="fo">송파구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('영등포구')}>
                    <div className="fo">영등포구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('용산구')}>
                    <div className="fo">용산구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('양천구')}>
                    <div className="fo">양천구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('은평구')}>
                    <div className="fo">은평구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('종로구')}>
                    <div className="fo">종로구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('중구')}>
                    <div className="fo">중구</div>
                  </MDBBtn>              
              </MDBRow>

              <MDBRow>
                  <MDBBtn color="blue" size="lg" className="guName" style={{color:"white"}}  onClick={()=>this.props.handleChange('중랑구')}>
                    <div className="fo">중랑구</div>
                  </MDBBtn>              
              </MDBRow>

        </Scrollbars >
      </MDBCard>
      </MDBCol>

    );
  }
};

export default GuList;