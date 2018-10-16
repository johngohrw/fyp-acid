import React, { Component } from 'react';
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
                <h5 className="tagline">automatic compound image detection</h5>
           </div>
        );
    };
};

