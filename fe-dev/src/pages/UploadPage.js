import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
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
                <div className="inner-content">
                    <div>
                        <FileUpload />
                    </div>
                </div>
                <div className="button-row">
                    <div>
                        <Link to="/">
                            <button className="btn btn-danger">Back</button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    };

    
};