# ASFETEC

## Especificações de sistema
-------------

#### Contratos
Vínculos com operadoras de serviço que a Associação disponibiliza aos Associados.

#### Associado
Pessoa cadastrada no sistema que possui uma ou mais contratações

#### Contratação
Relacionamento entre o associado e os contratos disponíveis. Pode estar ativa ou não e possui um valor base que é utilizado no momento da criação das mensalidades.

#### Competência
Período de vigência aberto para recebimento de contas do mês. O fechamento de uma competência corresponde à abertura da próxima momento no qual:

- novas mensalidades são geradas à partir da lista de contratações ativas dos associados;
- saldos existentes nos pagamentos da competência anterior são transportados para a mensalidade sendo criada;
- multas são aplicadas às mensalidades já vencidas.

#### Mensalidade
Para cada competência aberta as contratações ativas de cada associado são coletadas e agrupadas para cobrança.

#### Valor da mensalidade
Soma do valor das alíneas (contratações)

#### Total da mensalidade
Valor das mensalidades acrescido de:

- Saldo (obtido na abertura de competência)
- Multa (aplicada na abertura de competência)
- Juros (calculado por demanda)

#### Percentual de multa
Valor percentual a ser aplicado sobre o **valor da mensalidade** que não foi paga até a data de vencimento. Será aplicada quando nova competência for aberta e a mensalidade estiver vencida.

#### Percentual de juros
Valor percentual a ser aplicado **mensalmente** ao **valor da mensalidade** que não foi paga até a data presente. Será aplicado à toda mensalidade enquanto esta estiver em aberto.

## Entidades do sistema
-------------
#### Competência

- Ano
- Mês
- Data base de vencimento (padrão: 25)

#### Contrato

- Nome

#### Associado

- Nome
- Matrícula
- Telefone

#### Contratação

- **Associado**
- **Contrato**
- Descrição
- Valor
- Ativo?
- Histórico

#### Mensalidade

- **Associado**
- **Competência**
- Data de vencimento
- Saldo anterior
- Multa
- Juros (calculado)
- Data do Pagamento
- Valor do Pagamento

#### Alínea

- **Mensalidade**
- **Contratação**
- Valor

#### Rúbrica

- Nome
- Crédito/Débito

#### Caixa

- Data
- **Rúbrica**
- Histórico
- Valor
# Technical specifications
<details><summary>View specs</summary>

### Environment Variables
```bash
PROJECT_NAME="asfetec"
PROJECTS_PATH="/home/user/Projects"
APP_NAME="app"
```

### Environment Installation
------------------------
```bash
sudo apt-get update
sudo apt install software-properties-common
sudo apt-get install python3 pip git
pip install pip-upgrader pylint pylint-flask pylint-flask-sqlalchemy
cd $PROJECTS_PATH
git clone https://gitlab.com/Kdio/$PROJECT_NAME.git
cd $PROJECT_NAME
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running app
-----------
```bash
cd $PROJECTS_PATH/$PROJECT_NAME
source venv/bin/activate
python manage.py runserver 0:8000
```

### Initializing Django
-----------
```bash
cd $PROJECTS_PATH
django-admin startproject $PROJECT_NAME
cd $PROJECTS_PATH/$PROJECT_NAME
python manage.py startapp $APP_NAME
python manage.py makemigrations $APP_NAME
python manage.py sqlmigrate $APP_NAME 0001
python manage.py migrate
python manage.py createsuperuser
```

### requirements.txt
-----------
```bash
# Generate
pip freeze > requirements.txt
# Upgrade
pip-upgrade
```

### Cleanup python cache
```bash
cd $PROJECTS_PATH/$PROJECT_NAME
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

### Dumping sqllite3 database
```bash
cd $PROJECTS_PATH/$PROJECT_NAME/databases
# Save schema
sqlite3 app.db .schema > schema.sql
# Save schema + data
sqlite3 app.db .dump > dump.sql
# Save data only
grep -vx -f schema.sql dump.sql > seed.sql
# Restore schema
sqlite3 app.db < schema.sql
# Restore data
sqlite3 app.db < seed.sql
```

### HOW TO DOCKER
-------------
```bash
cd $PROJECTS_PATH/$PROJECT_NAME
# Build app
sudo docker build --tag app_name .
# Run app
sudo docker run -d -p 5000:5000 app_name
# List running images
sudo docker ps
# Stopping app
sudo docker stop <CONTAINER ID>
# Copying image to another host
docker save --output app_name-latest.tar app_name:latest
docker load --input app_name-latest.tar
# Cleaning up
sudo docker images
sudo docker system prune
```

#### Run GitLab Docker image
```bash
sudo docker login registry.gitlab.com
sudo docker run registry.gitlab.com/kdio/asfetec:latest
```

### Reset passwords
----------------
```python
from django.contrib.auth.models import User
users = User.objects.all()
user = users[1]
user.set_password('gustavo')
user.save()
```


!!!!!!!!!!!!!!! TILL HERE !!!!!!!!!!!!!!!!!!!


### Initial seed (ASFETEC)
```python
import datetime
from werkzeug.security import generate_password_hash
from app import db
from app.usuario.model import Usuario
kdio = Usuario(nome='kdio', password=generate_password_hash('kdio'), admin=True)
db.session.add(kdio)
gustavo = Usuario(nome='gustavo', password=generate_password_hash('gustavo'), admin=True)
db.session.add(gustavo)
luana = Usuario(nome='luana', password=generate_password_hash('luana'), admin=False)
db.session.add(luana)

from app.competencia.model import Competencia
competencia = Competencia(ano='2021', mes='01', data=datetime.datetime(2021, 1, 25))
db.session.add(competencia)

db.session.commit()
```

### QUALITY ASSURANCE
-------------

#### Pylint
```bash
pylint --rcfile=.pylintrc *.py > pylint.txt
```

#### Pytest
```bash
python -m pytest -v --cov=app --cov-report term-missing > tests/pytest-result.txt
```

</details>
