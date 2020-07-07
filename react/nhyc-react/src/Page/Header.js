import React from 'react';
import './Header.css';
import logo from '../Img/logo.png'
import KakaoLogin from 'react-kakao-login';
import styled from 'styled-components';


class Header extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            id:'',
            name:'',
            provider:'',
        }

    }


    responseKakao = (res) => {
        this.setState({
            id : res.profile.id,
            name:res.profile.properties.nickname,
            provider:'kakao'
        })
        console.log(res);
        console.log(res.response["access_token"]);
        


    }

    responseFail = (err) =>{
        console.error(err);
    }


    render(){
        return <div className="app-header">
            <a href="/about" className="header logo">HanBang</a>
            <a href="/about" className="header about">About</a>
            <a href="/map" className="header map">Map</a>
            <a href="/recommand" className="header graph">Recomend</a>
            <a href="/login" className="header login">Login</a>
            {/* <KakaoButton jsKey="5a1110517c8e6aeb882b96ddc23779e3" buttonText="Kakao" 
            onSuccess={this.responseKakao} onFailure={this.responseFail} getProfile="true"/> */}
            
            {/*<a href="#" className="header info">Join</a>*/}
            
            </div>
    }
}


const KakaoButton = styled(KakaoLogin)`
    padding :0;
    width:190px;
    hegiht:44px;
    line-height:44px;
    color : #783c00;
    background-color:#FFEB00;
    border:1px solid transparent;
    border-radius:3px;
    font-size:16px;
    font-weight:bold;
    text-align:center;
`







export default Header;