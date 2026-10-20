# Papéis, sons e tom

Cada camada da intro tem um papel. A escolha do som segue três perguntas, nesta ordem: ele cumpre o papel, cabe no tom da música e, se houver referência, parece com a camada dela no perfil de frequências.

## Os papéis

| Papel | Som | Função | Cuidado |
|---|---|---|---|
| Golpe tonal ("ping") | nota de piano ou de sino na tônica, cauda longa | abre a intro no 1º quadro e marca acentos | só no médio (150 Hz a 2,2 kHz); com sub, embola com os acordes |
| Drone | som grave e contínuo, quase sem ataque | cama que segura a intro até o drop | passa-altas em ~90 Hz; dois drones somados dão corpo |
| Textura | pad ou ar com movimento lento | dá vida ao drone | mais baixa que o drone (−2 dB) |
| Melodia de cello | frases curtas, com começo e fim claros | "pergunta" antes da voz e "resposta" no respiro | escolha cello de verdade (Sol2 a Sol3); frase de violino no lugar soa aguda demais |
| Progressão de acordes | piano tocando um acorde por vez, com sustentação | marca as palavras fortes e a harmonia | precisa de baixo; fatie um acorde por compasso |
| Riser de ar | ruído ou respiração subindo | primeiro arco até o drop | passa-baixas em ~5 kHz |
| Riser agressivo | sintetizador tonal crescente | segundo arco, mais curto e mais forte | passa-baixas em ~4 kHz |
| Impacto | golpe grave com cauda | soma ao bumbo do drop | passa-altas em 60 Hz para não brigar com o bumbo |

Sons tonais costumam vir gravados nos 12 tons. Ao montar a pasta, nomeie cada arquivo com a nota (`drone-1-A.wav`, `cello-C.wav`): no plano, `{tom}` e `{nota}` escolhem o arquivo certo.

## A regra do tom

Tudo o que entra precisa caber nas notas da música.

- Uma tonalidade menor e a maior que fica 3 semitons acima usam as mesmas sete notas: Lá menor e Dó maior, Mi menor e Sol maior, Ré menor e Fá maior. A maior é o **relativo maior** da menor.
- Numa música menor, servem: sons menores no tom; sons maiores no relativo maior; sons que funcionam nos dois modos (marcados como maior/menor, ou sem terça). Em Lá menor, o exemplo usou cello e acordes em Dó maior.
- Numa música maior, o inverso: sons maiores no tom, menores no relativo menor (3 semitons abaixo) e sons dos dois modos.
- Nunca ponha um som maior na mesma tônica de uma música menor (Lá maior sobre Lá menor), nem o contrário. As terças brigam e tudo desafina.
- Notação: Lá♭ = G#, Mi♭ = D#, Si♭ = A#, Ré♭ = C#, Sol♭ = F#.

## Antes de escolher: a afinação

Meça com `medir_musica.py`. Se a música estiver mais de ~20 cents fora do Lá 440, todo som tonal vai soar desafinado por cima dela. Há músicas conhecidas assim (uma delas mede cerca de +45 cents, e as fontes de tom divergem entre dois tons vizinhos). Prefira outra música, ou corrija o tom dos sons antes (`rubberband` no ffmpeg).

## Escolher por medida

Com uma referência:

1. Ache o trecho em que a camada toca quase sozinha (o ping no começo, o drone antes da voz, os risers antes do drop).
2. Rode `medicao/match.py referencia.wav ini fim "sons/**/*.wav"`: ele ranqueia os arquivos pelo perfil de frequências desse trecho.
3. Ouça os três primeiros no lugar, dentro do plano, e fique com o que soa certo junto da voz.
4. Depois, compare o balanço por faixa de cada trecho (`medicao/bands.py`). Se um trecho tem grave a mais, filtre o som que mora ali; não troque todos.

Sem referência, escolha pelo papel e pelo tom, e confira no espectrograma se o ping está no médio, se os acordes têm baixo e se os risers chegam ao drop.

## Fatiar a progressão de acordes

1. `medicao/chords.py sons/acordes-C.wav` mostra onde começa cada acorde do arquivo (no exemplo: Fá 0 s, Sol 8 s, Lám 16 s, Dó 24 s, Rém 32 s, Dó 40 s).
2. `medicao/chromat.py musica.wav ini dur` mostra a harmonia da música segundo a segundo, no trecho da intro.
3. Para cada compasso com palavra forte, pegue no arquivo o acorde que a música toca ali (`"corte"` = início do acorde no arquivo) e ponha no 1º tempo do compasso (`"em"`). O tempo exato sai dos saltos de grave da música em `medicao/env.py` com passo de 5 ms.
4. Cada fatia termina 0,06 s depois do começo da seguinte, com fade de 0,15 s; a última corta no drop.

Quando a harmonia da música troca de acorde a cada compasso e não há arquivo de progressão que siga, use por baixo da voz o instrumento harmônico da própria música (o "(other)" da separação), na mesma velocidade da voz. Uma cama fixa desafina sobre troca de acordes.

## O ping a partir de notas de piano

`prep_ping.py saida.wav nota_media.wav nota_aguda.wav [nota_grave.wav]`: a tônica em duas oitavas (ganhos 1,0 e 0,6) e a de baixo bem de leve (0,2), catedral de 8 s com mix de 55%, filtros de 150 Hz e 2,2 kHz. Qualquer piano sampleado em WAV ou FLAC serve. Para Lá menor, Lá4 + Lá5 + Lá3.
