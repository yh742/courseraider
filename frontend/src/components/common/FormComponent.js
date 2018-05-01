import React from "react";
import Form from "react-jsonschema-form";

// ViewForms Parent Component
export default class FormComponent extends React.Component {
  constructor(props) {
    super(props);

    // default ui local state
    this.state = {};

    // bind <this> to the event method
    // this.removeElement = this.props.removeElement.bind(this);
  }


  // render
  render() {
    const { schema } = this.props;
    const uiSchema = {
      "TV killed the radio star": {
        "malaysian_state": {
          "ui:widget": "radio"
        }
      }
    };

    const uiSchema2 = {
      "netid": {
        "ui:autofocus": true,
        "ui:emptyValue": ""
      },
      "feedback": {
        "ui:widget": "textarea"
      },
      "Question1": {
        "ui:widget": "radio"
      },
      "Question2": {
        "ui:widget": "radio"
      },
      "Question3": {
        "ui:widget": "radio"
      },
      "Question4": {
        "ui:widget": "radio"
      },
      "Question5": {
        "ui:widget": "radio"
      },
      "Question6": {
        "ui:widget": "radio"
      }
    };

    const dummySchema = {
      "type": "object",
      "properties": {
        "TV killed the radio star": {
          "title": "Your favourite state",
          "type": "object",
          "required": [
            "malaysian_state",
          ],
          "properties": {
            "malaysian_state": {
              "type": "string",
              "title": "Malaysian states",
              "enum": [
                "Kuala Lumpur",
                "Johor",
                "Kedah"
              ]
            }
          }
        },
        "title": {type: "string", title: "Title", default: "A new task"}
      }
    };

    const dummySchema2 = {
      "title": "Feedback Form",
      "description": "A simple feedback form",
      "type": "object",
      "required": [
        "netid"
      ],
      "properties": {
        "netid": {
          "type": "string",
          "title": "Netid"
        },
        "Question1": {
          "type": "string",
          "title": "Question 1",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "Question2": {
          "type": "string",
          "title": "Question 2",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "Question3": {
          "type": "string",
          "title": "Question 3",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "Question4": {
          "type": "string",
          "title": "Question 4",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "Question5": {
          "type": "string",
          "title": "Question 5",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "Question6": {
          "type": "string",
          "title": "Question 6",
          "enum": ["1", "2", "3", "4", "5"]
        },
        "feedback": {
          "type": "string",
          "title": "Feedback"
        }
      }
    }

    return (
      <div className="">
        <Form schema={schema || dummySchema2}
          uiSchema={uiSchema2}
          onChange={console.log("changed")}
          onSubmit={console.log("submitted")}
          onError={console.log("errors")} />
      </div>
    );
  }

}
