import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './paginas/Home';
import Resolver from './paginas/Resolver'; 
import Login from './paginas/Login';
import Cadastro from './paginas/Cadastro';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota da Página Inicial */}
        <Route path="/" element={<Home />} />

        {/* Rota da Página de Login */}
        <Route path="/login" element={<Login />} />

        {/* Rota da Página de Cadastro */}
        <Route path="/cadastro" element={<Cadastro />} />
        
        {/* Rota da Página de Resolução */}
        <Route path="/resolver/:slug" element={<Resolver />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;