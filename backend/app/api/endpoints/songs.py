from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.storage import storage_manager

from app.db.models import Song, get_db
from app.api.schemas import Song as SongSchema, SongCreate, SongUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=SongSchema)
async def create_song(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(...),
    duration: int = Form(0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cria uma nova música com upload de arquivo (requer autenticação de admin).
    """
    # Validar tipo de arquivo
    if not file.content_type.startswith('audio/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo deve ser um arquivo de áudio"
        )

    # Fazer upload do arquivo para o Digital Ocean Spaces
    file_path = await storage_manager.upload_file(file)
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao fazer upload do arquivo"
        )

    # Criar a música no banco de dados
    db_song = Song(
        title=title,
        artist=artist,
        file_path=file_path,
        duration=duration
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    # Gerar URL assinada para o arquivo
    signed_url = storage_manager.get_signed_url(db_song.file_path)
    if not signed_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar URL do arquivo"
        )

    # Adicionar a URL assinada à resposta
    response_song = SongSchema.model_validate(db_song)
    response_song.file_url = signed_url
    return response_song

@router.get("/", response_model=List[SongSchema])
def read_songs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de músicas com URLs assinadas.
    """
    songs = db.query(Song).offset(skip).limit(limit).all()
    response_songs = []
    
    for song in songs:
        song_schema = SongSchema.model_validate(song)
        signed_url = storage_manager.get_signed_url(song.file_path)
        song_schema.file_url = signed_url if signed_url else None
        response_songs.append(song_schema)
    
    return response_songs

@router.get("/{song_id}", response_model=SongSchema)
def read_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna uma música específica pelo ID.
    """
    song = db.query(Song).filter(Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return song

@router.put("/{song_id}", response_model=SongSchema)
def update_song(
    song_id: int,
    song: SongUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza uma música (requer autenticação de admin).
    """
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    update_data = song.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_song, field, value)
    
    db.commit()
    db.refresh(db_song)
    return db_song

@router.delete("/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Remove uma música (requer autenticação de admin).
    """
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    db.delete(db_song)
    db.commit()
    return {"message": "Música removida com sucesso"}
