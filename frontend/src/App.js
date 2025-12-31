import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const values = input.split(',').map(Number);
    const res = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ values })
    });
    const data = await res.json();
    setResult(data.prediction);
  };

  return (
    <div>
      <h1>EcoOptima AI Frontend</h1>
      <p>Dashboard inicial do projeto.</p>
      <div>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Digite valores, ex: 6,7,8"
        />
        <button onClick={handlePredict}>Prever Consumo</button>
      </div>
      {result && (
        <div>
          <h2>Previsão:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
