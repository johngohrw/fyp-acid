import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/resultspage.css';


export default class ResultsPage extends Component {

    constructor(props) {
        super(props);

        this.state = {
            files: null,
            responses: []
        };

    };

    componentDidMount() {
        document.getElementsByClassName('results-list')[0].innerHTML = "Retrieving images.."
        console.log('results component mount! probing for results:',this.props)
        var resultsProbe = setInterval(() => {
            if (this.props.files !== null ) {
                this.setState({files: this.props.files})
                this.setState({responses: this.props.reponses})
                clearInterval(resultsProbe)
                this.loadResults()
            }
        },100) 
    }

    // push images to result list
    loadResults() {

        if (this.state.files === null) {
            document.getElementsByClassName('results-list')[0].innerHTML = "Failed to load images"
            return
        } else {
            document.getElementsByClassName('results-list')[0].innerHTML = ""
        }

        console.log('load images!');

        for (let i = 0; i < this.state.files.length; i++) {
            var div = document.getElementsByClassName('results-list')
            var resultcontainer = document.createElement("div");
            resultcontainer.className = "result-item";
            resultcontainer.id = "ri" + i;

            var imgcontainer = document.createElement("div");
            imgcontainer.className = "result-item-img-container";

            var textcontainer = document.createElement("div");
            textcontainer.className = "result-item-text-container";

            var img = document.createElement("img");
            img.src = this.state.files[i];
            img.className = "results--image"

            var text1 = document.createElement("p");
            text1.className = "results--text"
            text1.innerHTML = "Model: " + this.props.responses[i].model  
            
            var text2 = document.createElement("p");
            text2.className = "results--text"
            text2.innerHTML = "Prediction: " + this.props.responses[i].prediction

            imgcontainer.appendChild(img);
            textcontainer.appendChild(text1);
            textcontainer.appendChild(text2);
            resultcontainer.appendChild(imgcontainer);
            resultcontainer.appendChild(textcontainer);
            div[0].appendChild(resultcontainer);
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
