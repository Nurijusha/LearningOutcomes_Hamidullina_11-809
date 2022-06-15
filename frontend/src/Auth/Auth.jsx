import React, { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Header from "../Header/Header";
import {
  useNavigate
} from "react-router-dom";
import '../App.css';

function Auth() {

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState({})
  const navigate = useNavigate();

  async function login() {
    fetch("/api/auth/token/login/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        password, username
      })
    })
      .then((response) => {
        if (response.ok) {
          response.json().then(({ auth_token }) => {
            sessionStorage.setItem('auth_token', auth_token);
            sessionStorage.setItem('username', username);
            navigate("/main")
          })
        }
        response.json().then(value => {
          setError(value);
        })
      });
  }

  return (
    <div className="contentCenter">
      <Header title="Регистрация" onClick={() => navigate("/reg")} isLogined={false} />
      {error["non_field_errors"] && (
        <Alert severity="error">
          <AlertTitle>Что то пошло не так!</AlertTitle>
          {error["non_field_errors"]}
        </Alert>
      )}
      <div className="authBlock">
        <h2>Авторизация</h2>
        <TextField
          error={error.hasOwnProperty("username")}
          id="outlined-required"
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          fullWidth
          helperText={error?.["username"] || ""}
          margin="normal"
        />
        <TextField
          error={error.hasOwnProperty("password")}
          id="filled-password-input"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          autoComplete="current-password"
          fullWidth
          helperText={error?.["password"] || ""}
          margin="normal"
        />
        <div className="authBlockButton">
          <Button variant="outlined" onClick={login}>Войти</Button>
        </div>
      </div>
    </div>
  );
}

export default Auth;
