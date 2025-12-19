import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Cadastro() {
  const [formData, setFormData] = useState({ username: '', email: '', password: '', password2: '' });
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCadastro = async (e) => {
    e.preventDefault();
    setMensagem({ texto: '', tipo: '' });
    
    if (formData.password !== formData.password2) {
        setMensagem({ texto: 'As senhas não coincidem.', tipo: 'erro' });
        return;
    }

    setLoading(true);

    try {
      const resposta = await fetch('http://127.0.0.1:8000/auth/registration/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const dados = await resposta.json();

      if (resposta.ok) {
        // Sucesso
        setMensagem({ 
            texto: 'Conta criada! Verifique seu email ou faça login.', 
            tipo: 'sucesso' 
        });
        // Opcional: Redirecionar após 2 segundos
        setTimeout(() => navigate('/login'), 2000);
      } else {
        // Erro de Validação do Django
        let msgErro = 'Erro ao criar conta.';
        if (dados.email) msgErro = `Email: ${dados.email[0]}`;
        if (dados.username) msgErro = `Usuário: ${dados.username[0]}`;
        if (dados.password) msgErro = `Senha: ${dados.password[0]}`;
        
        setMensagem({ texto: msgErro, tipo: 'erro' });
      }
    } catch (error) {
      setMensagem({ texto: 'Erro de conexão.', tipo: 'erro' });
    } finally {
        setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' }}>
      <div style={{ background: 'white', padding: '40px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', color: '#333' }}>Crie sua Conta</h2>
        
        {mensagem.texto && (
          <div style={{ 
            padding: '10px', marginBottom: '15px', borderRadius: '4px', textAlign: 'center',
            backgroundColor: mensagem.tipo === 'erro' ? '#ffebee' : '#e8f5e9',
            color: mensagem.tipo === 'erro' ? '#c62828' : '#2e7d32',
            border: `1px solid ${mensagem.tipo === 'erro' ? '#ef9a9a' : '#a5d6a7'}`
          }}>
            {mensagem.texto}
          </div>
        )}

        <form onSubmit={handleCadastro}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Usuário</label>
            <input name="username" type="text" onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }} required />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Email</label>
            <input name="email" type="email" onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }} required />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Senha</label>
            <input name="password" type="password" onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }} required />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Confirmar Senha</label>
            <input name="password2" type="password" onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' }} required />
          </div>

          <button type="submit" disabled={loading} style={{ width: '100%', padding: '12px', background: loading ? '#ccc' : '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: loading ? 'default' : 'pointer' }}>
            {loading ? 'CRIANDO...' : 'CADASTRAR'}
          </button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <Link to="/login" style={{ color: '#2196F3', textDecoration: 'none' }}>Já tem conta? Faça Login</Link>
        </div>
      </div>
    </div>
  );
}

export default Cadastro;