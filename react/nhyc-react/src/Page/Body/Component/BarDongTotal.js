import React, { Component } from 'react'
import { Bar } from 'react-chartjs-2';
import './BarGraph.css'

//여기에 교통 연결하면됨


// 너무 많은 mousemove 때문에 최초의 mouseover만 구하기 위한 flag값 
let mouseEventFlag = true;
let mouseOverTime = 0; // 마우스 올라간 시간 저장
let mouseOutTime = 0;  // 마우스 내려온 시간 저장

		// Bar Graph 옵션값 
		var options = {
			legend: {
				display: true,
				position : 'right'
			},

			responsive: false, // true로 바꾸면 화면에 꽉차게끔 그래프가 그려짐 (default = true)

			tooltips: {
				custom: function (tooltip) {
					 
					

					// tooltip 보일 때
					if (tooltip.opacity > 0) {
						
						//console.log("Tooltip is showing");

						const date = new Date();

						// 마우스가 올라간 현재 시간 저장  s
						mouseOverTime = date.getTime();

						// mouseover 한번만 인식 하도록 Flag 설정 
						mouseEventFlag = false;
					} 
					
					// tooltip 사라질 때
					else {
						//console.log("Tooltip is hidden");

						const date = new Date();

						// 마우스 내려온 현재 시간 저장
						mouseOutTime = date.getTime();
						
						// onMouseOver을 다시 인식할 수 있도록 Flag 설정 
						mouseEventFlag = true;
						
						// 마우스가 내려온시간에서 마우스가 올라간 시간을 빼서 머무른 시간 구하기 
						let trackedTime = mouseOutTime - mouseOverTime;
						console.log(options["title"]["text"]+ " Table " + trackedTime + " miliseconds");

						// 여기서 API 호출 함수 불러주면 될 듯
						// 
					}
					//return;
				},

				callbacks: { // 툴팁에 나타나는 문구 수정 해줄 수 있음
					label: function (tooltipItem) {
						
						return   Number(tooltipItem.yLabel)+"개";
						
					}
				}
			},

			title: {
				display: true,
				//text: 'Ice Cream Truck',
				position: 'bottom'
			},

			
			scales: {
				xAxes: [{
					stacked: true,
				}],
				yAxes: [{
					ticks: {
						beginAtZero: true
					},
					stacked: true
				}]
			},

			maintainAspectRatio: true
		};




class BarDongTotal extends Component {

	constructor(props) {
		super(props);
		this.getCntData = this.getCntData.bind(this);

		this.state={
			busCnt : '',
			subwayCnt : '',
			cctvCnt : '',
			policeCnt : '',
			lightCnt : '',
			parkCnt :'',
			pharmacyCnt:'',
			marketCnt : '',
			libraryCnt : '',
			sportsCnt : '',
			artCnt : '',
			concertCnt : '',



		}

	};
	



