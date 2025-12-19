import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../App.css'; // Para aproveitar o estilo

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [erro, setErro] = useState(null);
  
  // Hook para navegar entre páginas (redirecionar)
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault(); // Não recarrega a página
    setErro(null);

    try {
      const resposta = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        // SUCESSO!
        // 1. Guardamos o token no navegador (localStorage)
        localStorage.setItem('access_token', dados.access);
        localStorage.setItem('refresh_token', dados.refresh);
        
        // 2. Mandamos o usuário para a Home
        alert("Login realizado com sucesso!");
        navigate('/');
      } else {
        // ERRO (Senha errada ou usuário não existe)
        setErro("Usuário ou senha incorretos.");
      }
    } catch (error) {
      setErro("Erro ao conectar com o servidor.");
    }
  };

  return (
    <div className="App" style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' }}>
      <div style={{ 
        background: 'white', padding: '40px', borderRadius: '10px', 
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' 
      }}>
        <h2 style={{ textAlign: 'center', color: '#333', marginTop: 0 }}>Entrar no OBI</h2>
        
        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#666' }}>Usuário</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
              required 
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#666' }}>Senha</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
              required 
            />
          </div>

          {erro && <p style={{ color: 'red', textAlign: 'center' }}>{erro}</p>}

          <button type="submit" style={{ 
            width: '100%', padding: '12px', background: '#2196F3', color: 'white', 
            border: 'none', borderRadius: '5px', fontSize: '16px', cursor: 'pointer', fontWeight: 'bold' 
          }}>
            ENTRAR
          </button>
        </form>

        <div style={{ marginTop: '15px', textAlign: 'center' }}>
            <Link to="/cadastro" style={{ color: '#2196F3', fontSize: '0.9rem' }}>
                Não tem conta? Cadastre-se
            </Link>
        </div>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <Link to="/" style={{ color: '#666', textDecoration: 'none' }}>Voltar para Home</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;