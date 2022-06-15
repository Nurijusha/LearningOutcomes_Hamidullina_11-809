import React, { useState } from "react";
import {
  useNavigate
} from "react-router-dom";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Header from "../Header/Header";
import '../App.css';

function Registration() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [username, setUsername] = useState("")
  const [error, setError] = useState({})
  const navigate = useNavigate();

  async function login() {
    fetch("/api/users/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email, password, username
      })
    })
      .then((response) => {
        if (response.ok) {
          navigate(`/send_email?email=${email}`)
        }
        response.json().then(value => {
          setError(value);
        })
      })
  }

  return (
    <div className="contentCenter">
      <Header title="Авторизация" onClick={() => navigate("/")} isLogined={false} />
      <div className="authBlock">
        <h2>Регистрация</h2>
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
          error={error.hasOwnProperty("email")}
          id="outlined-required"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          helperText={error?.["email"] || ""}
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
          <Button variant="outlined" onClick={login}>Зарегистрироваться</Button>
        </div>
      </div>
    </div>
  );
}

export default Registration;
