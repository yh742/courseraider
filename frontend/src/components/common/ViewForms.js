import React from "react";
import FormComponent from "./FormComponent";

// ViewForms Parent Component
export default class ViewForms extends React.Component {
  constructor(props) {
    super(props);

    // default ui local state
    this.state = {};

    // bind <this> to the event method
    // this.removeElement = this.props.removeElement.bind(this);
  }


// render
  render() {
    const { type, id, removeElement, labelUpdate, optionsUpdate } = this.props;
    return (
      <div className="dynamic-element-container">
        <FormComponent />
      </div>
    );
  }

}
