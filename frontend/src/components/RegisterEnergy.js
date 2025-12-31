import React, { useState } from 'react';

function RegisterEnergy({ onRegister }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onRegister(parseFloat(value));
    setValue('');
  };

  return (
    <div>
      <h2>Registrar Consumo</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Consumo (kWh)"
          value={value}
          onChange={e => setValue(e.target.value)}
          required
        />
        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default RegisterEnergy;
