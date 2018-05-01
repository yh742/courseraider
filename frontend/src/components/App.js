import React from "react";
import { connect } from "react-redux";
import { ProgressBar } from "react-bootstrap";
import Menu from "./common/Menu";
import "../stylesheets/main.scss";
import imgSrc from '../assets/course-raider-logo.jpg';
import { CirclePie } from 'salad-ui.chart';
import Alert from 'react-s-alert';

import 'react-s-alert/dist/s-alert-default.css';
import 'react-s-alert/dist/s-alert-css-effects/slide.css';

// App component
export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      conentWrapperMaxHeight: "0px"
    }
  }

  // pre-render logic
  componentWillMount() {
    // the first time we load the app, we need that users list
    this.props.dispatch({type: 'USERS_FETCH_LIST'});
  }

  componentDidMount() {
      this.setState({conentWrapperMaxHeight: window.innerHeight - 80});
   }

  // render
  render() {
    // show the loading state while we wait for the app to load
    const {users, children} = this.props;
    if (!users.length) {
      return (
        <ProgressBar active now={100}/>
      );
    }

    // render
    return (
      <div className="">
        <div className="header-container">
          <div className="logo-container" href="/">
            <img src={imgSrc} />
          </div>
          <div className="title-container">
          </div>
        </div>
        <div className="mn-container">
          <div className="sidebar-container" style={{maxHeight: this.state.conentWrapperMaxHeight}}>
            <Menu/>
            <div className="donut-chart-container">
              <div className="donut-chart-header" >
                Aggregate Feedback Score
              </div>
              <CirclePie
                width={175}
                height={175}
                strokeWidth={30}
                percent={65}
                strokeColor="#8F85E8"
                labelColor="#eee"
              />
            </div>
          </div>
          <Alert stack={{limit: 3}} />
          <div className="routes-container" style={{maxHeight: this.state.conentWrapperMaxHeight}}>{children}</div>
        </div>
      </div>
    );
  }
}

// export the connected class
function mapStateToProps(state) {
  return {
    users: state.users || [],
  };
}
export default connect(mapStateToProps)(App);
