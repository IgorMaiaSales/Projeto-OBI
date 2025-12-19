import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../App.css';

function Cadastro() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [erro, setErro] = useState(null);
  
  const navigate = useNavigate();

  const handleCadastro = async (e) => {
    e.preventDefault();
    setErro(null);

    try {
      const resposta = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });

      if (resposta.ok) {
        alert("Conta criada com sucesso! Agora faça login.");
        navigate('/login');
      } else {
        const dados = await resposta.json();
        // Se o usuário já existe, o Django avisa aqui
        setErro(dados.username ? "Este nome de usuário já existe." : "Erro ao criar conta.");
      }
    } catch (error) {
      setErro("Erro de conexão.");
    }
  };

  return (
    <div className="App" style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' }}>
      <div style={{ background: 'white', padding: '40px', borderRadius: '10px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', color: '#333' }}>Crie sua Conta</h2>
        
        <form onSubmit={handleCadastro}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', color: '#666' }}>Usuário</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} style={{ width: '100%', padding: '10px' }} required />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', color: '#666' }}>Email (Opcional)</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', padding: '10px' }} />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', color: '#666' }}>Senha</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%', padding: '10px' }} required />
          </div>

          {erro && <p style={{ color: 'red', textAlign: 'center' }}>{erro}</p>}

          <button type="submit" style={{ width: '100%', padding: '12px', background: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>
            CADASTRAR
          </button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <Link to="/login" style={{ color: '#2196F3' }}>Já tem conta? Faça Login</Link>
        </div>
      </div>
    </div>
  );
}

export default Cadastro;