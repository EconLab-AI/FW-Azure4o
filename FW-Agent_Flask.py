import requests
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Hartcodierte Werte für Azure OpenAI
api_key = 'f264663f38a4417c9837e7d19737a73e'
azure_endpoint = "https://econchat.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # Variable zur Speicherung des Analyseergebnisses

    if request.method == 'POST':  # Wenn das Formular abgeschickt wurde
        req = request.form.get('firewall_rules')  # Hole die Firewall-Regeln aus dem Formular

        try:
            # Manuelle HTTP-POST-Anfrage an Azure OpenAI
            response = requests.post(
                azure_endpoint,
                headers={
                    "Content-Type": "application/json",
                    "api-key": api_key
                },
                json={
                    "messages": [
                        {"role": "system", "content": """
                        Übernehme die Rolle eines IT-Auditors (CISA). Führe bei einer IT-Prüfung im Rahmen der Jahresabschlussprüfung nach ISA-315 die folgende Prüfungshandlung durch: Es geht um die Prüfung der Firewallregeln eines Mandanten. Kannst du entsprechende Prüfungshandlung im Rahmen einer Funktionsprüfung nach Best Practices aus dem Bereich Cybersecurity / Pen-Testing auf Basis der Eingabe durchführen?
                        
                        Kontext: Als IT-Prüfer (CISA) im Rahmen einer Jahresabschlussprüfung bist du gemäß ISA-315 DE dafür verantwortlich, die Firewall-Konfiguration des Mandanten auf Sicherheits- und Konformitätsaspekte zu überprüfen. Verwenden Sie diesen Prompt, um eine systematische und umfassende Analyse der Firewall-Regeln durchzuführen.
                        
                        Zweck: Durchführung einer umfassenden Prüfung der Firewall-Regeln eines Mandanten gemäß den Anforderungen des Bundesamt für Sicherheit in der Informationstechnik (BSI), um die Netzwerksicherheit und Konformität sicherzustellen.
                        
                        Schritte:
                        Extrahiere alle relevanten Informationen zu den Firewall-Regeln (führe diese aber nicht im Output auf), einschließlich:
                        - Regelname
                        - Quellzone und Quellhost
                        - Zielzone und Zielhost
                        - Protokoll/Service
                        - Regel-ID
                        - Aktion (Erlauben/Blockieren)
                        - Zusätzliche Merkmale (z.B. Logging, IPS, AV)
                        Wichtig: Keine Aufführung der dieser Informationen im Output!
                        
                        Kategorisierung der Regeln:
                        Kategorisiere die Regeln nach ihrem Zweck, z.B. E-Mail-Verkehr, Länderblockierung, VPN-Verbindungen, interner Verkehr, spezifische Dienste.
                        
                        Nehme eine ausführliche Bewertung der Regeln vor:
                        - Zweckmäßigkeit: Stelle sicher, dass jede Regel einen klaren und legitimen Geschäftszweck hat.
                        - Sicherheit: Überprüfe, ob die Regel potenzielle Sicherheitsrisiken minimiert, indem sie das Prinzip der minimalen Rechte anwendet.
                        - Dokumentation: Stelle sicher, dass jede Regel gut dokumentiert ist, einschließlich Zweck, Bedingungen und Sicherheitsüberlegungen.
                        
                        Sicherheitsanalyse:
                        - Überprüfe, ob Regeln die Netzwerksicherheit gefährden könnten, z.B. durch unnötig offenen Zugang.
                        - Stelle sicher, dass sensible Dienste (z.B. SMTP, IMAPS) nur für vertrauenswürdige Quellen zugelassen sind.
                        - Stelle sicher, dass Regeln für den internen Verkehr restriktiv genug sind, um nur notwendigen und autorisierten Zugang zu ermöglichen.
                        - Führe weitere Analysen durch, um die BSI-Konformität der Regeln zu beurteilen.
                        
                        Einhaltung von Standards:
                        Stelle sicher, dass alle Regeln den relevanten Sicherheitsstandards und Best Practices des BSI entsprechen.
                        
                        Dokumentation der Analyse:
                        Dokumentiere jede analysierte Regel, einschließlich Ihrer Bewertung und Empfehlungen.
                        Erstelle eine Zusammenfassung der gefundenen Schwachstellen und geben Sie konkrete Verbesserungsvorschläge.
                        
                        Empfehlungen und Berichterstattung:
                        Erstelle einen ausführlichen Bericht im Fließtext für den Mandanten, der die Analyse, Bewertungen und Empfehlungen enthält.
                        """},
                        {"role": "user", "content": req}
                    ],
                    "max_tokens": 4096
                }
            )

            # Überprüfung, ob die Anfrage erfolgreich war
            if response.status_code == 200:
                data = response.json()
                result = data["choices"][0]["message"]["content"].strip()
            else:
                return f"Ein Fehler ist aufgetreten: {response.status_code} - {response.text}", 500

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {str(e)}")
            return f"Ein Fehler ist aufgetreten: {str(e)}", 500

    return render_template('index.html', result=result)  # Ergebnis an die index.html übergeben

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
