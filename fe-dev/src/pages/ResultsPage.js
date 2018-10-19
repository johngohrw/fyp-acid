import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/resultspage.css';


export default class ResultsPage extends Component {

    constructor(props) {
        super(props);

        this.state = {
            files: null
        };

    };

    componentDidMount() {
        console.log('results component mount! probing for 3 seconds:',this.props)
        var probe = setInterval(() => {
            this.setState({files: this.props.files})
        },100)

        setTimeout(() => {
            clearInterval(probe)
            this.loadImages()
        },3000)
    }

    // push images to result list
    loadImages() {
        console.log('load images!');

        for (let i = 0; i < this.state.files.length; i++) {
            var div = document.getElementsByClassName('results-list')
            var imgcontainer = document.createElement("div");
            imgcontainer.className = "result-item";
            imgcontainer.id = "ri" + i;

            var img = document.createElement("img");
            img.src = this.state.files[i];
            img.className = "results"

            imgcontainer.appendChild(img);
            div[0].appendChild(imgcontainer);
        }
    }

    render() {
        return (
            <div className="results-page__container">
                <div className="inner-content">
                    <h4>Results</h4>
                    <div className="results-list">
                    
                    </div>
                </div>
                <div className="button-row">
                    <Link to="/">
                        <button className="btn btn-success">Back to Home</button>
                    </Link>
                </div>
            </div>
        );
    };
};
