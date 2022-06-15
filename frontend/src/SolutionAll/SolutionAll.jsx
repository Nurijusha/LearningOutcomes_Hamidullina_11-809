import React, { useEffect, useMemo, useState } from "react";
import '../App.css';
import Header from "../Header/Header";

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

import { getScore } from "../helpers";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const init_score = {
  5: 0,
  4: 0,
  3: 0,
  2: 0
}

function SolutionAll() {
  const [solutions, setSolutions] = useState([]);
  const [score, setScore] = useState(0);
  const [oldScore, oldSetScore] = useState(0);
  useEffect(() => {
    fetch(`/api/solutions/`, {
      method: "GET",
      headers: new Headers({
        'Authorization': `Token ${sessionStorage.getItem('auth_token')}`,
      }),
    })
      .then((response) => {
        response.json().then(value => {
          value = value.map((solution) => ({ ...solution, learning_outcomes: solution.learning_outcomes.sort((a, b) => a.name > b.name ? 1 : -1) }))
          setSolutions(value)
          let newscore = Object.assign({}, init_score);
          value[0].learning_outcomes.map((value) => newscore[value.score] = newscore[value.score] + 1);
          newscore = getScore(newscore).toFixed(2)
          setScore(newscore)
          let oldscore = Object.assign({}, init_score);
          if (value[1]) {
              value[1] && value[1].learning_outcomes.map((value) => oldscore[value.score] = oldscore[value.score] + 1);
              oldscore = getScore(oldscore).toFixed(2)
              oldscore = (newscore - oldscore).toFixed(2)
              oldSetScore(oldscore);
          }
        })
      })
  }, [])

  const labels = solutions.map(solution => new Date(solution.created_at).toLocaleDateString());

  const options = {
    scales: {
      yAxis: {
        min: 0,
        max: 5,
      }
    }
  };

  const data = useMemo(() => {
    return {
      labels: labels,
      datasets: [
        {
          label: 'Dataset 1',
          data: solutions.map((solution) => {
            const newscore = {
              5: 0,
              4: 0,
              3: 0,
              2: 0
            }
            solution.learning_outcomes.map((value) => newscore[value.score] = newscore[value.score] + 1);
            return (getScore(newscore))
          }),
          borderColor: 'green',
          backgroundColor: 'green',
        },
      ],
    };
  }, [solutions])

  const data2 = useMemo(() => {
    return {
      labels: solutions[0]?.learning_outcomes.map((_, i) => String(i + 1)),
      datasets: [
        {
          label: 'текущая оценка',
          data: solutions[0]?.learning_outcomes.map(solution => solution.score),
          backgroundColor: 'rgba(255, 99, 132)',
        },
        {
          label: 'прошлая оценка',
          data: solutions[1]?.learning_outcomes.map(solution => solution.score),
          backgroundColor: 'rgba(53, 162, 235)',
        }
      ],
    };
  }, [solutions])

  return (
    <div className="contentCenter" >
      <Header title={sessionStorage.getItem('username')} />
      <div className="solution">
        <h1>Образовательные результаты</h1>
        <div className="tooltip">
          <div className="block3">
            <Line
              options={{
                ...options,
                plugins: {
                  legend: {
                    display: false,
                  }
                }
              }}
              data={data}
            />
          </div>
          <div className="block3">
            <Bar
              options={options}
              data={data2}
            />
          </div>
          <div className="block3">
            <h2 style={{
              position: "absolute",
              top: "0px"
            }}>Средняя оценка</h2>
            <div className="score2">{score}
              <div className="score3" style={{ color: oldScore >= 0 ? "green" : "red" }}>{typeof oldScore === "string" ? (oldScore >= 0 ? `+${oldScore}` : oldScore) : ""}</div>
            </div>
            <div className="url"><span style={{
              fontWeight: "600"
            }}>URL</span> <a target="_blank" rel="noopener noreferrer" href={solutions[0]?.github_url}>{solutions[0]?.github_url}</a></div>
          </div>
        </div>
        <div className="tableSolution">
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Образовательный результат</TableCell>
                  {
                    solutions.map((_) => (
                      <>
                        <TableCell align="left">Дата/время</TableCell>
                        <TableCell align="left">Уровень</TableCell>
                      </>
                    ))
                  }
                </TableRow>
              </TableHead>
              <TableBody>
                {
                  solutions[0]?.learning_outcomes.map((learning_outcome, i) => (
                    <TableRow
                      key={learning_outcome.name}
                    >
                      <>
                        <TableCell align="left">{i + 1}</TableCell>
                        <TableCell align="left">{learning_outcome.name}</TableCell>
                        {
                          solutions.map(solution => (
                            <>
                              <TableCell align="left">{new Date(solution?.created_at).toLocaleString()}</TableCell>
                              <TableCell align="left">{solution.learning_outcomes[i]?.score}</TableCell>
                            </>
                          ))
                        }
                      </>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      </div>
    </div >
  );
}

export default SolutionAll;
