import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../App.css';

function Home() {
  const [problemas, setProblemas] = useState([]);
  const [usuarioLogado, setUsuarioLogado] = useState(false);
  const navigate = useNavigate();

  // Estados dos Filtros
  const [filtroAno, setFiltroAno] = useState("");
  const [filtroNivel, setFiltroNivel] = useState("");
  const [filtroFase, setFiltroFase] = useState("");

  // Função de busca que reage aos filtros
  const buscarProblemas = () => {
    let url = 'http://127.0.0.1:8000/problemas/?';
    
    // Constrói a Query String
    const params = [];
    if (filtroAno) params.push(`ano=${filtroAno}`);
    if (filtroNivel) params.push(`nivel=${filtroNivel}`);
    if (filtroFase) params.push(`fase=${filtroFase}`);
    
    url += params.join('&');

    fetch(url)
      .then(response => response.json())
      .then(data => setProblemas(data))
      .catch(error => console.error('Erro ao buscar problemas:', error));
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) setUsuarioLogado(true);
    
    // Busca inicial
    buscarProblemas();
  }, []); // Executa apenas na montagem

  // Efeito para buscar automaticamente quando muda o filtro (Opcional, pode ser num botão)
  useEffect(() => {
    buscarProblemas();
  }, [filtroAno, filtroNivel, filtroFase]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUsuarioLogado(false);
    navigate(0); 
  };

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '1000px', margin: '0 auto' }}>
      
      {/* CABEÇALHO */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', borderBottom: '1px solid #eee', paddingBottom: '20px' }}>
        <div>
          <h1 style={{ margin: 0, color: '#2c3e50' }}>Pratique OBI</h1>
          <p style={{ margin: 0, color: '#666' }}>Plataforma de Treinamento</p>
        </div>
        <div>
          {usuarioLogado ? (
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <span style={{ color: 'green', fontWeight: 'bold' }}>● Online</span>
              <button onClick={handleLogout} style={{ padding: '8px 15px', background: '#ff4444', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Sair</button>
            </div>
          ) : (
            <Link to="/login"><button style={{ padding: '10px 20px', background: '#2196F3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Login</button></Link>
          )}
        </div>
      </header>

      {/* BARRA DE FILTROS */}
      <div style={{ display: 'flex', gap: '15px', marginBottom: '30px', background: '#f8f9fa', padding: '15px', borderRadius: '8px' }}>
        <input 
          type="number" 
          placeholder="Ano (ex: 2025)" 
          value={filtroAno} 
          onChange={(e) => setFiltroAno(e.target.value)}
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
        />
        
        <select value={filtroNivel} onChange={(e) => setFiltroNivel(e.target.value)} style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd', minWidth: '150px' }}>
          <option value="">Todos os Níveis</option>
          <option value="PJ">Iniciação (PJ)</option>
          <option value="J">Júnior</option>
          <option value="1">Nível 1</option>
          <option value="2">Nível 2</option>
          <option value="S">Sênior</option>
        </select>

        <select value={filtroFase} onChange={(e) => setFiltroFase(e.target.value)} style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}>
          <option value="">Todas Fases</option>
          <option value="1">Fase 1</option>
          <option value="2">Fase 2</option>
          <option value="3">Fase 3</option>
        </select>
      </div>

      {/* LISTA DE PROBLEMAS (TABELA CLICÁVEL) */}
      <div className="lista-problemas">
        {problemas.length === 0 ? (
          <p style={{textAlign: 'center', color: '#888'}}>Nenhum problema encontrado com esses filtros.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {/* Cabeçalho da Lista */}
            <div style={{ display: 'grid', gridTemplateColumns: '4fr 2fr 1fr 1fr', padding: '10px 20px', fontWeight: 'bold', color: '#555' }}>
              <span>Título</span>
              <span>Nível</span>
              <span>Ano</span>
              <span>Fase</span>
            </div>

            {/* Itens */}
            {problemas.map(problema => (
              <div 
                key={problema.id} 
                onClick={() => navigate(`/resolver/${problema.slug}`)}
                style={{ 
                  display: 'grid', 
                  gridTemplateColumns: '4fr 2fr 1fr 1fr', 
                  padding: '20px', 
                  backgroundColor: '#fff', 
                  border: '1px solid #e0e0e0',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'transform 0.1s, box-shadow 0.1s',
                  alignItems: 'center'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                  e.currentTarget.style.borderColor = '#2196F3';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'none';
                  e.currentTarget.style.boxShadow = 'none';
                  e.currentTarget.style.borderColor = '#e0e0e0';
                }}
              >
                <span style={{ fontWeight: 'bold', color: '#2c3e50', fontSize: '1.1rem' }}>{problema.titulo}</span>
                <span style={{ color: '#0288d1', fontWeight: '500' }}>{problema.nivel_extenso}</span>
                <span style={{ color: '#666' }}>{problema.ano}</span>
                <span style={{ color: '#666' }}>{problema.fase}ª</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;