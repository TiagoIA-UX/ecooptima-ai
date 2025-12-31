import React from 'react';
import { Line } from 'react-chartjs-2';

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Dashboard Energético' },
  },
};

function Dashboard({ chartData }) {
  return (
    <div>
      <h2>Dashboard</h2>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default Dashboard;
