import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Footer from '../components/Footer';
import './AdminPage.css';

function AdminPage() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleLogin = async (e) => {
		e.preventDefault();
		setError('');
		setIsLoading(true);

		try {
			const formData = new URLSearchParams();
			formData.append('username', username);
			formData.append('password', password);

			const response = await fetch('http://localhost:8000/auth/token', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				body: formData
			});

			if (response.ok) {
				const data = await response.json();
				// Salvar o token no localStorage
				localStorage.setItem('token', data.access_token);
				navigate('/admin/dashboard');
			} else {
				const errorData = await response.json();
				setError(errorData.detail || 'Erro ao fazer login');
			}
		} catch (error) {
			setError('Erro ao conectar com o servidor');
			console.error('Erro:', error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<>
			<div className="admin-page">
				<img 
					src="/bg_images/desktop/desktop_bg1.png" 
					alt="background" 
					className="background-image"
				/>
				<div className="background-blur"></div>
				<div className="content">
					<div className="login-container">
						<h1>Página do Administrador</h1>
						{error && <div className="error-message">{error}</div>}
						<form onSubmit={handleLogin}>
							<div className="form-group">
								<label htmlFor="username">Login:</label>
								<input
									type="text"
									id="username"
									value={username}
									onChange={(e) => setUsername(e.target.value)}
									required
								/>
							</div>
							<div className="form-group">
								<label htmlFor="password">Senha:</label>
								<input
									type="password"
									id="password"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									required
								/>
							</div>
							<button type="submit" className="login-btn" disabled={isLoading}>
								{isLoading ? 'Entrando...' : 'Entrar'}
							</button>
							<div className="forgot-password-link">
								<Link to="/forgot-password">Esqueci minha senha</Link>
							</div>
						</form>
					</div>
				</div>
			</div>
			<Footer />
		</>
	)
}

export default AdminPage;