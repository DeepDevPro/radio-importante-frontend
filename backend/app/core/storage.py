import boto3
from botocore.config import Config
from fastapi import UploadFile
import os
from typing import Optional
from datetime import datetime, timedelta

class StorageManager:
    def __init__(self):
        self.region = os.getenv("DO_SPACES_REGION", "nyc3")
        self.bucket = os.getenv("DO_SPACES_BUCKET", "radio-importante")
        self.key = os.getenv("DO_SPACES_KEY")
        self.secret = os.getenv("DO_SPACES_SECRET")
        
        # Configurar o cliente S3 para Digital Ocean Spaces
        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            endpoint_url=f'https://{self.region}.digitaloceanspaces.com',
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            config=Config(signature_version='s3v4')
        )

    async def upload_file(self, file: UploadFile, folder: str = "musicas") -> Optional[str]:
        """
        Faz upload de um arquivo para o Digital Ocean Spaces
        Retorna o caminho do arquivo se bem sucedido, None caso contrário
        """
        try:
            # Criar o caminho completo do arquivo
            file_path = f"{folder}/{file.filename}"
            
            # Ler o conteúdo do arquivo
            file_content = await file.read()
            
            # Fazer upload para o Spaces
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=file_path,
                Body=file_content,
                ContentType=file.content_type
            )
            
            # Retornar apenas o caminho do arquivo, não a URL completa
            return file_path
            
        except Exception as e:
            print(f"Erro no upload: {str(e)}")
            return None

    def get_signed_url(self, file_path: str, expires_in: int = 3600) -> Optional[str]:
        """
        Gera uma URL assinada temporária para um arquivo
        :param file_path: Caminho do arquivo no bucket
        :param expires_in: Tempo de expiração em segundos (padrão: 1 hora)
        :return: URL assinada ou None se houver erro
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': file_path
                },
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            print(f"Erro ao gerar URL assinada: {str(e)}")
            return None

    def delete_file(self, file_path: str) -> bool:
        """
        Deleta um arquivo do Digital Ocean Spaces
        Retorna True se bem sucedido, False caso contrário
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket,
                Key=file_path
            )
            return True
        except Exception as e:
            print(f"Erro ao deletar arquivo: {str(e)}")
            return False

# Criar uma instância global do StorageManager
storage_manager = StorageManager() 