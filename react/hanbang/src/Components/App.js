import React, {Component} from 'react';
import BarGraph from './BarGraph';
import './App.css'


// react-vis
class App extends Component {
  render() {

    const seoulGu = ['강동구', '노원구', '노원구', '노원구', '노원구', '노원구', '노원구', '노원구' ]

    return (
      <div className="graph-area" >
        <BarGraph name="서울시 면적당 CCTV 설치 현황" labelData={seoulGu}/>
        <BarGraph name="서울시 경찰서 / 파출소 / 지구대 현황" labelData={seoulGu}/>
        <BarGraph name="서울시 가로등 설치 현황" labelData={seoulGu}/>
      </div>
    );
  }
}



export default App;