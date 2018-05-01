import React from "react";
import _ from 'lodash';
import DynamicFormElement from "./common/DynamicFormElement.js";
import Alert from 'react-s-alert';


// CreateFeedbackForm component
export default class CreateFeedbackForm extends React.Component {
  constructor(props) {
    super(props);

    // default ui local state
    this.state = {
      title: '',
      description: '',
      type: "object",
      required: [],
      properties: {},
      elements: [],
      UISchema: {},
      ctr: 0
    };

    // bind <this> to the event method
    this.addElement = this.addElement.bind(this);
    this.removeElement = this.removeElement.bind(this);
    this.labelUpdate = this.labelUpdate.bind(this);
    this.optionsUpdate = this.optionsUpdate.bind(this);
    this.saveForm = this.saveForm.bind(this);
    this.generateUISchema = this.generateUISchema.bind(this);
  }
  // render
  render() {
    // console.log(this.state.properties, 'new properties');
    const formElements = [];
    this.state.elements.forEach((elem, i) => {
      formElements.push(<DynamicFormElement key={i} id={elem.id} radio={elem.radio} removeElement={this.removeElement} labelUpdate={this.labelUpdate} optionsUpdate={this.optionsUpdate} type={elem.type} />);
    });
    return (
      <div className="page-home">
        <div className="create-form-container">
          <div className="create-form-play-area">
            <div className="form-title-input">
              <label>Title:</label> <input className="form-control question-label-input" onBlur={(evt) => { this.setState({ title: evt.target.value});}} />
            </div>
            <div className="form-title-input">
              <label>Description:</label> <input className="form-control question-label-input" onBlur={(evt) => { this.setState({ description: evt.target.value});}} />
            </div>
            { formElements }
          </div>
          <div className="create-form-toolbox">
            <h4 className="toolbox-header">Tool Box</h4>
            <ul>
              <li><span>Radio Button</span> <span><button className="btn btn-info" onClick={() => this.addElement('string', true)}>Add</button></span></li>
              <li><span>Text</span> <span><button className="btn btn-info" onClick={() => this.addElement('string', false)}>Add</button></span></li>
            </ul>
          </div>
        </div>
        <button type="button" onClick={() => this.saveForm()} className="btn btn-success">Save!</button>
      </div>
    );
  }

  addElement(type, radioFlag) {
    const elemId = type + this.state.ctr;
    const newObj = {
      type: type,
      id: elemId,
      radio: radioFlag
    }

    let newPropObj = Object.assign(this.state.properties);
    newPropObj[elemId] = {
      type: type,
      title: ''
    }

    const updatedElementsList = this.state.elements;
    updatedElementsList.push(newObj);
    this.setState({
      elements: updatedElementsList,
      ctr: (this.state.ctr + 1),
      properties: newPropObj
    });
  }

  removeElement(id) {
    const updatedElementsList = this.state.elements;
    const newPropsObj = Object.assign(this.state.properties);
    delete newPropsObj[id];
    this.setState({
      elements: _.remove(updatedElementsList, (elem) => { return elem.id !== id; }),
      properties: newPropsObj
    });
  }

  labelUpdate(id, newLabel) {
    let newPropObj = Object.assign(this.state.properties);
    newPropObj[id]['title'] = newLabel;
    this.setState({
      properties: newPropObj
    });
  }

  optionsUpdate(id, updatedOptions) {
    let newPropObj = Object.assign(this.state.properties);
    newPropObj[id]['enum'] = updatedOptions.split(',');
    newPropObj[id]['type'] = "string";
    this.setState({
      properties: newPropObj
    });
  }

  saveForm() {
    // Check to see if title has been written
    // Check to see if there is atleast one question in the form
    let UISchema = null;
    if (this.state.elements.length < 1) {
      Alert.error('Please add atleast 1 question', {
              position: 'top-right',
              effect: 'slide',
              timeout: 2000
          });
    }

    if (this.state.title.length < 1) {
      Alert.error('Please provide a title', {
              position: 'top-right',
              effect: 'slide',
              timeout: 2000
          });
    }

    if (!(this.state.title.length < 1 || this.state.elements.length < 1)) {
      UISchema = this.generateUISchema();

      const formSchema = {
        title: this.state.title,
        properties: this.state.properties,
        description: this.state.description,
        type: this.state.type
      }

      this.setState({
        UISchema: UISchema
      });
    }

  }

  generateUISchema() {
    let UISchema = {};
    this.state.elements.forEach((elem, i) => {
      UISchema[elem.id] = {
        'ui:widget': elem.radio ? 'radio' : 'textarea'
      }
    });
    return UISchema;
  }

}
