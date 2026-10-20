# Medir a referência e conferir cada versão

Os tempos, o tom, o BPM e os níveis vêm de medida. Quando existe uma referência (um remix ou uma demo de que a pessoa gosta), ela é a régua: o drop é a mesma música nas duas e serve de calibração.

## Medir a referência

1. **Separe a voz da referência** (`separar_voz.py`; use o arquivo "(other)") para ter só os tonais. A sua versão também é comparada sem voz.
2. **Alinhe com a música** (`medicao/align.py referencia.wav musica.wav ini fim`): mostra, a cada segundo, que ponto da música a referência usa. Um deslocamento fixo do começo ao fim quer dizer que a voz entra inteira, sem cortes (no exemplo, 14,83 s).
3. **Ponto zero no 1º golpe** (`medicao/env.py referencia.wav ini fim 0.005`): o instante em que a energia salta. No exemplo, o ping sai de −60 para −17 dB em 5,950 s da referência. A partir dali, todos os tempos da sua intro se contam.
4. **Acordes:** harmonia com `medicao/chromat.py`; o tempo exato de cada acorde sai dos saltos de energia abaixo de 80 Hz. No exemplo, todos caem no 1º tempo do compasso, junto das palavras.
5. **Drop:** o bumbo da música em RMS de 10 ms (`medir_musica.py --bumbo`).
6. **Música:** tom no croma (e confirmação externa), BPM por beat tracking, afinação em cents.

## Conferir cada versão

### Espectrograma

`conferir.py sua.wav --ref referencia.wav --desloc-ref <s> --png espectro.png` põe as duas no mesmo eixo de tempo. Procure:

- ping com sub (faixa abaixo de 100 Hz acesa no 1º quadro);
- acordes sem baixo (a referência tem energia abaixo de 70 Hz, a sua não);
- risers que não chegam ao drop ou que passam dele;
- drones que entram tarde ou cedo demais.

### Balanço por faixa

`medicao/bands.py ref_sem_voz.wav sua_sem_voz.wav --trechos trechos.json` mede 20–70, 70–250, 250–2 k, 2–8 k e 8–16 kHz em cada trecho, normalizado pelo drop. O drop tem de bater em até ~1 dB. Diferença em um trecho aponta qual camada filtrar.

### Ouvido

- Quem decide é o ouvido da pessoa. Peça o segundo exato do que incomoda.
- Para uma segunda opinião, `conferir.py --video ab.mp4` gera um MP4 de tela preta: referência, 2 s de silêncio, a sua versão. Mande ao Gemini com a pergunta: "Compare as duas trilhas. Dê uma nota de 0 a 10 de semelhança, liste os problemas da segunda com o tempo de cada um (contado do começo dela) e diga o que corrigir, em números."
- Para escolher entre separações de voz, faça teste cego: mesma frase, ordem embaralhada, sem dizer qual é qual.
- O Gemini erra nome de instrumento. Acerta estrutura, nível, eco e artefato.

### Medir antes de culpar

Quando algo soa errado, meça antes de mexer. No exemplo, "a voz some aos 17 s" parecia o limitador. A medida mostrou que o limitador não agia (0,0 dB de redução) e que o acorde de Lá menor mais o ping estavam 2 a 5 dB acima da voz. A correção veio da prioridade dinâmica da voz, e o limitador ficou como estava.

## Números de entrega

| Item | Alvo |
|---|---|
| Loudness integrado | −14 LUFS |
| Pico | abaixo de −1 dBFS |
| Eco da voz | ~5 dB abaixo da voz seca |
| Médio dos tonais enquanto a voz canta | ≥ 5 dB abaixo da voz |
| Contraste subida → drop | ~4 a 5 dB (exemplo: 5,1; referência: 4,3) |
| Drop contra a referência, no balanço por faixa | até ~1 dB |
