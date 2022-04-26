# UD3.PR2_AnalisisDeSentimientos_Spacy_nltkVader
Analisis de sentimientos de un texto en ingles mediante nltk vader y en español mediante pysentimiento

Posibles problemas a la hora de ejecutar el codigo
- "vader_lexicon.txt" not found
  - Para solucionar este problema, hay que descargar el archivo entrando en el entorno virtual y ejecutando las siguientes lineas\
`Python
import nltk
nltk.downloader.download('vader_lexicon')`\
Para soluciones alternativas consultar [stack overflow](https://stackoverflow.com/questions/43546593/error-message-with-nltk-sentiment-vader-in-python)
- "es_core_news_sm" o "en_core_web_sm" no enconctrados
  - Segun el paquete que falte ejecutar el comando correspondiente\
    `python -m spacy download es_core_news_sm`\
    `python -m spacy download en_core_web_sm`
