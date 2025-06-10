import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('/api/products/')
      .then(response => setProducts(response.data))
      .catch(error => console.error('Ошибка:', error));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Товары с Wildberries</h1>
      <table border="1" style={{ width: '100%' }}>
        <thead>
          <tr>
            <th>Название</th>
            <th>Цена (₽)</th>
            <th>Ссылка</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            <tr key={product.id}>
              <td>{product.name}</td>
              <td>{product.price}</td>
              <td><a href={product.url} target="_blank" rel="noreferrer">Открыть</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