	getCntData(guName,dongName){
		
		//교통
		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getBusCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({busCnt : json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSubwayCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({subwayCnt : json}))



		//보안
		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCCTVCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({cctvCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPoliceOfficeCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({policeCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getSecurityLightCnt/'+guName+'/'+dongName +'/')
		.then(res => res.json())
		.then(json => this.setState({lightCnt :json}))


		//생활
		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getParkCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({parkCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getPharmacyCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({pharmacyCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getMarketCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({marketCnt:json}))


		//문화
		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getLibraryCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({libraryCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getGymCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({sportsCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getCulturalFacilityCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({artCnt :json}))

		fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getConcertHallCnt/'+guName+'/'+dongName+'/')
		.then(res => res.json())
		.then(json => this.setState({concertCnt :json}))


		
	}


	componentDidMount(){
		this.getCntData(this.props.guName, this.props.dongName);
	}



	render() {

		var busData = this.state.busCnt[0];
		var subwayData = this.state.subwayCnt[0];
		
		var cctvData = this.state.cctvCnt[0];
		var policeData = this.state.policeCnt[0];
		var lightData = this.state.lightCnt[0];

		var parkData = this.state.parkCnt[0];
		var pharmacyData = this.state.pharmacyCnt[0];
		var marketData = this.state.marketCnt[0];

		var libraryData=this.state.libraryCnt[0];
		var sportsData = this.state.sportsCnt[0];
		var artData = this.state.artCnt[0];
		var concertData = this.state.concertCnt[0];


		const data_Security = {
			// 상위 컴포넌트에서 
			labels: ['보안'],
			
			datasets: [
				
					//보안
					{
						label: 'police',
						labelColor : '#2E294E',
						backgroundColor: '#2E294E',
						borderColor: 'rgba(35, 27, 88, 0.514)',
						borderWidth: 1,
						hoverBackgroundColor:'#2e294e83',
						
						data: [policeData] // 수정 요함 

					},

					{
						label: 'light',
						labelColor : '#9055A2',
						backgroundColor: '#9055A2',
						borderColor: 'rgba(209, 82, 152, 0.918)',
						borderWidth: 1,
						hoverBackgroundColor:'rgba(209, 82, 152, 0.363)',
						
						data: [lightData] // 수정 요함 

					},

					{
						label: 'CCTV',
						labelColor : '#d499b9f5',
						backgroundColor: '#d499b9f5',
						borderColor: '#d481afea',
						borderWidth: 1,
						hoverBackgroundColor:'#d499b998',
						
						data: [cctvData] // 수정 요함 

					}
				
			]
		};




		const data_life = {
			// 상위 컴포넌트에서 
			labels: ['생활'],
			
			datasets: [
				
				{
					label: 'park',
					labelColor : '#FFEEE4',
					backgroundColor: '#FFEEE4',
					borderColor: '#f8d2bc',
					borderWidth: 1,
					hoverBackgroundColor:'#ffeee49d',
					
					data: [parkData] // 수정 요함 

				},

				{
					label: 'pharmacy',
					labelColor : '#F17F42',
					backgroundColor: '#F17F42',
					borderColor: 'rgb(248, 157, 104)',
					borderWidth: 1,
					hoverBackgroundColor:'#f17f428f',
					
					data: [pharmacyData] // 수정 요함 

				},

				{
					label: 'market',
					labelColor : 'rgba(255, 202, 104, 0.938)',
					backgroundColor: 'rgba(255, 202, 104, 0.938)',
					borderColor: 'rgba(248, 175, 38, 0.938)',
					borderWidth: 1,
					hoverBackgroundColor:'rgba(255, 202, 104, 0.3)',
					
					data: [marketData] // 수정 요함 

				},
				
			]
		};



		const data_culture = {
			// 상위 컴포넌트에서 
			labels: ['문화'],
			
			datasets: [
				
				{
					label: 'library',
					labelColor : '#CADBE9',
					backgroundColor: '#CADBE9',
					borderColor: 'rgba(116, 118, 211, 0.418)',
					borderWidth: 1,
					hoverBackgroundColor:'rgba(97, 99, 207, 0.199)',
					
					data: [libraryData] // 수정 요함 

				},

				{
					label: 'sports',
					labelColor : '#8EC0E4',
					backgroundColor: '#8EC0E4',
					borderColor: 'rgba(81, 164, 224, 0.478)',
					borderWidth: 1,
					hoverBackgroundColor:'#8ec0e47a',
					
					data: [sportsData] // 수정 요함 

				},

				{
					label: 'gallery',
					labelColor : '#D4DFE6',
					backgroundColor: '#D4DFE6',
					borderColor: 'rgba(157, 196, 219, 0.557)',
					borderWidth: 1,
					hoverBackgroundColor:'#d4dfe68e',
					
					data: [artData] // 수정 요함 

				},

				{
					label: 'concert',
					labelColor : '#6AAFE6',
					backgroundColor: '#6AAFE6',
					borderColor: '#3a97e4d0',
					borderWidth: 1,
					hoverBackgroundColor:'#6aaee6a4',
					
					data: [concertData] // 수정 요함 

				},
				
			]
		};

		const data_traffic = {
			// 상위 컴포넌트에서 
			labels: ['교통'],
			
			datasets: [
				
				{
					label: 'bus',
					labelColor : '#cff0da',
					backgroundColor: '#cff0da',
					borderColor: '#93e4ae',
					borderWidth: 1,
					hoverBackgroundColor:'#cff0da9c',
					
					data: [busData] // 수정 요함 

				},

				{
					label: 'subway',
					labelColor : '#88dba3',
					backgroundColor: '#88dba3',
					borderColor: '#57d17f',
					borderWidth: 1,
					hoverBackgroundColor:'#88dba483',
					
					data: [subwayData] // 수정 요함 

				},

				
			]
		};


		return (
			<div className="graph">
				<div className="graph-title">
				<span className="line-dongtotal" /><div className="title"> {this.props.guName} 통합 차트</div>  
				
				</div> 
				<div>
					<div className="barcontainer">
						<Bar  data={data_Security} options={options} width={230} height={300}/>
					</div>

					<div className="barcontainer">
						<Bar data={data_life} options={options} width={230} height={300}/>
					</div>

					<div className="barcontainer">
						<Bar  data={data_culture} options={options} width={230} height={300}/>
					</div>

					<div className="barcontainer">
						<Bar  data={data_traffic} options={options} width={230} height={300}/>
					</div>
				</div>

			</div>
		);
	}
}

export default BarDongTotal;