import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './Page/Header';
import Footer from './Page/Footer';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { About, MapInfo, Recommand, Login } from './Page';

import Profile from './Page/Body/AuthTest/Profile';
import { signIn } from './Page/Body/Login/auth';
import AuthRoute from './Page/Body/Login/AuthRoute';
import SignUp from './Page/Body/Login/SignUp'




function App() {

  const [user, setUser] = useState(null);
  const authenticated = user != null;

  const login = ({ email, password }) => setUser(signIn({ email, password }));
  const logout = () => setUser(null);

  return (
    <Router>

      {/* header */}
      <div className="App-Header">
        <Header />
      </div>

      {/* body */}
      <div className="App-Body">
        <Route exact path='/' component={About} />
        <Route exact path='/about' component={About} />
        <Route path='/map' component={MapInfo} />
        <Route path='/recommand' component={Recommand} />
        {/* <Route path='/login' component={Login} /> */}

        {/* <Route path="/profile" component={Profile} /> */}

        {/* <AuthRoute
          authenticated={authenticated}
          path="/recommand"
          render={props => <Recommand user={user} {...props} />}
        /> */}

        <Route
          path="/login"
          render={props => (
            <Login authenticated={authenticated} login={login} {...props} />
          )}
        />

        <Route
          path="/signup"
          render={props => (
            <SignUp authenticated={authenticated} login={login} {...props} />
          )}
        />

        


      </div>

      {/* footer */}
    </Router>
  );
}

export default App;
