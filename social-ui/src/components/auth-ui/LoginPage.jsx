import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import './style.css';
import '../../App.css';

import Header from '../extend/Header';
import Error404NotFound from '../extend/Error404NotFound';
import LoginForm from "./include/LoginForm";


const LoginPage = (props) => {
    if (props.isAuth) {
        return (
            <div>
                <Header/>
                {"\n"}
                <Error404NotFound/>
            </div>
        )
    } else {
        return (
            <div>
                <Header/>
                {"\n"}
                <LoginForm/>
            </div>
        )
    }
}

export default LoginPage;
