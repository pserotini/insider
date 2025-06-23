# Arquitetura da Solução - Titanic ML API

Este documento descreve, de forma simplificada, a arquitetura do projeto com foco na automação de deploy e estrutura da aplicação.

## Visão Geral

O fluxo a seguir descreve como o código vai do GitHub até a execução da API na EC2:

```
[Developer] 
     │
     ▼
[GitHub Repository]
     │ (merge to main)
     ▼
[GitHub Actions CI/CD Pipeline]
     │
     ├──> Executa testes com pytest
     ├──> Copia os arquivos via scp
     └──> Reinicia a API via ssh na EC2
             │
             ▼
     [EC2 Instance AWS]
             │
             ▼
     [Docker Container]
             │
             ▼
     [FastAPI Application]
             │
             ├──> POST /predict
             ├──> POST /load
             ├──> GET /history
             └──> GET /health
```

## Componentes

- **FastAPI**: Framework web leve para servir o modelo via HTTP.
- **Docker**: Isolamento e portabilidade da aplicação.
- **EC2 (AWS)**: Infraestrutura de nuvem usada para servir a aplicação.
- **GitHub Actions**: Pipeline de CI/CD configurada para testar e atualizar automaticamente o serviço.

## Acesso Público

- Documentação da API:  
  http://ec2-3-138-186-68.us-east-2.compute.amazonaws.com:8000