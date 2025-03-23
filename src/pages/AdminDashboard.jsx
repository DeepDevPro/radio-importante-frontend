import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import Modal from 'react-modal';
import { useDropzone } from 'react-dropzone';
import Footer from '../components/Footer';
import { API_URL } from '../config';
import './AdminDashboard.css';

// Vincular o modal ao elemento root da aplicação
Modal.setAppElement('#root');

function AdminDashboard() {
    const [selectedPeriod, setSelectedPeriod] = useState({ value: '7days', label: '7 dias' });
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadStatus, setUploadStatus] = useState('');
    const [songs, setSongs] = useState([]);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const onDrop = useCallback(acceptedFiles => {
        setUploadedFiles(prev => [...prev, ...acceptedFiles]);
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'audio/mpeg': ['.mp3'],
            'audio/wav': ['.wav']
        }
    });

    const periodOptions = [
        { value: '7days', label: '7 dias' },
        { value: '30days', label: '30 dias' },
        { value: 'alltime', label: 'Todo o período' }
    ];

    const customStyles = {
        control: (provided, state) => ({
            ...provided,
            backgroundColor: 'rgba(30, 30, 30, 0.9)',
            borderColor: state.isFocused ? '#ebd0aa' : 'rgba(235, 208, 170, 0.2)',
            borderRadius: '12px',
            padding: '0.2rem',
            boxShadow: 'none',
            '&:hover': {
                borderColor: 'rgba(235, 208, 170, 0.4)'
            }
        }),
        menu: (provided) => ({
            ...provided,
            backgroundColor: 'rgba(30, 30, 30, 0.98)',
            border: '1px solid rgba(235, 208, 170, 0.2)',
            borderRadius: '8px',
            padding: '0.5rem'
        }),
        option: (provided, state) => ({
            ...provided,
            backgroundColor: state.isSelected ? 'rgba(235, 208, 170, 0.2)' : 
                           state.isFocused ? 'rgba(235, 208, 170, 0.1)' : 'transparent',
            color: '#ebd0aa',
            cursor: 'pointer',
            '&:active': {
                backgroundColor: 'rgba(235, 208, 170, 0.3)'
            }
        }),
        singleValue: (provided) => ({
            ...provided,
            color: '#ebd0aa'
        }),
        dropdownIndicator: (provided) => ({
            ...provided,
            color: '#ebd0aa',
            '&:hover': {
                color: '#ebd0aa'
            }
        }),
        indicatorSeparator: () => ({
            display: 'none'
        })
    };

    // Estilos do Modal
    const modalStyles = {
        overlay: {
            backgroundColor: 'rgba(0, 0, 0, 0.75)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0
        },
        content: {
            position: 'relative',
            background: 'none',
            border: 'none',
            padding: 0,
            top: 'auto',
            left: 'auto',
            right: 'auto',
            bottom: 'auto',
            maxWidth: '500px',
            width: '90%',
            margin: '0 auto',
            overflow: 'visible',
            inset: 'auto'
        }
    };

    useEffect(() => {
        fetchSongs();
    }, []);

    const fetchSongs = async () => {
        setIsLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/admin');
                return;
            }

            const response = await fetch(`${API_URL}/songs/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setSongs(data);
            } else if (response.status === 401) {
                localStorage.removeItem('token');
                navigate('/admin');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Erro ao carregar as músicas');
            }
        } catch (error) {
            setError('Erro ao conectar com o servidor');
            console.error('Erro:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUploadClick = () => {
        setIsUploadModalOpen(true);
    };

    const closeUploadModal = () => {
        setIsUploadModalOpen(false);
        setUploadedFiles([]);
    };

    const handleUpload = async () => {
        if (uploadedFiles.length === 0) return;

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                setUploadStatus('Erro: Token não encontrado. Por favor, faça login novamente.');
                return;
            }

            setUploadStatus('Iniciando upload...');
            const totalFiles = uploadedFiles.length;
            let completedFiles = 0;

            for (const file of uploadedFiles) {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('title', file.name.replace(/\.[^/.]+$/, "")); // Remove extensão
                formData.append('artist', 'Artista'); // Você pode adicionar um campo para o artista no formulário
                formData.append('duration', 0); // A duração será calculada no backend

                setUploadStatus(`Enviando ${file.name}...`);

                const response = await fetch('http://localhost:8000/songs/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Erro ao fazer upload de ${file.name}`);
                }

                completedFiles++;
                setUploadProgress((completedFiles / totalFiles) * 100);
            }

            setUploadStatus('Upload concluído com sucesso!');
            setTimeout(() => {
                setUploadedFiles([]);
                setUploadProgress(0);
                setUploadStatus('');
                closeUploadModal();
            }, 2000);
        } catch (error) {
            console.error('Erro no upload:', error);
            setUploadStatus(`Erro no upload: ${error.message}`);
        }
    };

    return (
        <>
            <div className="dashboard-page">
                <div className="background-blur"></div>
                <div className="dashboard-content">
                    {/* Bloco do topo */}
                    <div className="top-block">
                        <div className="top-left">
                            <h1>Radio Importante</h1>
                            <h2>Painel de Controle do Administrador</h2>
                        </div>
                        <div className="top-right">
                            <button className="upload-btn" onClick={handleUploadClick}>
                                Upload
                            </button>
                        </div>
                    </div>

                    {/* Seção principal */}
                    <div className="main-section">
                        {/* Coluna da esquerda (1/3) */}
                        <div className="stats-column">
                            <div className="period-selector">
                                <Select
                                    value={selectedPeriod}
                                    onChange={setSelectedPeriod}
                                    options={periodOptions}
                                    styles={customStyles}
                                    isSearchable={false}
                                />
                            </div>

                            <div className="stats-cards">
                                <div className="stat-card">
                                    <h3>Total de Ouvintes</h3>
                                    <p className="stat-value">1,234</p>
                                </div>
                                <div className="stat-card">
                                    <h3>Média de Tempo de Audição por Ouvinte</h3>
                                    <p className="stat-value">45 min</p>
                                </div>
                            </div>
                        </div>

                        {/* Coluna da direita (2/3) */}
                        <div className="songs-column">
                            <div className="songs-list">
                                <div className="songs-header">
                                    <span>Nome do Artista</span>
                                    <span>Nome da Música</span>
                                    <span>Ações</span>
                                </div>
                                {/* Lista exemplo */}
                                <div className="song-item">
                                    <span>Artista Exemplo</span>
                                    <span>Música Exemplo</span>
                                    <button className="delete-btn">Excluir</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <Footer />
            {/* Modal permanece aqui fora do dashboard-page */}
            <Modal
                isOpen={isUploadModalOpen}
                onRequestClose={closeUploadModal}
                style={modalStyles}
                contentLabel="Upload Modal"
            >
                <div className="upload-modal">
                    <button className="close-modal-btn" onClick={closeUploadModal}>×</button>
                    <h2>Upload de Músicas</h2>
                    
                    <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
                        <input {...getInputProps()} />
                        {isDragActive ? (
                            <p>Solte os arquivos aqui...</p>
                        ) : (
                            <p>Arraste e solte arquivos MP3 aqui, ou clique para selecionar</p>
                        )}
                    </div>

                    {uploadedFiles.length > 0 && (
                        <div className="uploaded-files">
                            <h3>Arquivos selecionados:</h3>
                            <ul>
                                {uploadedFiles.map((file, index) => (
                                    <li key={index}>{file.name}</li>
                                ))}
                            </ul>
                            {uploadStatus && (
                                <div className="upload-status">
                                    <p>{uploadStatus}</p>
                                    {uploadProgress > 0 && (
                                        <div className="progress-bar">
                                            <div 
                                                className="progress-fill" 
                                                style={{ width: `${uploadProgress}%` }}
                                            ></div>
                                        </div>
                                    )}
                                </div>
                            )}
                            <button className="upload-submit-btn" onClick={handleUpload}>
                                Fazer Upload
                            </button>
                        </div>
                    )}
                </div>
            </Modal>
        </>
    );
}

export default AdminDashboard;
