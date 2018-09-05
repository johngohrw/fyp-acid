import React, { Component } from 'react';
import axios from 'axios';
import '../css/components/FileUpload.css'

export default class FileUpload extends Component {

    constructor(props) {
        super(props);
          this.state = {
            uploadStatus: false
          }
        this.handleUploadImages = this.handleUploadImages.bind(this);
      }
    
    
      handleUploadImages(ev) {
        ev.preventDefault();
    
        let fileList = [];

        for (let i=0; i < this.uploadInput.files.length; i++) {
            fileList.push(this.uploadInput.files[i]); // to keep track locally

            const data = new FormData();
            data.append('file', this.uploadInput.files[i])
            axios.post('http://localhost:5000/api/v0/ocr', data)
                .then(function (response) {
                    console.log(response);
                    // this.setState({ imageURL: `http://localhost:8000/${response.body.file}`, uploadStatus: true });
                })
                .catch(function (error) {
                    console.log(error);
                }
            );
        }
      }
      
   render() {
     return(
        <div className="uploader-container">
            <h4>Upload your shit</h4>
         <form onSubmit={this.handleUploadImages}>
           <div className="form-group">
             <input className="form-control"  ref={(ref) => { this.uploadInput = ref; }} type="file" multiple/>
           </div>
 
           <button className="btn btn-success" type>Upload</button>
         </form>
       </div>
     )
   }
 }