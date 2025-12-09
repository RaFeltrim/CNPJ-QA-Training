# Scripts de CI/CD

Este diretório contém scripts auxiliares para integração contínua.

## Estrutura

- `run_tests.sh` - Script para executar todos os testes localmente (Linux/Mac)
- `run_tests.bat` - Script para executar todos os testes localmente (Windows)
- `pre_commit.py` - Hook de pré-commit para validações locais
- `sync_to_zephyr.py` - Script para sincronizar resultados com Zephyr Scale

## Uso

### Linux/Mac
```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

### Windows
```cmd
scripts\run_tests.bat
```
