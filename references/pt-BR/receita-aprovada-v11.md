# Receita aprovada (v11): "Laugh Now Cry Later"

A intro tem ~39 s. O cantor entra quase a capela, com o reverb de sala de concerto, e os tonais ficam em volta como complemento. A música inteira entra seca no bumbo do verso e segue ~18 s (58 s no total). No ouvido do Gemini, comparada com a referência, a v11 teve 9,7 de 10. O plano completo está em `examples/plano-exemplo.pt-BR.json`.

## A música

- Lá menor, **136 BPM** (o Google mostra 134), afinação +0,02 semitom (padrão).
- Bumbo do drop: 30,485 s da música, medido em RMS de 10 ms. Na intro, ele cai em 39,37 s.
- Voz: separada da própria música pelo MelBand RoFormer Big Beta 4, trecho de 1,0 a 31,0 s da música, posto em 9,88 s da intro.

## Linha do tempo e camadas

| Tempo (s) | Camada | Ajustes |
|---|---|---|
| 0,00 | ping de piano em Lá (Lá4 + Lá5, Lá3 de leve), catedral de 8 s com mix de 55% | passa-altas 150 Hz, passa-baixas 2,2 kHz (4ª ordem); −21 LUFS |
| 2,5 → 39,37 | drone 1 em Lá | fade-in 4 s; passa-altas 90 Hz, +1,5 dB em 180 Hz, +2 dB em 280 Hz, passa-baixas 2,5 kHz; −26 |
| 2,5 → 39,37 | drone 2 (textura) em Lá | fade-in 4,5 s; passa-altas 90 Hz, +1,5 dB em 180 Hz, +2,5 dB em 280 Hz; −28 |
| 4,2–10,6 | cello em Dó maior (relativo), frase Lá→Mi, a "pergunta" | fade-in 0,8 s, fade-out 1 s; passa-baixas 3,2 kHz; −22 |
| 9,88 → 39,37 | voz com reverb | −16 |
| 13,4–18,0 | cello, frase em Mi, a "resposta" | fade-in 0,6 s, fade-out 1,5 s; passa-baixas 3,2 kHz; −26 |
| 16,09 / 21,50 / 25,00 / 28,70 / 32,23 / 35,85 | acordes fatiados Lám, Sol, Fá, Sol, Lám, Sol (progressão em Dó maior: Fá Sol Lám Dó Rém Dó, 8 s cada) | +5 dB em 70 Hz, passa-baixas 2,5 kHz; fade-out 0,15 s; −17 |
| 16,09 e 35,85 | ping de acento | −25 e −26 (o segundo corta no drop) |
| 34,25 → 39,37 | riser 2, mais agressivo | pico no drop; passa-baixas 4 kHz; fade de 60 ms no fim; −16 |
| 35,69 → 39,37 | riser 1, ar subindo | pico no drop; passa-baixas 5 kHz; fade de 60 ms; −17,5 |
| 39,37 | drop: música a partir de 30,42 s (bumbo em 30,485) + ping + impacto tonal | música −11,5; ping −21; impacto com passa-altas 60 Hz, −20; tudo da intro corta seco |

Sem filtro, o riser agressivo ficava 10 dB mais claro que o da referência. A progressão foi escolhida por ter baixo: a referência mede +6 dB abaixo de 70 Hz nos acordes.

## Reverb da voz (réplica de um Concert Hall, sem plugin)

| Parâmetro do preset | Réplica no `prep_voz.py` |
|---|---|
| Concert Hall, cor anos 70 | ataque lento (envelope de 60 ms), cauda escura |
| Decay 4,00 s | RT60 de 4 s no médio (700 Hz a 6 kHz) |
| BassFreq 700 Hz × 1,5 | RT60 de 6 s abaixo de 700 Hz |
| Damping 6 kHz / −24 dB | RT60 de 1,2 s acima de 6 kHz, a −9 dB |
| Predelay 20 ms | 20 ms |
| HighCut 8 kHz | 5,5 kHz (com 8 kHz, a cauda soava mais clara que a da referência) |
| Mod 2,53 Hz / 38% | chorus de 2,53 Hz, profundidade 0,15, mix 0,5, só na cauda |
| Mix 40,7% | molhado na mesma energia do seco; saída = 0,593 × seco + 0,407 × molhado |

Mais −1,5 dB em 3,8 kHz (Q 1) na voz seca. Resultado: eco a −4,9 dB da voz.

## Mixagem com a voz por cima

1. `trilha_momentos.py` resolve as camadas, os tempos e os níveis.
2. `stems.py` exporta os grupos com o mesmo ganho de master da mixagem.
3. `mix_voz_na_frente.py`: os tonais viram um bus dividido em 250 Hz. Enquanto a voz canta, o médio do bus fica ≥ 5 dB abaixo da voz (redução de até 7 dB) e o grave desce no máximo 2 dB. Envelopes de 50 ms, ataque de 15 ms, soltura de 300 ms. Volta a −14 LUFS e passa pelo limitador (`alimiter` 0,84).
4. As camadas finais saem desse passo com o atraso de 239 amostras do limitador e somam a mixagem.

Saída: −14,0 LUFS, pico −1,2 dBFS.

## Campos do plano

`arquivo`, `papel` (golpe, drone, melodia, acordes, riser, voz, musica), `grupo`, `em`, `corte` (ou `"metade"`), `ate`, `golpe: true` (pico do arquivo em `em`), `pico_em` + `subida` (riser), `sync_s` (pico do arquivo, se a medida automática errar), `ataque` (segundos entre o corte e o bumbo), `a_partir_de`, `tempo`, `passa_altas`, `filtro` (ffmpeg livre), `lufs_alvo`, `ganho_db`, `fade_in`, `fade_out`, `mudo`. No topo: `duracao`, `saida_lufs`, `tom`. Chaves começadas por `_` são comentários.

## As 11 versões

| Versão | Mudança | Resultado |
|---|---|---|
| v1 | tempos medidos; um golpe com sub no lugar do ping; progressão sem baixo; voz com hall 40% | espectrograma: piano sem baixo, ping com sub demais |
| v2–v3 | ping de piano de verdade; filtros pelo balanço de faixas; progressão com baixo | faixas perto da referência; drop igual |
| v4 | acordes no tempo exato, pelos saltos de grave | 9,2 |
| v5 | reverb 50% + catedral, drones mais encorpados, mergulho nos risers | 9,3 |
| v6 | drop com mais contraste, risers mais abertos | 9,6; "ficou MUITO bom", mas "muito eco na voz" |
| v7 | reverb 20%, só hall | — |
| v8 | reverb 10% + tonais −2,5 dB fixos quando ele canta | "a capela demais" |
| v9 | réplica do Concert Hall, mix 40,7% | voz 9/10 igual à da referência |
| v10 | cauda mais escura, −1,5 dB em 3,8 kHz | melhor, mas a voz "se perde" aos 17 s e a separação é fraca |
| **v11** | voz pelo Big Beta 4 + prioridade dinâmica da voz | **9,7**; "o mais próximo da perfeição até agora" |

## Para refinar

Duas sugestões do Gemini que não foram testadas: abrir o estéreo e saturar de leve o sub no primeiro tempo do drop. Vale testar num editor de áudio, de ouvido.
