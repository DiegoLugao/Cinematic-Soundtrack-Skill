---
name: trilha-cinematografica
author: "@iamjeff.ia"
source: "https://www.instagram.com/iamjeff.ia/"
description: "Faz a versão cinematográfica de uma música real pelo Claude Code: mede tom, BPM, afinação e o bumbo do drop, separa a voz da própria música (MelBand RoFormer Big Beta 4 pelo audio-separator), põe em volta efeitos tonais no tom (golpe, drones, cello em pergunta e resposta, acordes de piano fatiados nas palavras fortes, dois risers com pico no drop), dá à voz um reverb de sala de concerto (~40%), mantém a voz por cima dos tonais e mixa em −14 LUFS por scripts em Python e ffmpeg. Use quando pedirem trilha cinematográfica, remix estilo trailer, intro de cinema com uma música, 'deixa essa música mais cinematográfica', efeitos tonais no tom da música, build-up até o drop ou uma comparação 'som normal × som cinematográfico'."
---

# Trilha cinematográfica com uma música real

A intro abre com a voz do cantor quase sozinha, com eco de sala de concerto. Em volta, efeitos tonais no tom da música complementam a voz sem disputar com ela. Tudo cresce até o drop, onde a intro corta seca e a música inteira entra no bumbo. Nada é tocado à mão: você mede a música, escreve um plano em JSON e os scripts de `scripts/` montam a mixagem com o ffmpeg. O exemplo aprovado é a intro de "Laugh Now Cry Later", com o plano em `examples/plano-exemplo.pt-BR.json`.

## Antes de começar

1. **Combine o "pronto".** Uso (Reel, abertura de vídeo longo, filme), duração da intro, se haverá narração depois do drop e o que entregar (WAV final, camadas separadas, versão "som normal" para comparar).
2. **Ferramentas.** `ffmpeg` no PATH; Python com `numpy scipy soundfile librosa pyloudnorm pedalboard matplotlib`; `audio-separator` num ambiente Python 3.11 próprio (no 3.14 uma dependência não compila). Confira com `ffmpeg -version` e rode um script sem argumentos para ver o uso.
3. **Sons.** Pergunte onde estão os sons da pessoa e liste o que existe para cada papel (tabela abaixo) no tom da música. Sons tonais costumam vir nos 12 tons; use o arquivo do tom certo. Se faltar um papel, diga qual e proponha o equivalente mais próximo.

## O processo

1. **Música e momento.** Uma frase de voz forte antes de uma entrada de batida. Em vídeo curto: ~13 s antes da voz e drop por volta dos 22 s. O exemplo tem a voz aos 9,9 s e o drop aos 39,37 s.
2. **Medir.** `scripts/medir_musica.py musica.wav --bumbo INI FIM` → tom, relativo, BPM, compasso, afinação e o segundo do bumbo. Tom automático erra (sobretudo entre tom e relativo): confirme no Hooktheory, no tunebat ou pelas notas da melodia (`medicao/notes.py`). Afinação acima de ±20 cents desafina qualquer tonal. BPM do Google também erra (exemplo: 134 no Google, 136 medido).
3. **Separar a voz da própria música.** `scripts/separar_voz.py musica.wav prep/voz.wav --dur 50`. Nunca use acapella baixada da internet: no teste cego, Big Beta 4 teve 8,5 e a acapella do YouTube, 4 ("oca, subaquática").
4. **Escolher os sons por papel e por tom** (`references/pt-BR/papeis-sons-e-tom.md`). Com uma referência, ranqueie os candidatos com `medicao/match.py` e decida no ouvido entre os três primeiros.
5. **Tempos.** Palavras e respiros com `medicao/tr.py`; harmonia com `medicao/chromat.py`; início exato de cada acorde pelos saltos de grave (`medicao/env.py` com passo de 5 a 10 ms). Monte a tabela de camadas (tempo, camada, papel, nível) e mostre antes de mixar.
6. **Plano.** Copie `examples/plano-exemplo.pt-BR.json` e troque tempos e arquivos. Campos em `references/pt-BR/receita-aprovada-v11.md` e no topo de `scripts/trilha_momentos.py`. Rascunho: `trilha_momentos.py plano.json saida/rascunho.wav`.
7. **Voz.** `prep_voz.py voz.wav prep/voz-reverb.wav --ini --fim` (Concert Hall de 4 s, mix 0,407).
8. **Mixagem com a voz na frente.** `stems.py plano.json saida/stems` e depois `mix_voz_na_frente.py saida/stems saida/final.wav saida/camadas`. Sai em −14 LUFS, pico abaixo de −1 dBFS.
9. **Conferir** (`references/pt-BR/medicao-e-validacao.md`). `conferir.py` com espectrograma contra a referência e vídeo A/B para ouvir; `medicao/bands.py` para o balanço por faixa. Meça antes de culpar um efeito.
10. **Entregar.** WAV final, camadas, o plano usado e uma linha com música, tom, BPM e o que foi trocado em relação ao exemplo.

