import React from "react";
import { Router, Route, IndexRoute } from "react-router";
import { history } from "./store.js";
import App from "./components/App";
import Home from "./components/Home";
import Dashboard from "./components/Dashboard";
import CreateFeedbackForm from "./components/CreateFeedbackForm";
import ViewForms from "./components/common/ViewForms";
import UserEdit from "./components/UserEdit";
import ClassDetails from "./components/ClassDetails";
import NotFound from "./components/NotFound";

// build the router
const router = (
  <Router onUpdate={() => window.scrollTo(0, 0)} history={history}>
    <Route path="/" component={App}>
      <IndexRoute component={Dashboard}/>
      <Route path="home" component={Home}/>
      <Route path="create-form" component={CreateFeedbackForm}/>
      <Route path="view-forms" component={ViewForms}/>
      <Route path="user-edit(/:id)" component={UserEdit}/>
      <Route path="class" component={ClassDetails}/>
      <Route path="*" component={NotFound}/>
    </Route>
  </Router>
);

// export
export { router };
