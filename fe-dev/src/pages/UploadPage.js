import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import '../css/pages/uploadpage.css';

export default class UploadPage extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            someState: 'haha'
        };
    };

    render() {
        return (
            <div className="upload-page__container">
                uplload pAGE
            </div>
        );
    };
};