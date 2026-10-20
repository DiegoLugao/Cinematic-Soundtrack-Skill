# Variações de intro e regras de continuidade

A receita da v11 (voz desde cedo, cello em pergunta e resposta, acordes fatiados nas palavras, dois risers) é uma entre várias. Cada música pede a sua: a velocidade, abrir pela voz ou pelo instrumental e a escolha das peças dependem do clima, da batida, do tom e do BPM.

## Briefing de trilha (preencha antes de cada música)

| Campo | Exemplo |
|---|---|
| Uso | Reel de 20–30 s, abertura de vídeo longo, filme |
| Emoção e arco | intimista → tensão → explosão; ou melancólico do começo ao fim |
| Música, tom, BPM, afinação | medidos e conferidos |
| Acordes do trecho | `medicao/chromat.py` |
| Receita base | uma das abaixo |
| Paleta | o que entra de novo nesta música e o que fica de fora |
| Velocidade | se desacelera, quanto e onde volta |

## Receitas

**Voz desde cedo (a do exemplo).** Ping no 1º quadro, drones a partir de ~2,5 s, cello sozinho, voz com reverb ~40%, cello responde no respiro, acordes no relativo maior fatiados um por palavra forte, ping de acento no 1º acorde, dois risers nos últimos 5 s, drop seco no bumbo.

**Construir até a voz.** Golpe melódico no 1º quadro, drone desde o 0 com fade-in suave, melodia de violino ou cello a partir de ~4,5 s, um swell tonal com pico na entrada da voz, a voz só nos ~10 s finais, um riser agudo de ~10 s e um grave de ~8 s, ambos terminando no drop, e um impacto tonal com cauda vazando para a música. Para vídeo curto, encurte só a parte instrumental antes da voz (a voz fica em ~9 s, os risers não mudam).

**Abrir pelo instrumento da própria música.** O sintetizador ou piano da faixa (o "(other)" da separação) a 85%, com o tom preservado, junto do ping e de trechos de cello. Ele some numa cauda de reverb (~30%) quando a voz entra, também a 85% e com reverb de ~40%. Piano em blocos nos tempos fortes, com um ping em cada ataque. Nos últimos segundos, um riser agressivo, e a **última frase volta a 100%**. Fim seco da frase, uma fração de silêncio e a música inteira.

**Abrir pelo instrumental abafado.** Os instrumentos da música sem a voz começam com passa-baixas fechado (~400 Hz) e abrem até o fim do primeiro ciclo de acordes. A voz entra no tempo original, depois de alguns compassos. Uma parada da própria música antes do refrão vira o respiro (~1 s), com um riser atravessando sozinho.

**Balada sem drop.** Drone baixando ~11 dB quando o piano entra; um sub-grave sob o pré-refrão, cortado seco no refrão.

## Velocidade

- A frase a 100% precisa **continuar a letra** que vinha a 85%; pular de verso junto com a troca de velocidade denuncia a montagem. Deixe um respiro de ~0,25 s antes dela.
- A velocidade sobe em rampa, sem salto: mude o `tempo` do rubberband a cada 50 ms (`asendcmd`), igual na voz e no instrumento.
- Teste cada voz antes: uma cantora a 85% soou robótica, e a 90%, natural. Voz desacelerada pede o rubberband em modo suave (`transients=smooth:detector=soft:window=long:channels=together`). Vogais longas são o ponto fraco.

## Continuidade

- Ninguém pode perceber uma emenda. Nenhuma camada sai de um jeito que se ouça o volume caindo.
- Uma camada contínua atravessa a intro do começo ao fim (um drone suave, por exemplo).
- O stem que abre não para seco: some numa cauda longa por baixo da entrada da voz. O instrumento que sai antes do drop precisa de fade de ~2,5 s; 0,4 s soa como corte.
- Antes do drop, o arranjo esvazia: piano e pings param, ficam a voz e o riser crescendo (~3 s). O riser atravessa o respiro como o único efeito, com o pico no drop. O respiro tem meio compasso.
- A última palavra pode se dissolver no respiro, com fade de ~1,2 s, em vez de cortar seco.
- Na troca de velocidade, o drone e o riser podem recomeçar com fade-in de 1,5 s: uma pequena puxada para trás que volta a crescer.
- Tudo termina no mesmo ponto, onde a música inteira entra.

## Emenda entre duas partes

1. A parte que sai termina no fim de uma frase. Nos últimos ~0,23 s, o reverb de catedral sobe de 0 a 50%, e a cauda continua soando.
2. Tonais no tom: um efeito vocal com o pico no corte, um piano grave subindo até o corte e, no momento calmo, drone e sub no tom.
3. A parte que entra volta abafada (passa-baixas ~650–700 Hz, passa-altas ~400 Hz), sempre num compasso da grade. Os filtros abrem nos ~4 s finais e chegam ao máximo no 1º tempo do refrão, com riser e ping no mesmo ponto.
4. A voz que entra começa no começo de uma frase, depois de um silêncio natural (ache pelas palavras do `medicao/tr.py`).
5. Os pedaços do mesmo stem levam o mesmo ganho, calculado no som cru.

**Dois arcos de hype.** O efeito da emenda não pode chegar em cima da hora. Um tonal e um riser começam na abertura e crescem até o corte da voz (arco 1); no corte, outro riser recomeça e cresce até a batida (arco 2).

## Pulso fixo

Piano e qualquer toque repetido seguem um pulso fixo do começo ao fim (por exemplo, a cada 2 tempos, na grade do bumbo). Quem ouve aprende o tempo e espera o próximo toque no mesmo intervalo. Para variar, ponha outra nota do mesmo acorde (terça ou quinta, em outra oitava), também no pulso, sem mudar o intervalo.

## Regras gerais

- O hype começa ~10 s antes da batida e só soma camadas até o impacto.
- Riser tonal com glissando choca com riff de guitarra fixo; nesse caso, use riser de ruído.
- Swell que termina seco precisa de cauda de reverb.
- Cada camada nova precisa ter função. Na dúvida, menos.
- Num vídeo narrado, o remix abre o vídeo e a narração começa pelo menos 0,5 s depois do drop, seca, com a música bem abaixo dela. Narração por cima do remix não funciona.
