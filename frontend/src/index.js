import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { GoogleOAuthProvider } from '@react-oauth/google'; // <--- Importe isso

const root = ReactDOM.createRoot(document.getElementById('root'));

// Substitua pelo SEU Client ID do Google Cloud (O público, não o secreto!)
const GOOGLE_CLIENT_ID = "974157308501-h997tn5ejlmbfh35ebtia6ie18b4d0bs.apps.googleusercontent.com";

root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <App />
    </GoogleOAuthProvider>
  </React.StrictMode>
);
