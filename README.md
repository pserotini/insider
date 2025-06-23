
# Titanic Survival Prediction API

Este projeto implementa uma solução de Machine Learning para prever a sobrevivência de passageiros do Titanic com base no dataset clássico disponível no Kaggle. O objetivo principal foi aplicar boas práticas de engenharia, modularização e exposição do modelo via API.

## Funcionalidades

- Modelo treinado com scikit-learn
- Pipeline de pré-processamento encapsulado em uma classe customizada
- API desenvolvida com FastAPI com os seguintes endpoints:
  - `POST /predict`: recebe os dados de um passageiro em JSON e retorna a predição (`0` ou `1`)
  - `POST /load`: permite carregar outro modelo salvo em `.pkl`
  - `GET /history`: retorna o histórico de chamadas ao endpoint de predição
  - `GET /health`: endpoint simples para verificar se a API está online

## Como executar com Docker

1. Certifique-se de que o Docker está instalado.
2. Na raiz do projeto, execute:

```bash
docker build -t titanic-api .
docker run -p 8000:8000 titanic-api
```

A API estará disponível em: http://localhost:8000

## Como rodar os testes

Com o ambiente Python ativado (fora do container), rode:

```bash
pytest tests/
```

O teste principal compara as predições da API com predições pré-calculadas, garantindo consistência do modelo em produção.

## Tecnologias utilizadas

- Python 3.11
- FastAPI
- scikit-learn
- pandas
- joblib
- MLflow (para tracking local dos experimentos)
- Docker

## Estrutura do Projeto

```
.
├── notebooks/           # EDA, treino do modelo e geração de arquivos .pkl
│   └── pickle_files/    # Modelos e pré-processadores salvos
├── src/                 # Código da API
├── tests/               # Testes automatizados
├── Dockerfile
├── requirements_api.txt
└── README.md
```

## Exemplo de payload para predição

```json
{
  "pclass": 2,
  "name": "John Doe",
  "sex": "male",
  "age": 29,
  "sibsp": 0,
  "parch": 0,
  "ticket": "PC 17599",
  "fare": 30.0,
  "cabin": "",
  "embarked": "S",
  "passengerid": 123
}
```
