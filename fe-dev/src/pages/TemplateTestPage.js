import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/testpage.css';


export default class TemplateTestPage extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            someState: 'haha'
        };
    };

    render() {
        return (
            <div className="test-page__container">
                <div className="inner-content">
                    <h1>Hallo!</h1>
                    <p>Welcome to FYP ACID</p>
                    <h1>H1 goes here</h1>
                    <h2>H2 goes here</h2>
                    <h3>H3 goes here</h3>
                    <h4>H4 goes here</h4>
                    <h5>H5 goes here</h5>
                    <h6>H6 goes here</h6>
                    <p>p goes here</p>
                </div>
                <div className="button-row">
                    <Link to="/">
                        <button className="btn btn-danger">Back</button>
                    </Link>
                </div>
            </div>
        );
    };
};
