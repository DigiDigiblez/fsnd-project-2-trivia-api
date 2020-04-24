import './stylesheets/App.css';

import React from 'react';
import {BrowserRouter as Router} from 'react-router-dom'
// import logo from './logo.svg';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import Switch from "react-router-dom/es/Switch";
import Route from "react-router-dom/es/Route";


const App = () => (
    <div className="App">
        <Header path/>
        <Router>
            <Switch>
                <Route path="/" exact component={QuestionView}/>
                <Route path="/add" component={FormView}/>
                <Route path="/play" component={QuizView}/>
                <Route component={QuestionView}/>
            </Switch>
        </Router>
    </div>
)

export default App;
