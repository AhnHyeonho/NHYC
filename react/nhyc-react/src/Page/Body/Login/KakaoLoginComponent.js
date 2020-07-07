
import React from 'react';

import KakaoLogin from 'react-kakao-login';
import styled from 'styled-components';


export class KaKaoLoginComponent extends React.Component{

    constructor(props){
        super(props);
        
        this.state = {
            id:'',
            name:'',
            provider:'',
            token : '',
            postId :''
        }

    }

    


    responseKakao = (res) => {
        this.setState({
            id : res.profile.id,
            name:res.profile.properties.nickname,
            provider:'kakao'
        })
        // console.log(res);
        // console.log(res.response["access_token"]);
        this.setState({token:res.response["access_token"]});
        


    }

    responseFail = (err) =>{
        console.error(err);
    }




    componentDidMount() {
        // Simple POST request with a JSON body using fetch
        
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ access_token: this.state.token })
        };

        fetch('http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/api/auth/kakaoLogin/', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ postId: data.id }));
    }


    

    render(){

        console.log(this.state.token);


        return(
            
            <div>
                <KakaoButton jsKey="5a1110517c8e6aeb882b96ddc23779e3" buttonText="Login with Kakao" 
                onSuccess={this.responseKakao} onFailure={this.responseFail} getProfile="true"/>
            </div>

        ); 
        

                 


    }
}


const KakaoButton = styled(KakaoLogin)`
    padding :0;
    width:380px;
    hegiht:20px;
    line-height:35px;
    color : #783c00;
    background-color:#FFEB00;
    border:1px solid transparent;
    border-radius:3px;
    font-size:14px;
    font-weight:bold;
    text-align:center;
    margin-bottom:10px;
`






export default KaKaoLoginComponent;