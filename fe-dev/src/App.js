import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import UploadPage from './pages/UploadPage';


import CssBaseline from '@material-ui/core/CssBaseline';
import './css/app.css';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <div className="container">
          <Router>
            <div className="content">
              <Route exact path='/' component={UploadPage}/>
            </div>
          </Router>
        </div>
      </React.Fragment>
    );
  }
}

export default App;
