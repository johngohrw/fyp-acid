import React, { Component } from 'react';
import { Link , withRouter } from 'react-router-dom';
import '../css/components/AppNav.css';

class AppNav extends Component {

    constructor(props) {
        super(props);
        this.state = { x: 10, y: 10 };
    };

    componentDidMount() {
        updateNavStatus("mount", this.props.location.pathname);
    }

    componentDidUpdate() {
        updateNavStatus("up",this.props.location.pathname);
    }

    render() {
        return (
               <div className="app-header__nav">
                    <h6>
                        <Link to="/"> welcome </Link> >
                        <Link to="/upload"> upload </Link> > 
                        <Link to="/training"> training </Link> > 
                        <Link to="/results"> results </Link> 
                    </h6>
               </div>
        );
    };
};

const updateNavStatus = (pathname) => {
    console.log(pathname);
}

export default withRouter(AppNav)

