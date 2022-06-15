import React, { useState, useRef, useEffect } from "react"; import {
  useNavigate,
  useLocation
} from "react-router-dom";
import Button from '@mui/material/Button';
import '../App.css';

function useOutsideAlerter(ref, func) {
  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        func();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, func]);
}

function Header({ title, onClick, isLogined = true }) {
  const navigate = useNavigate();
  const wrapperRef = useRef(null);
  const [openMenu, setopenMenu] = useState(false);
  useOutsideAlerter(wrapperRef, () => { setopenMenu(false) });

  return (
    <div className="header">
      <img className="icon" src={require('../img/icon.png')} onClick={() => {
        isLogined ? navigate("/main") : navigate("/")
      }}/>
      <p className="headerTitle">Проверка репозитория на образовательные результаты</p>
      {isLogined
        ? <p onClick={() => setopenMenu(true)} className="headerButtom">{title}</p>
        : <Button variant="text" onClick={onClick}>{title}</Button>
      }
      {openMenu && (
        <div className="select_menu" ref={wrapperRef}>
          <div className="select_item" onClick={() => navigate("/solution-all")}>Прошлые результаты</div>
          <div className="select_item" onClick={() => {
            sessionStorage.setItem('auth_token', "");
            navigate("/")
          }}>Выйти</div>
        </div>
      )}
    </div>
  );
}

export default Header;
