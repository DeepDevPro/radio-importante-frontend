import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Modal from 'react-modal'
import App from './App.jsx'
import AdminPage from './pages/AdminPage.jsx'
import AdminDashboard from './pages/AdminDashboard.jsx'
import ForgotPasswordPage from './pages/ForgotPasswordPage.jsx'
import ResetPasswordPage from './pages/ResetPasswordPage.jsx'
import './index.css'

// Configurar o Modal
Modal.setAppElement('#root')

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<App />} />
        <Route path='/admin' element={<AdminPage />} />
        <Route path='/admin/dashboard' element={<AdminDashboard />} />
        <Route path='/forgot-password' element={<ForgotPasswordPage />} />
        <Route path='/reset-password' element={<ResetPasswordPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
