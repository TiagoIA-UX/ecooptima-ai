import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import RegisterEnergy from './components/RegisterEnergy';
import EnergyList from './components/EnergyList';
import CarbonMarketplace from './components/CarbonMarketplace';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [records, setRecords] = useState([]);

  // Login real com JWT
  const handleLogin = async (username, password) => {
    const form = new URLSearchParams();
    form.append('username', username);
    form.append('password', password);
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString()
    });
    if (res.ok) {
      const data = await res.json();
      setUser({ id: data.user_id, username });
      setToken(data.access_token);
    } else {
      alert('Usuário ou senha inválidos');
    }
  };

  // Busca automática do histórico ao logar
  useEffect(() => {
    const fetchRecords = async () => {
      if (!token) return;
      const res = await fetch('http://localhost:8000/energy', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setRecords(data);
      }
    };
    fetchRecords();
  }, [token]);

  // Registrar consumo usando token
  const handleRegisterEnergy = async (value) => {
    if (!token) return;
    const res = await fetch('http://localhost:8000/energy', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ value })
    });
    if (res.ok) {
      const data = await res.json();
      setRecords(prev => [...prev, data]);
    } else {
      alert('Erro ao registrar consumo');
    }
  };

  // Logout
  const handleLogout = () => {
    setUser(null);
    setToken(null);
    setRecords([]);
  };

  // Dados para o gráfico
  const chartData = {
    labels: records.map(r => new Date(r.timestamp).toLocaleDateString()),
    datasets: [
      {
        label: 'Consumo Energético (kWh)',
        data: records.map(r => r.value),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div>
      <h1>EcoOptima AI</h1>
      {!user ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          <button onClick={handleLogout}>Sair</button>
          <Dashboard chartData={chartData} />
          <RegisterEnergy onRegister={handleRegisterEnergy} />
          <EnergyList records={records} />
          <CarbonMarketplace token={token} />
        </>
      )}
    </div>
  );
}

export default App;
