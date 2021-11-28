import React, { useState, useEffect } from 'react';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'simple-line-icons';
import '../style.css';
import '../../../App.css';


const SignUpForm = () => {
    return (
        <div className="row">
            <div className="col-10 mx-auto">
                <div className="registration-form">
                    <div className="form">
                        <div className="form-icon">
                            <span><i className="icon icon-user"></i></span>
                        </div>
                        <div className="form-group">
                            <input type="text" className="form-control item" id="username" placeholder="Username"/>
                        </div>
                        <div className="form-group">
                            <input type="password" className="form-control item" id="password1" placeholder="Password"/>
                        </div>
                        <div className="form-group">
                            <input type="password" className="form-control item" id="password2" placeholder="Repeat Password"/>
                        </div>
                        <div className="form-group">
                            <input type="text" className="form-control item" id="email" placeholder="Email"/>
                        </div>
                        <a href="#" style={{float: "right", marginTop: "-10px"}}>Already have an account?</a>
                        {"\n"}
                        <div className="form-group">
                            <button type="button" className="btn btn-block create-account">Create Account</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUpForm;