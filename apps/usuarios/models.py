from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser, 
    PermissionsMixin
)

# Create your models here.

class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None):
        usuario = self.model(
            email=self.normalize_email(email) # normaliza o e-mail para salvar no banco
        )
        # Explicitando informações
        usuario.is_active = True
        usuario.is_staff = False
        usuario.is_superuser = False

        if password:
            usuario.set_password(password) # método da AbstractBaseUser

        usuario.save() # método da AbstractBaseUser

        return usuario
    
    def create_superuser(self, email, password):
        usuario = self.create_user(email, password)

        # Explicitando informações
        usuario.is_active = True
        usuario.is_staff = True
        usuario.is_superuser = True

        usuario.set_password(password) # método da AbstractBaseUser

        usuario.save()

        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(
        verbose_name="E-mail do usuário",
        max_length=194,
        unique=True,
    )

    is_active = models.BooleanField(
        verbose_name="Usuário está ativo",
        default=True,
    )

    is_staff = models.BooleanField(
        verbose_name="Usuário é da equipe de desenvolvimento",
        default=False,
    )
    
    is_superuser = models.BooleanField(
        verbose_name="Usuário é um superusuário",
        default=False,
    )

    USERNAME_FIELD = "email" # campo usado para autenticação

    objects = UsuarioManager() # Manager padrão

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "usuario" # nome da tabela no banco de dados

    def __str__(self):
        return self.email