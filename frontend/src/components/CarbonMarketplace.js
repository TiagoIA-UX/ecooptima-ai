import React, { useState, useEffect } from 'react';

function CarbonMarketplace({ token }) {
  const [credits, setCredits] = useState([]);
  const [amount, setAmount] = useState('');
  const [price, setPrice] = useState('');
  const [currency, setCurrency] = useState('BRL');
  const [converted, setConverted] = useState(null);
  const [transactions, setTransactions] = useState([]);

  // Buscar créditos disponíveis
  useEffect(() => {
    if (!token) return;
    fetch('http://localhost:8000/carbon/credits', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setCredits);
  }, [token]);

  // Buscar transações do usuário
  useEffect(() => {
    if (!token) return;
    fetch('http://localhost:8000/carbon/transactions', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setTransactions);
  }, [token]);

  // Colocar crédito à venda
  const handleSell = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:8000/carbon/credits', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ amount: parseFloat(amount), price: parseFloat(price), currency })
    });
    if (res.ok) {
      alert('Crédito colocado à venda!');
      setAmount('');
      setPrice('');
      setCurrency('BRL');
    } else {
      alert('Erro ao vender crédito');
    }
  };

  // Comprar crédito
  const handleBuy = async (credit_id) => {
    const res = await fetch('http://localhost:8000/carbon/buy', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ credit_id })
    });
    if (res.ok) {
      alert('Compra realizada!');
    } else {
      alert('Erro ao comprar crédito');
    }
  };

  // Converter moeda
  const handleConvert = async () => {
    if (!price || !currency) return;
    const res = await fetch(`http://localhost:8000/currency/convert?amount=${price}&from_currency=${currency}&to_currency=USD`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      const data = await res.json();
      setConverted(data.amount);
    } else {
      alert('Erro na conversão de moeda');
    }
  };

  // Validar crédito
  const handleValidate = async (credit_id) => {
    const res = await fetch(`http://localhost:8000/carbon/validate?credit_id=${credit_id}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      alert('Crédito validado!');
    } else {
      alert('Erro na validação');
    }
  };

  return (
    <div>
      <h2>Marketplace de Créditos de Carbono</h2>
      <form onSubmit={handleSell}>
        <input
          type="number"
          placeholder="Quantidade (kgCO2)"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Preço"
          value={price}
          onChange={e => setPrice(e.target.value)}
          required
        />
        <select value={currency} onChange={e => setCurrency(e.target.value)}>
          <option value="BRL">BRL</option>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
        </select>
        <button type="button" onClick={handleConvert}>Converter para USD</button>
        {converted && <span>Valor em USD: {converted}</span>}
        <button type="submit">Vender Crédito</button>
      </form>
      <h3>Créditos Disponíveis</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Quantidade</th>
            <th>Preço</th>
            <th>Moeda</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {credits.map(c => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.amount}</td>
              <td>{c.price}</td>
              <td>{c.currency || 'BRL'}</td>
              <td>{c.verified || 'pendente'}</td>
              <td>
                <button onClick={() => handleBuy(c.id)}>Comprar</button>
                <button onClick={() => handleValidate(c.id)}>Validar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Minhas Transações</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Comprador</th>
            <th>Vendedor</th>
            <th>Quantidade</th>
            <th>Preço</th>
            <th>Moeda</th>
            <th>Data/Hora</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(t => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.buyer_id}</td>
              <td>{t.seller_id}</td>
              <td>{t.amount}</td>
              <td>{t.price}</td>
              <td>{t.currency || 'BRL'}</td>
              <td>{new Date(t.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CarbonMarketplace;
