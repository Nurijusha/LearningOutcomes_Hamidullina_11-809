import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Auth from "./Auth/Auth";
import Registration from "./Registration/Registration";
import Congratulation from "./Congratulation/Congratulation";
import SendEmail from "./SendEmail/SendEmail";
import Main from "./Main/Main";
import Solution from "./Solution/Solution";
import SolutionAll from "./SolutionAll/SolutionAll";
import Activate from "./Activate/Activate";

import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<Auth />} />
        </Routes>
        <Routes>
          <Route exact path="/reg" element={<Registration />} />
        </Routes>
        <Routes>
          <Route exact path="/congratulation" element={<Congratulation />} />
        </Routes>
        <Routes>
          <Route exact path="/send_email" element={<SendEmail />} />
        </Routes>
        <Routes>
          <Route exact path="/main" element={<Main />} />
        </Routes>
        <Routes>
          <Route exact path="/solution" element={<Solution />} />
        </Routes>
        <Routes>
          <Route exact path="/solution-all" element={<SolutionAll />} />
        </Routes>
        <Routes>
          <Route exact path="/activate-account/:uid/:token" element={<Activate />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
