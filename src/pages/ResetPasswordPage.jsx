import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { API_URL } from '../config';
import './ResetPasswordPage.css';

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    new_password: '',
    confirm_password: '',
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.new_password !== formData.confirm_password) {
      setMessage('As senhas não coincidem.');
      return;
    }

    setIsLoading(true);
    setMessage('');

    try {
      const formData = new URLSearchParams();
      formData.append('token', token);
      formData.append('new_password', formData.new_password);

      const response = await fetch(`${API_URL}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      if (response.ok) {
        setIsSuccess(true);
        setMessage('Senha alterada com sucesso!');
        navigate('/admin', { state: { message: 'Senha redefinida com sucesso!' } });
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || 'Erro ao redefinir a senha.');
      }
    } catch (error) {
      setMessage('Erro ao conectar com o servidor. Tente novamente mais tarde.');
      console.error('Erro:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (!token) {
    return (
      <div className="reset-password-container">
        <div className="reset-password-card">
          <h2>Link Inválido</h2>
          <p>O link de redefinição de senha é inválido ou expirou.</p>
          <button 
            onClick={() => navigate('/admin')}
            className="primary-button"
          >
            Voltar para Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reset-password-container">
      <div className="reset-password-card">
        <h2>Redefinir Senha</h2>
        {!isSuccess ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="new_password">Nova Senha:</label>
              <input
                type="password"
                id="new_password"
                name="new_password"
                value={formData.new_password}
                onChange={handleChange}
                required
                minLength={8}
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirm_password">Confirmar Senha:</label>
              <input
                type="password"
                id="confirm_password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                required
                minLength={8}
              />
            </div>
            <div className="buttons">
              <button 
                type="button" 
                onClick={() => navigate('/admin')}
                className="secondary-button"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                disabled={isLoading}
                className="primary-button"
              >
                {isLoading ? 'Redefinindo...' : 'Redefinir Senha'}
              </button>
            </div>
            {message && (
              <div className={`message ${isSuccess ? 'success' : 'error'}`}>
                {message}
              </div>
            )}
          </form>
        ) : (
          <div className="success-container">
            <p>{message}</p>
            <button 
              onClick={() => navigate('/admin')}
              className="primary-button"
            >
              Ir para Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResetPasswordPage;
