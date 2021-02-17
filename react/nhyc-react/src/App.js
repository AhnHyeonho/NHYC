import React, {useState} from 'react';
import './App.css';

import {BrowserRouter as Router, Route} from 'react-router-dom';
import {About, MapInfo, Recommand , Login} from './Page';



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
      <div className="App"> 
        <div className ="App-Body">
          <Route exact path ='/' component ={About}/>
          <Route exact path ='/about' component ={About}/>
          <Route path ='/map' component={MapInfo}/>
          <Route path ='/recommand' component={Recommand}/>
          

          
          <AuthRoute
            authenticated={authenticated}
            path="/recommand"
            render={props => <Recommand user={user} {...props} />}
          />
       
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
        
      </div>
    </Router>
  );
}

export default App;
