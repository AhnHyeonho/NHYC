import React, { Component } from 'react'

class TableGraph extends React.Component{
    constructor(props) {
        super(props);
        this.getRankData = this.getRankData.bind(this);
        this.state = {
            sdData : 'rent',
            deposit_rent : [],
            gu_rent:[],
            rental_rent:[],
            deposit_depo : [],
            gu_depo:[],
            rental_depo:[]
        }
    }

    handleSDData = (event) =>
        this.setState({sdData : event.target.value});


    getRankData(guName){
        if(guName =="서울시"){
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getRankingChartData/rent/')
            .then(res => res.json())
            .then(json => this.setState({deposit_rent:json.deposit, gu_rent:json.gu, rental_rent:json.rentalFee }))

            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getRankingChartData/depo/')
            .then(res => res.json())
            .then(json => this.setState({deposit_depo:json.deposit, gu_depo:json.gu, rental_depo:json.rentalFee }))
        }else{
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getRankingChartData/rent/'+guName)
            .then(res => res.json())
            .then(json => this.setState({deposit_rent:json.deposit, gu_rent:json.gu, rental_rent:json.rentalFee }))
            
            fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/getRankingChartData/depo/'+guName)
            .then(res => res.json())
            .then(json => this.setState({deposit_depo:json.deposit, gu_depo:json.gu, rental_depo:json.rentalFee }))

        }

    }

    
    componentDidMount(){
        this.getRankData(this.props.name);
    }







    render(){
        var local;
        var rent;
        var depo;
        if(this.state.sdData == "rent"){
            local = this.state.gu_rent;
            rent = this.state.rental_rent;
            depo = this.state.deposit_rent;
        }else{
            local = this.state.gu_depo;
            rent = this.state.rental_depo;
            depo = this.state.deposit_depo;
        }


        console.log(this.state.deposit_rent);



        return(
            <div className="graph">
                <div className="graph-title">
                    <span className="line" /><div className="title">{this.props.name} 월세/보증금 순위</div>
                    <select className ="selection_Graph" onChange={this.handleSDData}>
                        <option value="rent">월세순</option>
                        <option value="depo">보증금순</option>
                     </select>
            



                    <table className="table table-hover">
                        <thead>
                        <tr>
                            <th>순위</th>
                            <th>지역</th>
                            <th>월세</th>
                            <th>보증금</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>1</td>
                            <td>{local[0]}</td>
                            <td>{rent[0]}만원</td>
                            <td>{depo[0]}만원</td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>{local[1]}</td>
                            <td>{rent[1]}만원</td>
                            <td>{depo[1]}만원</td>
                        </tr>
                        <tr>
                            <td>3</td>
                            <td>{local[2]}</td>
                            <td>{rent[2]}만원</td>
                            <td>{depo[2]}만원</td>
                        </tr>

                        <tr>
                            <td>4</td>
                            <td>{local[3]}</td>
                            <td>{rent[3]}만원</td>
                            <td>{depo[3]}만원</td>
                        </tr>

                        <tr>
                            <td>5</td>
                            <td>{local[4]}</td>
                            <td>{rent[4]}만원</td>
                            <td>{depo[4]}만원</td>
                        </tr>
                        </tbody>
                    </table>













                </div>
            </div>
        )
    }


}



export default TableGraph;