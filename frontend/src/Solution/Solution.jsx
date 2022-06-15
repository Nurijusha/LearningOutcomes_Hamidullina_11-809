import React, { useEffect, useMemo, useState } from "react";
import Button from '@mui/material/Button';
import {
  useNavigate,
  useLocation
} from "react-router-dom";
import '../App.css';
import Header from "../Header/Header";

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function Solution() {
  const navigate = useNavigate();
  const location = useLocation();
  const [score, setScore] = useState({
    5: 0,
    4: 0,
    3: 0,
    2: 0
  });

  useEffect(() => {
    const newscore = {
      5: 0,
      4: 0,
      3: 0,
      2: 0
    }
    location.state.learning_outcomes.map((value) => newscore[value.score] = newscore[value.score] + 1);
    setScore(newscore)
  }, [location])

  const data = useMemo(() => {
    return {
      labels: ['на 2', 'на 3', 'на 4', 'на 5'],
      datasets: [
        {
          label: '# of Votes',
          data: Object.values(score),
          backgroundColor: [
            'rgba(255, 99, 132)',
            'rgba(54, 162, 235)',
            'rgba(255, 206, 86)',
            'rgba(75, 192, 192)',
          ],
          borderWidth: 1,
        },
      ],
    };
  }, [score])

  return (
    <>
      <Header title={sessionStorage.getItem('username')} />
      <div className="contentCenter">
        <div className="solution">
          <h1>Образовательные результаты</h1>
          <div className="tooltip">
            <div className="block">
              <div className="pie">
                <Pie
                  height="200px"
                  width="200px"
                  options={{ maintainAspectRatio: false }}
                  data={data}
                />
              </div>
            </div>
            <div className="block">
              <h2>Средняя оценка</h2>
              <div className="score">{((5 * score[5] + 4 * score[4] + 3 * score[3] + 2 * score[2]) / Object.values(score).reduce((ac, sc) => ac + sc)).toFixed(2)}</div>
            </div>
            <div className="block2">
              <h2 style={{
                textAlign: "center"
              }}>Общие данные</h2>
              <div>URL репозитория <a target="_blank" rel="noopener noreferrer" href={location.state.github_url}>{location.state.github_url}</a></div>
              <div>Дата время проверки: {new Date(location.state.created_at).toLocaleString()}</div>
              <Button variant="outlined" onClick={() => navigate("/solution-all")} >Посмотреть прошлые результаты</Button>
            </div>
          </div>
          <div className="tableSolution">
            <TableContainer component={Paper}>
              <Table style={{ tableLayout: 'fixed' }} sx={{ minWidth: 650 }} aria-label="simple table" stickyHeader={true}>
                <TableHead>
                  <TableRow>
                    <TableCell>Образовательный результат</TableCell>
                    <TableCell align="left">Уровень</TableCell>
                    <TableCell align="left">Необходимо повторить или изучить</TableCell>
                    <TableCell align="left">Номера задач для практики</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {
                    location.state.learning_outcomes.map((row) => (
                      <TableRow
                        key={row.name}
                      >
                        <TableCell component="th" scope="row">
                          {row.name}
                        </TableCell>
                        <TableCell align="left">{row.score}</TableCell>
                        <TableCell align="left">
                          {row.recommendations.map((recommendation) => <div>{recommendation.name}</div>)}
                        </TableCell>
                        <TableCell align="left">
                          {
                            row.recommendations.map((recommendation) => <div>{recommendation.task}</div>)
                          }
                        </TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        </div>
      </div>
    </>
  );
}

export default Solution;
