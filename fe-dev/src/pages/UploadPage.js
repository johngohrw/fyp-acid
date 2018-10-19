import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import '../css/pages/uploadpage.css';


class UploadPage extends Component {
    
    constructor(props) {
        super(props);

        this.fileHandler = this.fileHandler.bind(this);
        this.uploadHandler = this.uploadHandler.bind(this);

        this.state = {
            files: null
        };
    };

    // send file array to parent component
    fileHandler(filearray) {
        console.log('parent receive file array', filearray)
        this.setState({
            files: filearray
        });

        // send to parent
        this.props.receiveFiles(filearray)
    }

    // trigger route when upload button is pressed
    uploadHandler() {
        console.log('push \'/results\' to history!')
        this.props.history.push("/results")
    }

    render() {
        return (
            <div className="upload-page__container">
                <div className="inner-content">
                    <h4>Upload your images</h4> 
                    <p>
                        You can provide multiple files at a time by selecting while holding down the Shift key!
                    </p>
                    <FileUpload receiveFiles={this.fileHandler} onClickUpload={this.uploadHandler}/>
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


export default withRouter(UploadPage)