import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import AppHeader from './components/AppHeader'

import UploadPage from './pages/UploadPage';
import WelcomePage from './pages/WelcomePage';
import TemplateTestPage from './pages/TemplateTestPage';

import CssBaseline from '@material-ui/core/CssBaseline';
import './css/app.css';

class App extends Component {

  componentWillMount() {
    document.title = 'FYP ACID'; // changing doc title upon loading. 
  }

  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Router>
          <div className="main-container container">  
            <AppHeader />
            <div className="content">
              <Route exact path='/' component={WelcomePage}/>
              <Route path='/upload' component={UploadPage}/>
              <Route path='/template-test' component={TemplateTestPage}/>
            </div>
          </div>
        </Router> 
      </React.Fragment>
    );
  }
}

export default App;
