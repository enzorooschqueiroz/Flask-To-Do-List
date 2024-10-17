# Projeto ToDoList

Este é um projeto de gerenciamento de tarefas hospedado no Azure, acessível na URL [https://prjtodolist.azurewebsites.net](https://prjtodolist.azurewebsites.net). O projeto utiliza **Flask** como framework web e **MongoDB** como banco de dados. O código é containerizado usando **Docker**.

## Funcionalidades

- Cadastro de usuários e login com JWT (JSON Web Tokens)
- Criação, leitura, atualização e exclusão de tarefas (CRUD)
- Integração com MongoDB para persistência de dados
- Sistema de autenticação com JWT
- APIs RESTful para gerenciar usuários e tarefas

## Tecnologias Utilizadas

- **Python 3.9**
- **Flask**
- **MongoDB**
- **JWT (Flask-JWT-Extended)**
- **Docker**
- **Azure App Service** (Hospedagem)
- **Docker Compose** (Ambiente local)

## Deploy na Azure

O projeto está hospedado na Azure App Service usando DockerHub.

## API Endpoints

Aqui está uma descrição detalhada dos endpoints da API no formato Swagger para facilitar a interação com o sistema.

### Endpoints de Usuário

#### 1. **Registro de Usuário**

- **Endpoint**: `/register`
- **Método**: `POST`
- **Descrição**: Registra um novo usuário no sistema.
- **Parâmetros**:
    - `user_name`: String (Obrigatório)
    - `user_email`: String (Obrigatório)
    - `user_password`: String (Obrigatório)
- **Exemplo de Requisição**:
    ```json
    {
      "user_name": "João Silva",
      "user_email": "joao@email.com",
      "user_password": "senha123"
    }
    ```
- **Resposta de Sucesso**:
    ```json
    {
      "message": "User created successfully",
      "user": { /* dados do usuário */ }
    }
    ```

#### 2. **Login de Usuário**

- **Endpoint**: `/login`
- **Método**: `POST`
- **Descrição**: Autentica o usuário e retorna um token JWT.
- **Parâmetros**:
    - `user_email`: String (Obrigatório)
    - `user_password`: String (Obrigatório)
- **Exemplo de Requisição**:
    ```json
    {
      "user_email": "joao@email.com",
      "user_password": "senha123"
    }
    ```
- **Resposta de Sucesso**:
    ```json
    {
      "access_token": "jwt_token_aqui"
    }
    ```

#### 3. **Obter Usuário Atual**

- **Endpoint**: `/user`
- **Método**: `GET`
- **Descrição**: Retorna as informações do usuário autenticado.
- **Autenticação**: JWT Token
- **Exemplo de Resposta**:
    ```json
    {
      "user": {
        "user_id": "12345",
        "user_name": "João Silva",
        "user_email": "joao@email.com"
      }
    }
    ```

#### 4. **Atualizar Usuário**

- **Endpoint**: `/user`
- **Método**: `PUT`
- **Descrição**: Atualiza as informações do usuário autenticado.
- **Autenticação**: JWT Token
- **Parâmetros** (opcional):
    - `user_name`: String
    - `user_password`: String (Será hashada)
- **Exemplo de Requisição**:
    ```json
    {
      "user_name": "João Atualizado",
      "user_password": "nova_senha"
    }
    ```
- **Resposta de Sucesso**:
    ```json
    {
      "message": "User updated successfully",
      "user": { /* dados atualizados do usuário */ }
    }
    ```

#### 5. **Deletar Usuário**

- **Endpoint**: `/user`
- **Método**: `DELETE`
- **Descrição**: Deleta o usuário autenticado do sistema.
- **Autenticação**: JWT Token
- **Exemplo de Resposta**:
    ```json
    {
      "message": "User deleted successfully"
    }
    ```

---

