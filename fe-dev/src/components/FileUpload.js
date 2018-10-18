import React, { Component } from 'react';
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';
import axios from 'axios';
import '../css/components/FileUpload.css'

export default class FileUpload extends Component {

    constructor(props) {
        super(props);
          this.state = {
            uploadStatus: false,
            mode: null
          }
        this.handleUploadImages = this.handleUploadImages.bind(this);
      }

      handleChange(e) {
        this.setState({mode: e.target.value});
      }
      
      handleUploadImages(ev) {
        ev.preventDefault();

        var param = this.state.mode
        
        if (param === 'Linear SVM') { param = 'linear' } 
        else if (param === 'RBF SVM') { param = 'rbf' } 
        else if (param === 'KNN') { param = 'knn' } 
        else if (param === 'Linear SVM + RBF SVM + KNN') { param = 'linear,rbf,knn' }

        let endpoint = 'http://localhost:5000/api/v0/classify?model=' + param
        console.log('Endpoint: ', endpoint)
    
        let fileList = [];
        for (let i = 0; i < this.uploadInput.files.length; i++) {
          fileList.push(this.uploadInput.files[i]); // to keep track locally

          const data = new FormData();
          data.append('file', this.uploadInput.files[i])
          console.log(data)
          axios.post(endpoint, data)
            .then(function (response) {
              console.log("fileupload: img response:", response);
            })
            .catch(function (error) {
              console.log(error);
            });
        }
        console.log(fileList)
      }

      
   render() {

    var uploadButton;
    if (this.state.mode === null || this.state.mode === "select a method") {
      uploadButton = <Button className="btn btn-success" disabled>Upload</Button>
    } else {
      uploadButton = <Button className="btn btn-success" >Upload</Button>
    }
     return(
        <div className="uploader-container">
          <Form onSubmit={this.handleUploadImages}>
            <FormGroup>
              <input className="form-control"  ref={(ref) => { this.uploadInput = ref; }} type="file" multiple />
            </FormGroup>
            <FormGroup>
              <Label for="mode">Select Mode</Label>
              <Input type="select" name="mode" id="mode" defaultValue="select a method" onChange={(e) => {this.handleChange(e)}}>
                <option disabled>select a method</option>
                <option>Linear SVM</option>
                <option>RBF SVM</option>
                <option>KNN</option>
                <option>Linear SVM + RBF SVM + KNN</option>
              </Input>
            </FormGroup>
            {uploadButton}
          </Form>
        </div>
     )
   }
 }