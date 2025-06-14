import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [products, setProducts] = useState([]);
  const [sortOrder, setSortOrder] = useState('asc'); // Сортировка
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    axios.get('/api/products/')
      .then(response => setProducts(response.data))
      .catch(error => console.error('Ошибка:', error));
  }, []);

  const sortedProducts = [...products].sort((a, b) => {
    if (sortOrder === 'asc') {
      return a.price - b.price;
    } else {
      return b.price - a.price;
    }
  });

  const filteredProducts = sortedProducts.filter(product => {
    const isWithinPrice = (minPrice === '' || product.price >= minPrice) &&
                         (maxPrice === '' || product.price <= maxPrice);
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
    return isWithinPrice && matchesSearch;
  });

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f0f4f8, #d9e2ec)', // Мягкий светлый градиент
      padding: '40px',
      boxSizing: 'border-box',
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      color: '#333'
    }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Товары с Wildberries</h1>

      <div style={{
        maxWidth: '700px',
        margin: '0 auto 30px auto',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap',
        justifyContent: 'center'
      }}>
        <input
          type="text"
          placeholder="Поиск по названию"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{ flex: '1 1 200px', padding: '8px', borderRadius: '6px', border: '1px solid #ccc' }}
        />
        <input
          type="number"
          placeholder="Минимальная цена"
          value={minPrice}
          onChange={e => setMinPrice(e.target.value)}
          style={{ width: '140px', padding: '8px', borderRadius: '6px', border: '1px solid #ccc' }}
        />
        <input
          type="number"
          placeholder="Максимальная цена"
          value={maxPrice}
          onChange={e => setMaxPrice(e.target.value)}
          style={{ width: '140px', padding: '8px', borderRadius: '6px', border: '1px solid #ccc' }}
        />
        <button
          onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          style={{
            padding: '10px 20px',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: '#3f51b5',
            color: 'white',
            cursor: 'pointer',
            minWidth: '140px'
          }}
        >
          Сортировать по цене: {sortOrder === 'asc' ? 'по убыванию' : 'по возрастанию'}
        </button>
      </div>

      <div style={{
        maxWidth: '900px',
        margin: '0 auto',
        overflowX: 'auto',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        borderRadius: '8px',
        backgroundColor: 'white',
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '600px' }}>
          <thead style={{ backgroundColor: '#f5f7fa' }}>
            <tr>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd', textAlign: 'left' }}>Название</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd', width: '120px' }}>Цена (₽)</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd', width: '120px' }}>Ссылка</th>
            </tr>
          </thead>
          <tbody>
            {filteredProducts.map(product => (
              <tr key={product.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '12px' }}>{product.name}</td>
                <td style={{ padding: '12px' }}>{product.price}</td>
                <td style={{ padding: '12px' }}>
                  <a href={product.url} target="_blank" rel="noreferrer" style={{ color: '#3f51b5', textDecoration: 'none' }}>
                    Открыть
                  </a>
                </td>
              </tr>
            ))}
            {filteredProducts.length === 0 && (
              <tr>
                <td colSpan="3" style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                  Нет товаров по заданным параметрам
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
