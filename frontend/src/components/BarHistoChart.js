import React from "react";
import ReactHighcharts from "react-highcharts";
import Highcharts from "highcharts";
var drilldown = require('highcharts/modules/drilldown');
var histogram = require('highcharts/modules/histogram-bellcurve');
var exporting = require('highcharts/modules/exporting');

const barChartData = {
  "Class 1": {
    avg: 0.8537,
    distribution: [[0.5098609587292944,2],[0.5727536605034427,1],[0.6356463622775909,14],[0.698539064051739,14],[0.7614317658258872,8],[0.8243244676000354,9],[0.8872171693741837,2]]
  },
  "Class 2": {
    avg: 0.86232,
    distribution: [[0.4589004874985227,2],[0.5326555459647132,0],[0.6064106044309038,7],[0.6801656628970943,16],[0.7539207213632849,11],[0.8276757798294755,11],[0.901430838295666,3]]
  },
  "Class 3": {
    avg: 0.8416,
    distribution: [[0.5343019189481634,4],[0.6167291050713104,9],[0.6991562911944574,16],[0.7815834773176044,15],[0.8640106634407515,5],[0.9464378495638984,0],[1.0288650356870455,1]]
  },
  "Class 4": {
    avg: 0.8021,
    distribution: [[0.4654022744477279,3],[0.5475397156456107,5],[0.6296771568434935,18],[0.7118145980413763,14],[0.793952039239259,5],[0.8760894804371419,3],[0.9582269216350245,2]]
  },
  "Class 5": {
    avg: 0.696170192,
    distribution: [[0.5061803871239141,4],[0.5691638585994836,5],[0.6321473300750531,9],[0.6951308015506227,12],[0.7581142730261922,12],[0.8210977445017617,4],[0.8840812159773311,3]]
  }
}

export default class BarHistoChart extends React.Component {

  componentWillMount() {
    histogram(Highcharts);
    exporting(Highcharts);
  }

  componentDidUpdate() {
    const routesContainerElem = document.getElementsByClassName('routes-container');
    if (routesContainerElem && routesContainerElem[0]) {
      routesContainerElem[0].scrollTop = this.state.routesContainerScrollPos;
    }
  }

  // constructor
  constructor(props) {
    super(props);

    // default ui local state
    this.state = {
      showHistogram: false,
      selectedClass: null,
      routesContainerScrollPos: 0

    };

    this.toggleSubMenu = this.toggleSubMenu.bind(this);
  }

  // render
  render() {
    const { selectedClass } = this.state;
    var callToggleSubMenu = this.toggleSubMenu;
    const barChartConfig = {
      chart: {
        type: 'column',
        margin: [60, 10, 40, 40]
      },
      credits: {
            enabled: false
      },
      title: {
        text: 'Q6 Avg Score Per Class'
      },
      subtitle: {
        text: 'Click the columns to view score distributions for each class'
      },
      xAxis: {
        categories: ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'],
        type: 'category'
      },
      yAxis: {
        title: {
          text: 'Total percent market share'
        }
      },
      exporting: {
       buttons: {
         contextButton: {
                    enabled: false
            }
         }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
          point: {
              events: {
                  click: function () {
                    const currentScrollPos = document.getElementsByClassName('routes-container')[0].scrollTop;
                    callToggleSubMenu(this.category, currentScrollPos);
                  }
              }
          },
          borderWidth: 0
        }
      },
      yAxis: {
        min: 0.5,
        max: 1,
          title: {
            text: ''
          }
      },
      series: [{
        name: 'Q6 Avg Score',
        colorByPoint: true,
        data: [{
          name: 'Class 1',
          y: barChartData["Class 1"]["avg"]
        }, {
          name: 'Class 2',
          y: barChartData["Class 2"]["avg"]
        }, {
          name: 'Class 3',
          y: barChartData["Class 3"]["avg"]
        }, {
          name: 'Class 4',
          y: barChartData["Class 4"]["avg"]
        }, {
          name: 'Class 5',
          y: barChartData["Class 5"]["avg"]
        }]
      }],
    };

    const histyData = [[0.5061803871239141,4],[0.5691638585994836,5],[0.6321473300750531,9],[0.6951308015506227,12],[0.7581142730261922,12],[0.8210977445017617,4],[0.8840812159773311,3]];

    const histyConfig = {
      title: {
          text: 'Q6 Histogram for ' + this.state.selectedClass
      },
      xAxis: [{
          title: { text: 'Data' },
          alignTicks: false
      }, {
          title: { text: 'Histogram' },
          alignTicks: false,
          opposite: true
      }],

      yAxis: [{
          title: { text: 'Data' }
      }, {
          title: { text: 'Histogram' },
          opposite: true
      }],
      navigation: {
        buttonOptions: {
            theme: {
                style: {
                    color: '#039',
                    textDecoration: 'underline'
                }
            }
        }
      },
      exporting: {
       buttons: {
         contextButton: {
                    enabled: false
            },
           'myButton': {

               _id: 'myButton',
               x: -62,
               onclick: function() {
                 const currentScrollPos = document.getElementsByClassName('routes-container')[0].scrollTop;
                 callToggleSubMenu(null, currentScrollPos);
               },
               _titleKey: "Back",
               text: "<- Back"

           }
       }
     },
      series: [{
          name: 'Histogram',
          type: 'bellcurve',
          data: selectedClass ? barChartData[selectedClass]["distribution"] : [],
          xAxis: 1,
          yAxis: 1,
          baseSeries: 's1',
          zIndex: -1
      }]
  }
    return (
      <div className="chart-container" id="bar-histo-chart" style={{marginTop: "10%"}}>
        { this.state.showHistogram ? <ReactHighcharts config={histyConfig}/> : <ReactHighcharts config={barChartConfig}/> }
      </div>
    );
  }

  toggleSubMenu(selectedClass, currentScrollPos) {
    this.setState({
      showHistogram: !this.state.showHistogram,
      selectedClass: selectedClass || null,
      routesContainerScrollPos: currentScrollPos
    });
  }

}
