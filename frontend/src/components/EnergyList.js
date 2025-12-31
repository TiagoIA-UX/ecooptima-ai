import React from 'react';

function EnergyList({ records }) {
  return (
    <div>
      <h2>Histórico de Consumo</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Valor (kWh)</th>
            <th>Data/Hora</th>
          </tr>
        </thead>
        <tbody>
          {records.map(record => (
            <tr key={record.id}>
              <td>{record.id}</td>
              <td>{record.value}</td>
              <td>{new Date(record.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EnergyList;
