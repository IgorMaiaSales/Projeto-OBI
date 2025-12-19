import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useGoogleLogin } from '@react-oauth/google'; // Hook do Google

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });
  
  const navigate = useNavigate();

  // --- Lógica do Login Normal (Usuário/Senha) ---
  const handleLogin = async (e) => {
    e.preventDefault();
    setMensagem({ texto: '', tipo: '' });

    try {
      const resposta = await fetch('http://127.0.0.1:8000/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }) // ou email
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        localStorage.setItem('access_token', dados.access_token); // Nota: dj-rest-auth usa 'access_token' ou 'key' dependendo da config
        localStorage.setItem('refresh_token', dados.refresh_token);
        navigate('/');
      } else {
        setMensagem({ texto: 'Usuário ou senha incorretos.', tipo: 'erro' });
      }
    } catch (error) {
      setMensagem({ texto: 'Erro ao conectar com o servidor.', tipo: 'erro' });
    }
  };

  // --- Lógica do Login com Google ---
  const googleLogin = useGoogleLogin({
    flow: 'auth-code', // Importante: Pede o 'code' para o Backend trocar
    onSuccess: async (codeResponse) => {
        try {
            const resposta = await fetch('http://127.0.0.1:8000/auth/google/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code: codeResponse.code 
                })
            });
            
            const dados = await resposta.json();
            
            // --- DEBUG: ISSO VAI MOSTRAR NO CONSOLE O QUE O BACKEND DEVOLVEU ---
            console.log("Resposta do Backend (Google):", dados); 
            
            if (resposta.ok) {
                // CORREÇÃO AQUI:
                // Tenta pegar o token de 'access' (JWT), 'access_token' (Custom) ou 'key' (Padrão Django)
                const tokenRecebido = dados.access || dados.access_token || dados.key;

                if (tokenRecebido) {
                    localStorage.setItem('access_token', tokenRecebido);
                    // Se tiver refresh token, salva também (opcional, depende do backend)
                    if (dados.refresh || dados.refresh_token) {
                        localStorage.setItem('refresh_token', dados.refresh || dados.refresh_token);
                    }
                    navigate('/');
                } else {
                    setMensagem({ texto: 'Token não encontrado na resposta.', tipo: 'erro' });
                    console.error("Estrutura inesperada:", dados);
                }
            } else {
                setMensagem({ texto: 'Erro na validação do Google pelo servidor.', tipo: 'erro' });
                console.error(dados);
            }
        } catch (err) {
            setMensagem({ texto: 'Erro de comunicação com o Backend.', tipo: 'erro' });
            console.error(err);
        }
    },
    onError: () => {
        setMensagem({ texto: 'Login com Google falhou.', tipo: 'erro' });
    }
  });

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f0f2f5' }}>
      <div style={{ background: 'white', padding: '40px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', color: '#333', marginBottom: '20px' }}>Entrar</h2>
        
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

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Usuário ou Email</label>
            <input 
              type="text" value={username} onChange={(e) => setUsername(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#555' }}>Senha</label>
            <input 
              type="password" value={password} onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
            />
          </div>

          <button type="submit" style={{ width: '100%', padding: '12px', background: '#2196F3', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px', cursor: 'pointer', fontWeight: 'bold' }}>
            ENTRAR COM E-MAIL
          </button>
        </form>

        <div style={{ display: 'flex', alignItems: 'center', margin: '20px 0' }}>
            <div style={{ flex: 1, height: '1px', background: '#e0e0e0' }}></div>
            <span style={{ padding: '0 10px', color: '#999', fontSize: '0.9rem' }}>OU</span>
            <div style={{ flex: 1, height: '1px', background: '#e0e0e0' }}></div>
        </div>

        {/* Botão Google Oficial */}
        <button onClick={() => googleLogin()} style={{ 
            width: '100%', padding: '10px', background: '#fff', color: '#555', 
            border: '1px solid #ddd', borderRadius: '4px', cursor: 'pointer', 
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px',
            fontWeight: '500', transition: 'background 0.2s'
        }}>
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="G" width="20" />
            Entrar com Google
        </button>

        <div style={{ marginTop: '25px', textAlign: 'center' }}>
            <span style={{ color: '#666' }}>Não tem conta? </span>
            <Link to="/cadastro" style={{ color: '#2196F3', fontWeight: 'bold', textDecoration: 'none' }}>Cadastre-se</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;