import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../App.css';

function Resolver() {
  const { slug } = useParams();
  const [problema, setProblema] = useState(null);
  const [codigo, setCodigo] = useState(""); 
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/problemas/${slug}/`) 
      .then(res => res.json())
      .then(data => {
        setProblema(data);
        setCodigo("# Escreva sua solução em Python:\n# Dica: Use sys.stdin.read().split() para ler entrada robusta\nimport sys\n\n");
      })
      .catch(err => console.error("Erro:", err));
  }, [slug]);

  const submeter = async () => {
    const token = localStorage.getItem('access_token'); 
    
    // Debug para ver se o token existe antes de enviar
    console.log("Token sendo enviado:", token); 

    if (!token) {
      alert("Você precisa estar logado para enviar soluções!");
      return;
    }
    setCarregando(true);
    setResultado(null);

    try {
      const resposta = await fetch(`http://127.0.0.1:8000/problemas/${slug}/submeter/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({ codigo: codigo })
      });
      
      const dados = await resposta.json();
      if (resposta.status === 401) {
        alert("Sua sessão expirou.");
      } else {
        setResultado(dados); 
      }
    } catch (erro) {
      alert("Erro de conexão.");
    } finally {
      setCarregando(false);
    }
  };

  if (!problema) return <div style={{padding: '50px', textAlign: 'center'}}>Carregando...</div>;

  return (
    <div className="App" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto', textAlign: 'left' }}>
      
      {/* Cabeçalho Rico */}
      <div style={{ marginBottom: '20px', borderBottom: '1px solid #ccc', paddingBottom: '15px' }}>
        <h1 style={{ margin: '0 0 10px 0', color: '#2c3e50' }}>{problema.titulo}</h1>
        
        <div style={{ display: 'flex', gap: '15px', fontSize: '0.9rem', color: '#555' }}>
            <span style={{ background: '#e3f2fd', color: '#0277bd', padding: '5px 10px', borderRadius: '15px', fontWeight: 'bold' }}>
                {problema.nivel_extenso}
            </span>
            <span style={{ background: '#f3e5f5', color: '#7b1fa2', padding: '5px 10px', borderRadius: '15px' }}>
                {problema.ano}
            </span>
            <span style={{ background: '#e0f2f1', color: '#00695c', padding: '5px 10px', borderRadius: '15px' }}>
                Fase {problema.fase}
            </span>
            <span style={{ background: '#ffebee', color: '#c62828', padding: '5px 10px', borderRadius: '15px' }}>
                Tempo Limite: {problema.time_limit} ms
            </span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        
        {/* Coluna da Esquerda: Enunciado */}
        <div style={{ backgroundColor: '#fff', padding: '25px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
          
          <h3 style={{ marginTop: 0 }}>Descrição</h3>
          <div style={{lineHeight: '1.6', color: '#333'}} dangerouslySetInnerHTML={{ __html: problema.enunciado }} />

          <h4 style={{marginTop: '25px'}}>Entrada</h4>
          <p style={{background: '#fafafa', padding: '10px', borderLeft: '4px solid #ddd'}}>{problema.entrada}</p>

          <h4>Saída</h4>
          <p style={{background: '#fafafa', padding: '10px', borderLeft: '4px solid #ddd'}}>{problema.saida}</p>

          {problema.restricoes && (
            <div style={{ marginTop: '20px', padding: '15px', background: '#fff8e1', borderRadius: '5px', border: '1px solid #ffe0b2' }}>
                <h4 style={{margin: '0 0 10px 0', color: '#f57f17'}}>Restrições</h4>
                <div dangerouslySetInnerHTML={{ __html: problema.restricoes }} />
            </div>
          )}

          {problema.exemplos && problema.exemplos.length > 0 && (
            <div style={{ marginTop: '30px' }}>
              <h3>Exemplos</h3>
              {problema.exemplos.map((ex, index) => (
                <div key={index} style={{ marginBottom: '20px', border: '1px solid #e0e0e0', borderRadius: '6px', overflow: 'hidden' }}>
                  <div style={{ display: 'flex', borderBottom: '1px solid #eee' }}>
                     <div style={{ flex: 1, padding: '15px', background: '#f8f9fa', borderRight: '1px solid #eee' }}>
                        <strong style={{color: '#555'}}>Entrada</strong>
                        <pre style={{ margin: '10px 0 0 0', fontFamily: 'monospace', fontSize: '1.1em' }}>{ex.entrada_texto}</pre>
                     </div>
                     <div style={{ flex: 1, padding: '15px', background: '#fff' }}>
                        <strong style={{color: '#555'}}>Saída</strong>
                        <pre style={{ margin: '10px 0 0 0', fontFamily: 'monospace', fontSize: '1.1em' }}>{ex.saida_texto}</pre>
                     </div>
                  </div>
                  {ex.explicacao && (
                    <div style={{ padding: '15px', background: '#e8f5e9', fontSize: '0.9rem', color: '#2e7d32', borderTop: '1px solid #c8e6c9' }}>
                        <strong>Explicação:</strong> {ex.explicacao}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Coluna da Direita: Editor */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ marginTop: 0 }}>Sua Solução (Python)</h3>
          
          <textarea
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            spellCheck="false"
            style={{
              flex: 1, minHeight: '500px', fontFamily: '"Fira Code", monospace', padding: '15px',
              backgroundColor: '#1e1e1e', color: '#d4d4d4', border: 'none', borderRadius: '8px 8px 0 0', 
              outline: 'none', fontSize: '14px', lineHeight: '1.5', resize: 'vertical'
            }}
          />

          <button 
            onClick={submeter}
            disabled={carregando}
            style={{
              padding: '18px', backgroundColor: carregando ? '#7f8c8d' : '#27ae60', color: 'white', fontWeight: 'bold',
              border: 'none', borderRadius: '0 0 8px 8px', fontSize: '1.1rem', cursor: 'pointer', transition: 'background 0.3s'
            }}
          >
            {carregando ? "JULGANDO CASOS DE TESTE..." : "ENVIAR SOLUÇÃO 🚀"}
          </button>

          {resultado && (
            <div style={{ 
              marginTop: '20px', padding: '20px', borderRadius: '8px',
              backgroundColor: resultado.erro ? '#ffebee' : (resultado.status === 'Accepted' ? '#e8f5e9' : '#fff3e0'),
              color: resultado.erro ? '#c62828' : (resultado.status === 'Accepted' ? '#2e7d32' : '#ef6c00'),
              border: '1px solid', borderColor: resultado.erro ? '#ef9a9a' : (resultado.status === 'Accepted' ? '#a5d6a7' : '#ffe0b2'),
              textAlign: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                {resultado.erro ? (
                  <h3>⚠️ {resultado.erro}</h3>
                ) : (
                  <>
                    <h2 style={{margin: '5px 0', fontSize: '1.8rem'}}>{resultado.status === 'Accepted' ? "✅ SUCESSO!" : "❌ " + resultado.status}</h2>
                    <p style={{fontSize: '1.1rem'}}>Tempo de Execução: <strong>{resultado.tempo.toFixed(3)}s</strong></p>
                  </>
                )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Resolver;