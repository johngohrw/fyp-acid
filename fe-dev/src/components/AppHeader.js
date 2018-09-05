import React, { Component } from 'react';
import '../css/components/AppHeader.css';

export default class AppHeader extends Component {
    
    render() {
        return (
           <div className="app-header">
               <h1>App Header</h1>
               <h4>subtitle goes here lorem ipsum</h4>
           </div>
        );
    };
};

