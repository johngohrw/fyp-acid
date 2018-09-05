import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/welcomepage.css';


export default class WelcomePage extends Component {

    render() {
        return (
            <div className="welcome-page__container">
                <div className="inner-content">
                    <h4>Hallo!</h4>
                    <p>Welcome to FYP ACID</p>
                </div>
                <div className="button-row">
                    <Link to="/template-test">
                        <button className="btn btn-info">Test</button>   
                    </Link>
                    <Link to="/upload">
                        <button className="btn btn-success">Next</button>
                    </Link>
                </div>
            </div>
        );
    };
};
