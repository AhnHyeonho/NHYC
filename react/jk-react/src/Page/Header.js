import React from 'react';
import './Header.css';
import logo from '../Img/logo.png'
class Header extends React.Component{

    render(){
        return <div className="app-header">
            <img src={logo} className="header logo"></img>
            <a href="/about" className="header about">About</a>
            <a href="/map" className="header map">Map</a>
            <a href="#" className="header graph">Graph</a>
            <a href="#" className="header info">Info</a>
            </div>
    }
}

{/*<a style={{'text-decoration': "none" }} href="/about" className="header about">About</a>*/}




export default Header;