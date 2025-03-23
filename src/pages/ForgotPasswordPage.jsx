import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config';
import './ForgotPasswordPage.css';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/request-password-reset`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include',
        mode: 'cors',
        body: JSON.stringify({ email })
      });

      if (response.ok) {
        setMessage('Se o email existir em nossa base de dados, você receberá um link para redefinir sua senha.');
        setEmail('');
        setIsSuccess(true);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erro ao processar a solicitação');
      }
    } catch (error) {
      setError('Erro ao conectar com o servidor');
      console.error('Erro:', error);
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
            {error && (
              <div className="error-message">
                {error}
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
