import React, { Component } from 'react';

export default class SampleComponent extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            someState: 'haha'
        };
    }
    
    render() {
        return (
           <div>
               SampleComponent
           </div>
        );
    };
};

