import React, { Component } from 'react';
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';
import axios from 'axios';
import '../css/components/FileUpload.css'

export default class FileUpload extends Component {

    constructor(props) {
        super(props);
          this.state = {
            uploadStatus: false,
            mode: null,
            files: [],
            responses: []
          }
        this.handleUploadImages = this.handleUploadImages.bind(this);
      }

      handleChange(e) {
        this.setState({mode: e.target.value});
      }
      
      handleUploadImages(ev) {
        ev.preventDefault();

        // get selected files from picker
        var files = document.getElementById('file-selector').files
        
        // check params
        var param = this.state.mode
        if (param === 'Linear SVM') { param = 'linear' } 
        else if (param === 'RBF SVM') { param = 'rbf' } 
        else if (param === 'KNN') { param = 'knn' } 
        else if (param === 'Linear SVM + RBF SVM + KNN') { param = 'linear,rbf,knn' }

        // set endpoint based on param
        let endpoint = 'http://localhost:5000/api/v0/classify?model=' + param
        console.log('Endpoint: ', endpoint)
        
        // initialise responses
        let responses = [];
        let numberOfFiles = this.uploadInput.files.length;

        // uploading files to backend
        let fileList = [];
        for (let i = 0; i < numberOfFiles; i++) {
          fileList.push(this.uploadInput.files[i]); // to keep track locally (?)
          const data = new FormData();
          data.append('file', this.uploadInput.files[i])
          console.log(data)
          axios.post(endpoint, data)
            .then(function (response) {
              console.log("fileupload: img response:", response);
              responses.push(response.data[0])
            })
            .catch(function (error) {
              console.log(error);
            });
        } 

        var imagedata = [];
        var reader = new FileReader();
        
        // recursive image reading
        const readNext = (imagedata, i, files, callback) => {
          if (i < files.length) {
            let f = files[i];
            reader.readAsDataURL(f)
            reader.onloadend = function (e) {
              imagedata.push(reader.result);
              i++;
              return readNext(imagedata, i, files, callback)
            }
          } else {
            return imageDataCallback(imagedata)
          }
        }

        const imageDataCallback = (imgarr) => {
          imagedata = imgarr;
        }
        
        // start reading
        readNext([], 0, files, imageDataCallback)
        
        // gather response from server
        var gatherResponses = setInterval(() => {
          console.log(responses.length, numberOfFiles)
          if (responses.length == numberOfFiles) {
            
            console.log('all files gathered!')
            clearInterval(gatherResponses);
            // this.setState({responses: responses});
            // setTimeout(()=>{ 
              console.log('read all image files!!', imagedata)
              console.log('child send array to parent')
              this.props.receiveFiles(imagedata)      // send images to parent component
              this.props.receiveResponses(responses) // send responses to parent component
              this.props.onClickUpload()            // trigger routechange

            // }, 2000)
          }
        },300) 
        

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
              <input className="form-control file-selector" id="file-selector" ref={(ref) => { this.uploadInput = ref; }} type="file" multiple />
            </FormGroup>
            <FormGroup>
              <Label for="mode">Classifier</Label>
              <Input type="select" name="mode" id="mode" defaultValue="select a classification model" onChange={(e) => {this.handleChange(e)}}>
                <option disabled>select a classification model</option>
                <option>Linear SVM</option>
                <option>RBF SVM</option>
                <option>KNN</option>
                <option>Linear SVM + RBF SVM + KNN</option>
              </Input>
            </FormGroup>
            {uploadButton}
          </Form>

          <div id="imgdisplay"></div>
        </div>
     )
   }
 }