# Cinematic Soundtrack Skill · Trilha Cinematográfica

> A bilingual Claude Code skill for building measured, in-key cinematic song intros with Python and FFmpeg.
>
> Uma skill bilíngue para Claude Code que cria intros cinematográficas medidas, no tom da música, com Python e FFmpeg.

## Credits · Créditos

Original skill and concept by [@iamjeff.ia](https://www.instagram.com/iamjeff.ia/).

Skill e conceito originais de [@iamjeff.ia](https://www.instagram.com/iamjeff.ia/).

See `CREDITS.md` for the attribution record.

## English

This repository turns a real song into a reproducible cinematic intro. It measures the song, separates the vocal, places tonal layers by musical role, protects vocal intelligibility, aligns the transition to the drop kick, and validates the result against loudness and spectral targets.

### Install

```bash
git clone <YOUR-REPOSITORY-URL>
cd trilha-cinematografica-skill
mkdir -p ~/.claude/skills/trilha-cinematografica
cp SKILL.md requirements.txt ~/.claude/skills/trilha-cinematografica/
cp -R scripts references examples ~/.claude/skills/trilha-cinematografica/
```

The default `SKILL.md` is in English.

English references are in `references/en/`, and the English example plan is `examples/example-plan.json`.

---

## Português

Este repositório transforma uma música real em uma intro cinematográfica reproduzível. Ele mede a música, separa a voz, posiciona camadas tonais por função musical, protege a inteligibilidade da voz, alinha a transição ao bumbo do drop e valida o resultado por loudness e espectro.

### Instalar

```bash
git clone <URL-DO-SEU-REPOSITORIO>
cd trilha-cinematografica-skill
mkdir -p ~/.claude/skills/trilha-cinematografica
cp SKILL.pt-BR.md ~/.claude/skills/trilha-cinematografica/SKILL.md
cp requirements.txt ~/.claude/skills/trilha-cinematografica/
cp -R scripts references examples ~/.claude/skills/trilha-cinematografica/
```

O primeiro comando `cp` ativa a versão em português.

As referências em português estão em `references/pt-BR/`, e o plano de exemplo é `examples/plano-exemplo.pt-BR.json`.

## Estrutura

```text
.
├── SKILL.md                    # English skill, default
├── SKILL.pt-BR.md              # Skill em português
├── README.md                   # Apresentação e instalação bilíngue
├── CREDITS.md                  # Crédito ao autor original
├── requirements.txt            # Dependências Python
├── references/
│   ├── en/                     # English technical references
│   └── pt-BR/                  # Referências técnicas em português
├── examples/
│   ├── example-plan.json
│   └── plano-exemplo.pt-BR.json
└── scripts/                    # Análise, preparação, mixagem e validação
```

## Requirements · Requisitos

- Python 3.10+ for the included scripts.
- Python 3.11 in a separate environment for `audio-separator`.
- FFmpeg available on `PATH`.
- Packages from `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ffmpeg -version
```

## Content notice · Aviso de conteúdo

No copyrighted song, acapella, or commercial sound-library asset is included. Use files you own or are licensed to use.

Nenhuma música, acapella ou biblioteca comercial protegida está incluída. Use arquivos próprios ou licenciados para o uso pretendido.
