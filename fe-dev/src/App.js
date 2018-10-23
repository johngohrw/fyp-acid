import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import AppHeader from './components/AppHeader'
// import AppNav from './components/AppNav'

import UploadPage from './pages/UploadPage';
import WelcomePage from './pages/WelcomePage';
import TemplateTestPage from './pages/TemplateTestPage';
import MethodologyPage from './pages/MethodologyPage';
import ResultsPage from './pages/ResultsPage';

import CssBaseline from '@material-ui/core/CssBaseline';
import './css/app.css';
import './css/trippycircles.css';
import './css/trippybourbon.css';


class App extends Component {

  constructor(props) {
      super(props);

      this.fileHandler = this.fileHandler.bind(this);
      this.responseHandler = this.responseHandler.bind(this);

      this.state = {
          files: null,
          responses: []
      };
  };

  fileHandler(filearray) {
      console.log('app receive file array', filearray)
      this.setState({
          files: filearray
      });
  }

  responseHandler(responsearr) {
      console.log('app receive response array', responsearr)
      this.setState({
          responses: responsearr
      });
  }


  componentWillMount() {
    document.title = 'FYP ACID'; // changing doc title upon loading. 
  }

  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Router>
          <div className="main-container container">  
            <div className="trippybg">
              <ul className="trippycontainer">
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
                <li className="trippycircle"></li>
              </ul>
            </div>
            <AppHeader />
            {/* <AppNav {...this.props} /> */}
            <div className="content">
              <Route exact path='/' component={WelcomePage}/>
              <Route exact path='/fyp-acid' component={WelcomePage}/>
              <Route path='/fyp-acid/upload' 
                render={(props) => <UploadPage {...props} receiveResponses={this.responseHandler} receiveFiles={this.fileHandler} />}/>
            <Route path='/fyp-acid/template-test' component={TemplateTestPage}/>
              <Route path='/fyp-acid/methodology' component={MethodologyPage}/>
              <Route path='/fyp-acid/results' 
                render={(props) => <ResultsPage {...props} files={this.state.files} responses={this.state.responses}/>}/>
            </div>
          </div>
        </Router> 
      </React.Fragment>
    );
  }
}

export default App;

// eslint-disable-next-line
{/* <div className="bourbon-container">
  <div className="bourbon-ring el-1"></div>
  <div className="bourbon-ring el-2"></div>
  <div className="bourbon-ring el-3"></div>
  <div className="bourbon-ring el-4"></div>
  <div className="bourbon-ring el-5"></div>
  <div className="bourbon-ring el-6"></div>
  <div className="bourbon-ring el-7"></div>
  <div className="bourbon-ring el-8"></div>
  <div className="bourbon-ring el-9"></div>
  <div className="bourbon-ring el-10"></div>
  <div className="bourbon-ring el-11"></div>
  <div className="bourbon-ring el-12"></div>
  <div className="bourbon-ring el-13"></div>
  <div className="bourbon-ring el-14"></div>
  <div className="bourbon-ring el-15"></div>
  <div className="bourbon-ring el-16"></div>
  <div className="bourbon-ring el-17"></div>
  <div className="bourbon-ring el-18"></div>
  <div className="bourbon-ring el-19"></div>
  <div className="bourbon-ring el-20"></div>
  <div className="bourbon-ring el-21"></div>
  <div className="bourbon-ring el-22"></div>
  <div className="bourbon-ring el-23"></div>
  <div className="bourbon-ring el-24"></div>
  <div className="bourbon-ring el-25"></div>
  <div className="bourbon-ring el-26"></div>
  <div className="bourbon-ring el-27"></div>
  <div className="bourbon-ring el-28"></div>
  <div className="bourbon-ring el-29"></div>
  <div className="bourbon-ring el-30"></div>
</div> */}

// eslint-disable-next-line
{/* <ul className="trippycontainer">
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
  <li className="trippycircle"></li>
</ul> */}
