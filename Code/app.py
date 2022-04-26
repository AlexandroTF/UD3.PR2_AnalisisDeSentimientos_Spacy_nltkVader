from flask import Flask, render_template, request
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pysentimiento import create_analyzer
analyzer = create_analyzer(task="sentiment", lang="es")

app = Flask(__name__)

def get_lang_detector(nlp, name):
    return LanguageDetector()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)


@app.route("/process", methods = ['POST', ])
def detectorspacy():
    if request.method == 'POST':
        texto = request.form.get("rawtext")
        opcion = request.form.get("taskoption")
        results=[]

        # Carga el modelo "es_core_news_sm"
        nlp = spacy.load("es_core_news_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp.add_pipe('language_detector', last=True)

        # Procesa el texto
        doc = nlp(texto)

        if doc._.language['language'] == 'es':
            sentimiento = analyzer.predict(texto)
            if sentimiento.output == "NEU":
                resultadoSentimiento = "Mayoritariamente neutral"
            elif sentimiento.output == "POS":
                resultadoSentimiento = "Mayoritariamente positivo"
            else:
                resultadoSentimiento = "Mayoritariamente negativo"
            
                ##return render_template("index.html", sentim=resultadoSentimiento, results=['tests'], num_of_results=len(results))

            pass
        elif doc._.language['language'] == 'en':
            #cargamos el otro
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(texto)
            sid = SentimentIntensityAnalyzer()
            resultados = sid.polarity_scores(texto)
            sentimiento = resultados["compound"]
            # Aqui manejariamos el resultado y lo mostrariamos

            if sentimiento > 0:
                # Sentimiento entre neutral y positivo
                distanciaNeut = sentimiento
                distanciaPos = 1 - sentimiento
                if distanciaNeut > distanciaPos:
                    resultadoSentimiento = "Mayoritariamente positivo"
                elif distanciaNeut < distanciaPos:
                    resultadoSentimiento = "Mayoritariamente neutral"
                else:
                    resultadoSentimiento = "Entre neutral y positivo"
            elif sentimiento <= 0:
                # Sentimiento entre negativo y neutral
                distanciaNeut = 0 - sentimiento
                distanciaNeg = 1 + sentimiento
                if distanciaNeut > distanciaNeg:
                    resultadoSentimiento = "Mayoritariamente negativo"
                elif distanciaNeut < distanciaNeut:
                    resultadoSentimiento = "Mayoritariamente neutral"
                else:
                    resultadoSentimiento = "Entre negativo y neutral"
        else:
            return render_template("index.html", sentim="Error", results=["Lo sentimos pero esta pagina no tiene soporte para idiomas distintos al español e inglés"], num_of_results=" Error")


        


        #reduce la opcion
        if opcion=="person":
            opc = "PER"
        elif opcion=="organization":
            opc = "ORG"
        else:
            opc = "none"
        
        #seleccionador
        if opc != "none":
            # Imprime en pantalla el texto del documento
            for ent in doc.ents:
                # Imprime en pantalla el texto de la entidad y su etiqueta
                if ent.label_ == opc:
                    # print(ent.text, ent.label_)
                    results.append(ent.text)
                    print(ent.text)

    # return render_template("results.html", text="hola")
    return render_template("index.html", sentim=resultadoSentimiento, results=results, num_of_results=len(results))

# # Carga el modelo "es_core_news_sm"
# nlp = spacy.load("es_core_news_sm")

# text = (
#     "De acuerdo con la revista Fortune, Apple fue la empresa "
#     "más admirada en el mundo entre 2008 y 2012."
# )

# # Procesa el texto
# doc = nlp(text)

# # Imprime en pantalla el texto del documento
# print(doc.text)