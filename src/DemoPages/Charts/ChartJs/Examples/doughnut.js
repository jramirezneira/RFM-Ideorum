import React, { Component } from 'react';
import {Doughnut, Line} from 'react-chartjs-2';
import { Table } from 'reactstrap';
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
import 'react-bootstrap-table/dist/react-bootstrap-table.min.css';


import {
    Row, Col,
    Card, CardBody,
    CardTitle
} from 'reactstrap';


export default class DoughnutComponent extends Component
{

   //Create constructor with state variables
   constructor(props) {
      super(props);
      this.state = {
        DataDoughnut: {},
        DataLineRFM: {},
        DataLineRecency: {},
        DataLineFrequency: {},
        DataLineMonetary: {},
        DataTable: [],
        select2: 0,
        filtered: 0
      }
    }

//Load DataDoughnut
    getRFMDoughnut()
    {

         // axios.get('http://localhost:5000/dash/api/rfm')
        // axios.get('rfmSegment.json')

          let rfmSegment = require('./data/rfmSegment.json');

          let description = [];
          let sum = [];
          rfmSegment.forEach(element => {
            description.push(element.description);
            sum.push(element.counts);
          });
          this.setState({
            DataDoughnut: {
              labels: description,
              datasets:[
                 {
                    label:'RFM',
                    data: sum ,
                    backgroundColor:[
                     'rgba(255,105,145,0.6)',
                     'rgba(155,100,210,0.6)',
                     'rgba(90,178,255,0.6)',
                     'rgba(240,134,67,0.6)',
                     'rgba(250,55,197,0.6)',
                     'rgba(255, 64, 61)',
                     'rgba(44, 159, 175)',
                     'rgba(246, 194, 62)',
                     'rgba(46, 89, 217)',
                     'rgba(23, 166, 115)',
                     'rgba(120,120,120,0.6)'
                  ]
                 }
              ]
           }

           });

    }
//Load Table
    getRFMCustomers = (value) => {
        //axios.get('http://localhost:5000/dash/api/rfmcustomers?sort='+value  )
          //    .then(res => {
              let rfmcustomers = require('./data/rfmcustomers.json');
              let rfms= {};
              if(value >0)
                rfms=  rfmcustomers.filter(l => l.sort== value);
              else
                rfms=rfmcustomers;

              this.setState({
                DataTable:rfms
               });
           //  });
    };

//Load table with details
    getRFMCustomersByMonth = (value) => {


       // axios.get('http://localhost:5000/dash/api/rfmcustomersTimeSeries?customerid='+value  )
           //   .then(res => {
            let rfmcustomersTimeSeries = require('./data/rfmcustomersTimeSeries.json');
            let rfms ={}
            console.log(value);
           // rfms=  Object.values(rfmcustomersTimeSeries).map;
            //alert(rfmcustomersTimeSeries[12347]);

            Object.values(rfmcustomersTimeSeries).map(val => {
                if (val.customerid == value  )
                 rfms= val;
              })
            console.log(rfms);
            this.setState({
                DataLineRFM: rfms.result[0],
                DataLineRecency: rfms.result[1],
                DataLineFrequency: rfms.result[2],
                DataLineMonetary: rfms.result[3],



            });



         //    });
    };




    componentDidMount() {
        this.getRFMDoughnut();
        this.getRFMCustomers(0);
      // this.getRFMCustomersByMonth(1);
    }

    trStyle = (row, rowIndex) => {


        return { backgroundColor: 'red' };
  }



imgFormatter(cell,row) {
    return  <button className='btn btn-info' onClick={() =>
      this.getRFMCustomersByMonth(row.customerid)}>Action


            </button>;
}


   render()
   {

      function rowStyleFormat(row, rowIdx) {
            if (rowIdx >=0)
                if(row.variation >=0)
                        return { backgroundColor: 'rgb(216, 250, 214, 0.3)' };
                    else
                        return { backgroundColor: '#FFDDDD' };
            return { backgroundColor:  'blue' };
        }

      const { DataTable } = this.state
      return(

      <Row>
        <Col lg="7">

            <Card className="main-card mb-3">
                <CardBody>
                    <CardTitle>RFM</CardTitle>
                        <div>

                            <Doughnut
                              data={this.state.DataDoughnut}
                              getElementAtEvent={(elems, event) => {
                                      this.getRFMCustomers(
                                      elems.map(o => {
                                        return o._index+1;
                                      })
                                    );


                             }}
                              />

                             <BootstrapTable data={this.state.DataTable} trStyle={ rowStyleFormat } pagination  exportCSV  >


                                <TableHeaderColumn dataField='customerid' isKey={true}   dataSort={ true } >Customer</TableHeaderColumn>
                                  <TableHeaderColumn dataField='description'  dataSort={ true } thStyle={ { whiteSpace: 'normal' } }  tdStyle={ { whiteSpace: 'normal' } }  >RFM</TableHeaderColumn>
                                  <TableHeaderColumn dataField='variation'  dataSort={ true } thStyle={ { whiteSpace: 'normal' } } >Variation</TableHeaderColumn>

                                    <TableHeaderColumn dataField='recency_total'  dataSort={ true } thStyle={ { whiteSpace: 'normal' } } >Recency</TableHeaderColumn>
                                  <TableHeaderColumn dataField='frequency_total'  dataSort={ true } thStyle={ { whiteSpace: 'normal' } } >Frequency</TableHeaderColumn>
                                  <TableHeaderColumn dataField='monetary_total'   dataSort={ true } thStyle={ { whiteSpace: 'normal' } } >Monetary</TableHeaderColumn>
                                 <TableHeaderColumn dataField='action' dataFormat={ this.imgFormatter.bind(this) } export={ false }>Action</TableHeaderColumn>

                              </BootstrapTable>
                         </div>
                    </CardBody>
            </Card>
        </Col>
        <Col lg="5">

            <Card className="main-card mb-3">
                <CardBody>
                    <CardTitle>RFM</CardTitle>
                    <div>
                          <Line data={this.state.DataLineRFM} />
                        </div>
                </CardBody>
            </Card>
            <Card className="main-card mb-3">
                <CardBody>
                    <CardTitle>Recency</CardTitle>
                    <div>
                          <Line data={this.state.DataLineRecency} />
                        </div>
                </CardBody>
            </Card>
            <Card className="main-card mb-3">
                <CardBody>
                    <CardTitle>Frequency</CardTitle>
                    <div>
                          <Line data={this.state.DataLineFrequency} />
                        </div>
                </CardBody>
            </Card>
             <Card className="main-card mb-3">
                <CardBody>
                    <CardTitle>Monetary</CardTitle>
                    <div>
                          <Line data={this.state.DataLineMonetary} />
                        </div>
                </CardBody>
            </Card>
        </Col>
      </Row>
      )
   }
}



