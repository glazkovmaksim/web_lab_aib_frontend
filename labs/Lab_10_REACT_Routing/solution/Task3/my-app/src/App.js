import './App.css';
import './App 2.0.css';
import React from 'react';
import User from './task3/User';
import UsersList from './task3/Users';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Router>
      <div>
	<a href='/'>Главная</a> 
        <Routes>
          <Route path="/" element={<UsersList />} />
          <Route path="/user/:id" element={<User />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;