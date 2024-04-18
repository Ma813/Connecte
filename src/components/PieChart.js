import React from "react";
import { Pie } from 'react-chartjs-2';
import {Chart} from 'chart.js/auto';

function PieChart({chartData}) {
  return (
    <div style={{
      width: '400px',
      height: '400px',
      margin: 'auto',
    }}>
      <Pie 
        data={chartData} 
        options={{
          backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(178, 255, 102, 0.6)', 'rgba(153, 102, 255, 0.6)'],
          borderWidth: 1,
          hoverBackgroundColor: ['rgba(75, 192, 192, 1)', 'rgba(178, 255, 102, 1)', 'rgba(153, 102, 255, 1)'],
          animation: {
            duration: 2500,
            easing: "easeInOutQuart",
          },
          plugins: {
            legend : {
              display: true,
              position: 'bottom',
              labels: {
                color: 'white',
              }

          }
        }
        }}
      />
    </div>
  );
}

export default PieChart;