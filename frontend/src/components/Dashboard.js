import React from "react";
import ReactHighcharts from "react-highcharts";
import { push } from "react-router-redux";
import { connect } from "react-redux";
import BarHistoChart from './BarHistoChart';

// Dashboard component
export class Dashboard extends React.Component {

  // render
  render() {
    const {dispatch} = this.props;
    const areaChartConfig = {
      chart: {
        type: 'area'
      },
      credits: {
            enabled: false
      },
      title: {
        text: 'Student Feedback'
      },
      subtitle: {
        text: ''
      },
      xAxis: {
        categories: ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'],
        tickmarkPlacement: 'on',
        title: {
          enabled: false
        }
      },
      yAxis: {
        categories: [0, 1, 2, 3, 4, 5],
        title: {
          text: 'Average Score'
        }
      },
      exporting: {
       buttons: {
         contextButton: {
                    enabled: false
            }
         }
      },
      tooltip: {
        split: true,
        valueSuffix: ''
      },
      plotOptions: {
        area: {
          stacking: 'normal',
          lineColor: '#666666',
          lineWidth: 1,
          marker: {
            lineWidth: 1,
            lineColor: '#666666'
          }
        },
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function () {
                        return new Promise((resolve, reject) => {
                          dispatch({
                            type: 'SET_SELECTED_CLASS',
                            classes: {
                              class_Id: this.category
                            },
                            callbackError: (error) => {
                              reject(new SubmissionError({_error: error}));
                            },
                            callbackSuccess: () => {
                              dispatch(push('/class'));
                              resolve();
                            }
                          });
                        });
                    }
                }
            }
        }
      },
      series: [{
        name: 'Difficulty',
        data: [3.92, 4.16, 3.88, 2.92, 2.14]
      }, {
        name: 'Interest',
        data: [3.8, 3.96, 3.92, 2.94, 1.98]
      }, {
        name: 'Helpfulness',
        data: [4.1, 4, 3.12, 2.92, 1.98]
      }, {
        name: 'Satisfaction',
        data: [3.96, 4.02, 3.92, 2.9, 1.94]
      }]
    };

    return (
      <div className="">
        <div className="chart-container">
          <ReactHighcharts config={areaChartConfig}/>
        </div>
        <BarHistoChart />
      </div>
    );
  }

}

export default connect()(Dashboard);
