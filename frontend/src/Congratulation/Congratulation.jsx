import React from "react";
import Button from '@mui/material/Button';
import {
  useNavigate
} from "react-router-dom";
import Header from "../Header/Header";
import '../App.css';

function Congratulation() {
  const navigate = useNavigate();

  return (
    <div className="contentCenter">
      <Header title="Регистрация" onClick={() => navigate("/")} isLogined={false} />
      <div className="authBlock sendEmail">
        <h2>Завершение регистрации</h2>
        <div style={{
          paddingTop: "10px"
        }}>
        Поздравляем! Вы зарегистрировались!
        </div>
        <div style={{
          paddingTop: "50px"
        }}>
        <Button variant="outlined" onClick={() => navigate("/")} >Войти</Button>
        </div>
      </div>
    </div>
  );
}

export default Congratulation;
