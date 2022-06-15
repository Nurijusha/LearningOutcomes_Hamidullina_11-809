import React, { useEffect, useState } from "react";
import {
  useNavigate
} from "react-router-dom";
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import KeyboardBackspaceIcon from '@mui/icons-material/KeyboardBackspace';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';
import Header from "../Header/Header";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import '../App.css';

function Main() {

  const navigate = useNavigate();
  const [topics, setTopics] = useState([])
  const [task, setTask] = useState()
  const [email, setEmail] = useState("")
  const [loader, setLoader] = useState(false);
  const [error, setError] = useState(false)

  const getTopics = () => {
    fetch("/api/topics/", {
      method: "GET",
      headers: new Headers({
        'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
      }),
    })
      .then((response) => {
        response.json().then(value => {
          setTopics(value)
        })
      })
  }

  const getTask = (id) => {
    fetch(`/api/tasks/${id}/`, {
      method: "GET",
      headers: new Headers({
        'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
      }),
    })
      .then((response) => {
        response.json().then(value => {
          setTask(value)
        })
      })
  }

  const checkUrl = () => {
    setLoader(true);
    setError(false);
    fetch(`/api/solution-testing/`, {
      method: "POST",
      headers: new Headers({
        'Content-Type': 'application/json',
        'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
      }),
      body: JSON.stringify({
        github_url: email
      })
    })
      .then((response) => {
        response.json().then((value) => {
          if (value.error) {
            setLoader(false);
            setError(value.error);
          } else {
            checkUrl2(value.id)
          }
        })
      })
  }

  const checkUrl2 = (id) => {
    let timerId = setInterval(() => {
      fetch(`/api/solution-testing/${id}/`, {
        method: "GET",
        headers: new Headers({
          'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
        })
      })
        .then((response) => {
          response.json().then(value => {
            if (value.status === "SUCCESS") {
              clearInterval(timerId);
              getSolutions(value.id)
            }
          })
        })
    }, 5000);
  }

  const getSolutions = (id) => {
    fetch(`/api/solutions/${id}/`, {
      method: "GET",
      headers: new Headers({
        'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
      })
    })
      .then((response) => {
        response.json().then(value => {
          setLoader(false);
          navigate("/solution", {
            state: value
          })
        })
      })
  }

  useEffect(getTopics, [])

  return (
    <React.Fragment>
      <Header title={sessionStorage.getItem('username')} />
      {loader && <div className="loaderScreen">
        <Stack sx={{ color: 'grey.500' }} spacing={2} direction="row">
          <CircularProgress />
        </Stack></div>}
      {
        task
          ? (
            <div className="main topics">
              <div className="title">
                <div style={{
                  display: "flex"
                }}>
                  <IconButton color="primary" onClick={() => setTask()}>
                    <KeyboardBackspaceIcon />
                  </IconButton>
                  <h2 style={{
                    width: "400px",
                    textAlign: "center"
                  }}>{task.name}</h2>
                </div>
              </div>
              <span style={{
                color: "#547FA6",
                whiteSpace: "pre-wrap"
              }}
                dangerouslySetInnerHTML={{ __html: task.description }}/>
            </div>
          )
          : (
            <div className="main topics">
              <h3>Список тем</h3>
              {topics.map(topic => (
                <Accordion>
                  <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                  >
                    <Typography style={{
                      color: "#547FA6"
                    }}>{topic.name}</Typography>
                  </AccordionSummary>
                  {topic.tasks.map(task => (
                    <AccordionDetails>
                      <Typography style={{
                        color: "#547FA6",
                        cursor: "pointer"
                      }} onClick={() => {
                        getTask(task.id)
                      }}>
                        {task.name}
                      </Typography>
                    </AccordionDetails>
                  ))}
                </Accordion>
              ))}
            </div>
          )
      }
      <div className="main checkUrl">
        <h3>Проверить репозиторий</h3>
        <TextField
          error={error}
          id="outlined-required"
          label="Введите url репозитоия"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          helperText={error}
          margin="normal"
        />
        <Button variant="outlined" onClick={checkUrl}>Проверить</Button>
        <p style={{fontSize: "14px", opacity: 0.8 }}>Для проверки репозитория на уровень образовательных результатов необходимо склонировать шаблон репозитория <a target="_blank" rel="noopener noreferrer" href={"https://github.com/Nurijusha/solution_template"}>ссылка</a> и разместить в данном репозитории свои решения</p>
      </div>
    </React.Fragment>
  );
}

export default Main;
