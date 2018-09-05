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
                {/* <form method="post" enctype="multipart/form-data"> */}
                    {/* <div>
                        <label for="image_uploads">Choose images to upload (PNG, JPG)</label>
                        <input type="file" id="image_uploads" name="image_uploads" accept=".jpg, .jpeg, .png" multiple />
                    </div>
                    <div className="preview">
                        <p>No files currently selected for upload</p>
                    </div>
                    <div>
                        <button>Submit</button>
                    </div>         */}
                    <div>
                        <FileUpload />
                    </div>

                    <div>
                        <Link to="/">Back</Link>
                    </div>
                {/* </form> */}
            </div>
        );
    };

    
};