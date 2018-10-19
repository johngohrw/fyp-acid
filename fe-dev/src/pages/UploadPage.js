import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import '../css/pages/uploadpage.css';


export default class UploadPage extends Component {
    
    constructor(props) {
        super(props);

        this.fileHandler = this.fileHandler.bind(this);

        this.state = {
            files: null
        };
    };


    fileHandler(filearray) {
        console.log('parent receive file array', filearray)
        this.setState({
            files: filearray
        });

        // send to parent
        this.props.receiveFiles(filearray)
    }

    render() {
        return (
            <div className="upload-page__container">
                <div className="inner-content">
                    <h4>Upload your images</h4> 
                    <p>
                        You can provide multiple files at a time by selecting while holding down the Shift key!
                    </p>
                    <FileUpload receiveFiles={this.fileHandler} />
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