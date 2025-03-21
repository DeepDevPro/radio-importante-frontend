import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ForgotPasswordPage.css';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      setMessage('Por favor, preencha o campo de email.');
      return;
    }
    
    setIsLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/auth/request-password-reset', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setIsSuccess(true);
        setMessage('Se o email existir em nossa base, você receberá as instruções para redefinir sua senha.');
      } else {
        throw new Error(data.detail || 'Ocorreu um erro ao processar sua solicitação.');
      }
    } catch (error) {
      setMessage('Erro ao conectar com o servidor. Tente novamente mais tarde.');
      console.error('Erro na recuperação de senha:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>Recuperação de Senha</h2>
        {!isSuccess ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Seu email"
                autoComplete="email"
              />
            </div>
            {message && (
              <div className={`message ${isSuccess ? 'success' : 'error'}`}>
                {message}
              </div>
            )}
            <div className="buttons">
              <button 
                type="button" 
                onClick={() => navigate('/admin')}
                className="secondary-button"
              >
                Voltar
              </button>
              <button 
                type="submit" 
                disabled={isLoading}
                className="primary-button"
              >
                {isLoading ? 'Enviando...' : 'Enviar'}
              </button>
            </div>
          </form>
        ) : (
          <div className="success-container">
            <p>{message}</p>
            <button 
              onClick={() => navigate('/admin')}
              className="primary-button"
            >
              Voltar para Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
