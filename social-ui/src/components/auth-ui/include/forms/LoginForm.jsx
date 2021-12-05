import React, { useState, useEffect } from 'react';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'simple-line-icons';
import '../../style.css';
import '../../../../App.css';


const LoginForm = (props) => {
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()

    const [error, setError] = useState("")

    const authUserAndCreateJwt = (event) => {
        axios
            .post("http://127.0.0.1:8000/jwt/token/", {
                username: username,
                password: password,
            })
            .then(response => {
                localStorage.setItem("jwt", response.data.access)
                window.location.href = 'http://127.0.0.1:8000/categories/';
             })
            .catch(error => {
                if (error.response.status == 401) {
                    setError("Вы неправильно ввели логин или пароль. Попробуйте снова.")
                } else if (error.response.status == 400) {
                    setError("Логин или пароль не могут быть пустыми -_-.")
                } else {
                    setError(`${error.response.status} error`)
                }
            });
    }

    return (
        <div className="row">
            <div className="col-10 mx-auto">
                <div className="registration-form">
                    <div className="form-login">
                        <div className="form-icon">
                            <span><i className="icon icon-user"></i></span>
                        </div>
                        <div className="form-group">
                            <input
                                type="text"
                                className="form-control item"
                                id="username"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                placeholder="Username"/>
                        </div>
                        <div className="form-group">
                            <input
                                type="password"
                                className="form-control item"
                                id="password1"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="Password"/>
                        </div>
                        <a href="#" style={{float:"right", marginTop: "-10px", backgroundColor: "PowderBlue"}}>Don't have an account?</a>{"\n"}
                        <p className="text-danger" style={{float:"right",  backgroundColor: "PowderBlue"}}>{error}</p>
                        {"\n\n"}
                        <div className="form-group">
                            <button type="button" className="btn btn-block create-account" onClick={authUserAndCreateJwt}>Sign In</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}


export default LoginForm