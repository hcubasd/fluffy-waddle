# yaml
npm i -g yaml-language-server @ansible/ansible-language-server

# docker-compose
npm i -g @microsoft/compose-language-service

# toml
curl -fsSL https://github.com/tamasfe/taplo/releases/latest/download/taplo-linux-x86_64.gz \
  | gzip -d - | install -m 755 /dev/stdin /usr/local/bin/taplo
curl -fsSL https://tombi-toml.github.io/tombi/install.sh | sh

export PATH="$PATH:/root/.local/bin"

# python
python -m pip install -U pip ty ruff jedi-language-server python-lsp-server
