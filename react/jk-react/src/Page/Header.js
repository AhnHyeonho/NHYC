import React from 'react';
import './Header.css';
import logo from '../Img/logo.png'
class Header extends React.Component {

    render() {
        return (
            <div className="header-block">
                
                {/* 로고 */}
                <div className="header logo">Hanbang</div>
                {/* 버튼 묶음 */}
                <div className="header buttons">
                    <a href="/about" className="header item">About</a>
                    <a href="/map" className="header item">Map</a>
                    <a href="/recommand" className="header item">Recommand</a>
                    <a href="#" className="header item">Info</a>
                </div>
            </div>
        )
    }
}

export default Header;