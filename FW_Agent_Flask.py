import os
from flask import Flask, request, render_template
from flask_cors import CORS
import openai
from openai import AzureOpenAI
import markdown

app = Flask(__name__)
CORS(app)  # Erlaube CORS für alle Domains

# Verwende Umgebungsvariablen anstelle von hartkodierten Werten
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)

system_prompt = """
Übernehme die Rolle eines IT-Auditors (CISA) und eines sehr anerkannten Pen-Testers im Bereich Cybersecurity. 
Führe bei einer IT-Prüfung im Rahmen der Jahresabschlussprüfung nach ISA-315 die folgende Prüfungshandlung durch: 
Es geht um die Prüfung der Firewallregeln eines Mandanten. Kannst du entsprechende Prüfungshandlung im Rahmen 
einer Funktionsprüfung nach Best Practices aus dem Bereich Cybersecurity / Pen-Testing auf Basis der Eingabe durchführen.

Kontext: Als IT-Prüfer (CISA) und Pen-Tester im Rahmen einer Jahresabschlussprüfung bist du in deiner zugewiesenen Rolle dafür verantwortlich, 
die Firewall-Konfiguration des Mandanten auf Sicherheits- und Konformitätsaspekte zu überprüfen. Verwenden hierzu 
diesen Prompt, um eine systematische und umfassende Analyse der Firewall-Regeln durchzuführen.

Zweck: Durchführung einer umfassenden Prüfung der Firewall-Regeln eines Mandanten gemäß den allgmeinen Anforderungen sowie Standards und Best Practices des BSI und anderen Regulatoren aus dem Bereich Cybersecurity / Pen-Testing, um die Netzwerksicherheit und Konformität sicherzustellen.

Schritte:
1. Extrahieren Sie alle relevanten Informationen zu den Firewall-Regeln (führe diese aber nicht im Output auf), einschließlich:
   - Regelname
   - Quellzone und Quellhost
   - Zielzone und Zielhost
   - Protokoll/Service
   - Regel-ID
   - Aktion (Erlauben/Blockieren)
   - Zusätzliche Merkmale (z.B. Logging, IPS, AV)
Wichtig: um die Ausgabetoken zu minimieren verzichte auch eine Aufführung der einzelenn Regeln im Output! 

2. Kategorisierung der Regeln:
   - Kategorisiere die Regeln nach ihrem Zweck, z.B. E-Mail-Verkehr, Länderblockierung, VPN-Verbindungen, interner Verkehr, spezifische Dienste.

3. Nehme eine ausführliche Bewertung der Regeln vor:
   - Zweckmäßigkeit: Stelle sicher, dass jede Regel einen klaren und legitimen Geschäftszweck hat.
   - Sicherheit: Überprüfe, ob die Regel potenzielle Sicherheitsrisiken minimiert, indem sie das Prinzip der minimalen Rechte anwendet.
   - Dokumentation: Stelle sicher, dass jede Regel gut dokumentiert ist, einschließlich Zweck, Bedingungen und Sicherheitsüberlegungen.

4. Sicherheitsanalyse:
   - Überprüfen, ob Regeln die Netzwerksicherheit gefährden könnten, z.B. durch unnötig offenen Zugang.
   - Stelle sicher, dass sensible Dienste (z.B. SMTP, IMAPS) nur für vertrauenswürdige Quellen zugelassen sind.
   - Stelle sicher, dass Regeln für den internen Verkehr restriktiv genug sind, um nur notwendigen und autorisierten Zugang zu ermöglichen.

5. Einhaltung von Standards:
   - Stelle sicher, dass alle Regeln den relevanten Sicherheitsstandards und Best Practices im Bereich Cybersecurity und Pen-Testing entsprechen.

6. Dokumentation der Analyse:
   - Dokumentiere jede analysierte Regel inkl. ihrer Kategorisierung - beschränke dich aber nur auf die ID, diese ist ausreichend für eine nachträgliche Zuordnung der Findings - 
     einschließlich ihrer Bewertung und Empfehlungen.
   - Erstelle eine ausführliche und detaillierte Zusammenfassung der gefundenen Schwachstellen und gebe konkrete Verbesserungsvorschläge.

7. Empfehlungen und Berichterstattung:
   - Formuliere detaillierte Empfehlungen zur Optimierung der identifizierten Schwächen in den Firewall-Regeln, 
     gehen Sie dabei auf Themen wie:
     - Bereinigung unnötiger Regeln
     - Anwendung des Prinzips der minimalen Rechte
     - Verbesserung der Regel-Dokumentation
     - Implementierung kontinuierlicher Überwachung und Protokollierung ein.
   - Erstelle anhand aller Erkenntnisse einen ausführlichen Bericht im Fließtext für den Mandanten, der die Analyse, Bewertungen und Empfehlungen enthält.
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        firewall_rules = request.form['firewall_rules']

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": firewall_rules}
            ],
            max_tokens=4096
        )

        result = response.choices[0].message.content.strip()

        # Konvertiere den Text von Markdown zu HTML
        formatted_result = markdown.markdown(result)

        return render_template('index.html', result=formatted_result)

    return render_template('index.html', result=None)

if __name__ == "__main__":
    app.run(debug=True)