## Papéis das camadas

| Papel | Onde entra | Nível antes do master (exemplo) |
|---|---|---|
| Golpe tonal (ping de piano na tônica, só médio) | 1º quadro; acento no 1º e no último acorde; drop | −21 / −25 / −26 / −21 LUFS |
| Dois drones ou texturas no tom | 2,5 s até o drop, fade-in de 4–4,5 s | −26 e −28 |
| Cello no relativo maior | pergunta sozinho antes da voz; resposta no respiro | −22 e −26 |
| Voz do cantor com reverb | da 1ª frase até o drop | −16 |
| Acordes de piano no relativo maior, fatiados | 1º tempo de cada compasso, numa palavra forte, seguindo a harmonia | −17 |
| Dois risers | começam ~5,1 e ~3,7 s antes; pico exato no drop | −16 e −17,5 |
| Impacto tonal sem sub (passa-altas 60 Hz) | no drop | −20 |
| Música inteira | seca, no bumbo do drop | −11,5 |

## Regras que não mudam

- **A voz é a prioridade; os tonais complementam.** Enquanto ela canta, o médio dos tonais (≥ 250 Hz) fica ≥ 5 dB abaixo da voz (até −7 dB) e o grave desce no máximo 2 dB. Um desvio fixo não basta.
- **Reverb da voz cantada:** Concert Hall, 4 s, predelay 20 ms, mix ~40%, eco ~5 dB abaixo da voz. 50% com catedral = eco demais; 10–20% = "a capela demais". Narração por cima do vídeo fica seca.
- **Tom:** tudo cabe nas notas da música. Música menor aceita sons menores no tom, maiores no relativo maior e sons que servem aos dois modos. Nunca maior na mesma tônica de uma música menor, nem o contrário.
- **Cello só nos respiros.** Nunca por cima de uma frase cantada.
- **Acordes no compasso.** Cada fatia no 1º tempo, junto de uma palavra, com o acorde que a música toca ali. Fatia termina com fade de 0,15 s, a última corta no drop.
- **Drop seco.** Tudo da intro corta no bumbo (fade de 20–60 ms), sem respiro antes; a força vem do contraste entre a subida e a entrada (no exemplo, 5,1 dB).
- **Ping no médio.** Passa-altas 150 Hz e passa-baixas 2,2 kHz: com sub, ele embola com os acordes.
- **Medir a referência, não estimar.** Tempos, tom, BPM e níveis vêm de medida; o drop da mesma música é a régua de calibração.
- **Menos é mais.** Cada camada nova precisa ter função; na dúvida, tire.

## Armadilhas

- O caminho de `"arquivo"` no plano parte da pasta do JSON; `{tom}` e `{nota}` são trocados pelo `"tom"` do plano e pela `"nota"` da camada.
- Riser com `"pico_em"`: o script acha o pico do arquivo (maior RMS em 50 ms). Se o arquivo tiver o clímax antes do fim, informe `"sync_s"`.
- Camada mais curta que o trecho acaba antes da hora: troque o som ou divida a camada (`"a_partir_de"`).
- O `trilha_momentos.py` sozinho não protege a voz. A entrega final passa pelo `mix_voz_na_frente.py`.
- Detector de tom, BPM do Google e nome de instrumento dado pelo Gemini erram. Ouvido e medida decidem.

## Referências desta skill

| Arquivo | Quando abrir |
|---|---|
| `references/pt-BR/receita-aprovada-v11.md` | a receita aprovada com todos os números, os campos do plano e as 11 versões |
| `references/pt-BR/papeis-sons-e-tom.md` | escolher cada som, regra do relativo, afinação, como fatiar a progressão |
| `references/pt-BR/medicao-e-validacao.md` | medir uma referência, espectrograma, balanço por faixa, A/B com o Gemini |
| `references/pt-BR/variacoes-de-intro.md` | outros formatos de intro, emenda entre partes, velocidade, pulso fixo |
| `scripts/` | scripts incluídos de análise, preparação, renderização, stems e validação |

## Onde instalar

Copie esta pasta para `~/.claude/skills/trilha-cinematografica/` (todos os projetos) ou `.claude/skills/trilha-cinematografica/` (só um projeto). Para chamar direto, peça "use a skill trilha-cinematografica".
