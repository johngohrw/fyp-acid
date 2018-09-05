import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/welcomepage.css';


export default class WelcomePage extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            someState: 'haha'
        };
    };

    render() {
        return (
            <div className="welcome-page__container">
                <h1>Hallo!</h1>
                <p>Welcome to FYP ACID</p>
                <div>
                    <Link to="/upload">Next</Link>
                </div>
            </div>
        );
    };
};
