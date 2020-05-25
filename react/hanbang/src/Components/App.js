import React, {Component} from 'react';
import BarGraph from './BarGraph';

// react-vis
class App extends Component {
  render() {
    return (
      <div>
        <BarGraph name="서울시 면적당 CCTV 설치 현황"/>
        <BarGraph name="서울시 경찰서 / 파출소 / 지구대 현황"/>
        <BarGraph name="서울시 가로등 설치 현황"/>
      </div>
    );
  }
}



export default App;