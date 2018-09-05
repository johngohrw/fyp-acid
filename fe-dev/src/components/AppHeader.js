import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/components/AppHeader.css';

export default class AppHeader extends Component {

    constructor(props) {
        super(props);
        this.state = { x: 10, y: 10 };
    };
    
    render() {
        return (
           <div className="app-header">
                <div onMouseMove={(e) => {
                    this.setState({ x: e.screenX, y: e.screenY})
                }}>
                    <h1>acid</h1>
                </div>
               <div className="app-header__nav">
                    <h6>
                        <Link to="/"> link1 </Link>/
                        <Link to="/"> link2 </Link>/ 
                        <Link to="/"> link3 </Link>/ 
                        <Link to="/"> link4 </Link> 
                    </h6>
               </div>
           </div>
        );
    };
};

