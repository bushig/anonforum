import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import {DataProvider} from './DataProvider'
//import logo from './logo.svg';
//import '../App.css';


const App = ()=>(
    <React.Fragment>
      <DataProvider endpoint="api" render={data => {return Object.keys(data).map(key=><p>{data[key].name}</p>)}} />
    </React.Fragment>
);

const wrapper = document.getElementById("app");

ReactDOM.render(<App />, wrapper);
