# FFMPYMEDIA

FFMPYMEDIA é um biblioteca que empacota o FFMPEG.
Ela interage com o ffmpeg através de chamadas de shell e interpreta os fluxos de saída para gerar as suas esttruturas internas.
No momento, somente o utilitário ffprobe está empacotado e só está provida a seguinte funcionalidade:

## Análise de Mídia

A saída do ffprobe é interpretada e a partir dela são geradas os objetos que abstraem os arquivos e os fluxos.
A classe MediaAnalyser expões as seguintes funções:
**MediaAnalyser.media_file_difference()** que retorna a diferença entre um arquivo de mídia e um Modelo.
**MediaAnalyser.validate_media_file()** que determina se um arquivo de mídia tem o mesmo layout que MediaTemplate ou outro arquivo de mídia.

## Funcionalidades Planejadas

Estão planejadas interfaces de alto nível para os utilitários ffmpeg e ffserver, a fim de gerar pipelines de transcodificação bem como de agragação e disponibilização de fluxos de mídia.