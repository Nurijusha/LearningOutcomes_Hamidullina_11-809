import React from "react";
import Button from '@mui/material/Button';
import Header from "../Header/Header";
import {
  useNavigate,
  useLocation,
} from "react-router-dom";
import '../App.css';

function SendEmail() {
  const navigate = useNavigate();
  const search = useLocation().search;
  const email = new URLSearchParams(search).get("email");

  return (
    <div className="contentCenter">
      <Header title="Авторизация" onClick={() => navigate("/")} isLogined={false} />
      <div className="authBlock sendEmail">
        <h2>Подтверждение email</h2>
        <div>На ваш email: <span style={{
          fontWeight: 700
        }}>{email}</span> был отправлена ссылка для подтверждения, пройдите по ней для регистрации!</div>
        <div className="buttonBack" >
          <Button variant="text" onClick={() => navigate("/")} >Назад</Button>
        </div>
      </div>
    </div>
  );
}

export default SendEmail;
