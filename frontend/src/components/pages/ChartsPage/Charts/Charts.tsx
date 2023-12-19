import React from "react";
import { Line } from "react-chartjs-2";
import "./../../../../styles/MainDataFillingForm.model.scss";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
  } from 'chart.js';
import { Link } from "react-router-dom";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Filler,
    Tooltip,
    Legend
);

type Props = {
    data: any[];
}

const Charts = (props: Props) => {
    let dates = []
    let true_cost = []
    let pred_cost = []
    let error = []
    let flag = false
    props.data.map((row) => {
        if (flag){
            dates.push(row[0])
            true_cost.push(row[2])
            pred_cost.push(row[10])
            error.push(row[11])
        }
        else{
            if (row[7] >= 5){
                flag = true
            }
        }
    })
    const firstLineChartData = {
      labels: dates,
      datasets: [
        {
          data: true_cost,
          label: "Истинное значение",
          borderColor: "#3333ff",
          fill: false,
          lineTension: 0.5
        },
        {
          data: pred_cost,
          label: "Предсказанное значение",
          borderColor: "#ff3333",
          backgroundColor: "rgba(255, 0, 0, 0.5)",
          fill: false,
          lineTension: 0.5
        }
      ]
    };
    const secondLineChartData = {
        labels: dates,
        datasets: [
            {
                data: error,
                label: "Ошибка, в %",
                borderColor: "#ff3333",
                backgroundColor: "rgba(255, 0, 0, 0.5)",
                fill: false,
                lineTension: 0.5
            }
        ]
    };
    return (
    <div className="LineCharts" >
        <Link to="/" className="form-button-download" style={{float: "left"}}>Обратно</Link>
        <Line
        width={80}
        height={30}
        options={{
            plugins:{
                title: {
                    display: true,
                    text: "Прогноз значений",
                },
                legend: {
                    display: true, //Is the legend shown?
                    position: "top" //Position of the legend.
                }
            }
        }}
        data={firstLineChartData}
        />
        <Line
            width={80}
            height={30}
            options={{
                plugins:{
                    title: {
                        display: true,
                        text: "Ошибка",
                    },
                    legend: {
                        display: true, //Is the legend shown?
                        position: "top" //Position of the legend.
                    }
                }
            }}
            data={secondLineChartData}
        />
    </div>
    );
  };
  export default Charts;