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
    
      handleUploadImages(ev) {
        ev.preventDefault();

        let endpoint = 'http://localhost:5000/api/v0/' + this.state.mode.toLowerCase()
        console.log('Endpoint: ', endpoint)
    
        let fileList = [];

        for (let i=0; i < this.uploadInput.files.length; i++) {
            fileList.push(this.uploadInput.files[i]); // to keep track locally

            const data = new FormData();
            data.append('file', this.uploadInput.files[i])
            axios.post(endpoint, data)
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

      handleChange(e) {
        this.setState({mode: e.target.value});
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
                <option>OCR</option>
                <option>LBP</option>
                <option>shapes</option>
              </Input>
            </FormGroup>
            {uploadButton}
          </Form>
        </div>
     )
   }
 }