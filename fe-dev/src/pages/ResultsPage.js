import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/resultspage.css';


export default class ResultsPage extends Component {

    render() {
        return (
            <div className="results-page__container">
                <div className="inner-content">
                    <h4>Results</h4>
                    <p>
                        ACID is an image classifier that is able to discriminate 
                        between compound and non-compound images from published 
                        sources in the biomedical field.  
                    </p>
                    <p>
                        We provide three different classification methods to apply 
                        onto your uploaded images, with each method providing varying
                        levels of accuracy.  
                    </p>
                    <p>
                        You can read more about our methodology in detail 
                        <Link to='/methodology'> here</Link>.
                    </p>
                </div>
                <div className="button-row">
                    {/* <Link to="/template-test">
                        <button className="btn btn-info">Test</button>   
                    </Link> */}
                    <Link to="/upload">
                        <button className="btn btn-success">Next</button>
                    </Link>
                </div>
            </div>
        );
    };
};
