# Data

## Die Deutschen Inschriften
Im Projekt "Die Deutschen Inschriften" werden zwei verschiedene Tagsets verwendet:

- **DIO-Tagset**: Im Typo3-Portal erfasste Inschriften. 
  Das DIO-Portal stellt Lesefassungen für alle bislang veröffentlichten Bestände bereit.
  Das umfasst eine Großzahl ursprünglich mit Word erstellter Bände. 
  Die Transkriptionen sind bis auf eine kleine Anzahl von Tags 
  zur Strukturierung der Inhalte nicht explizit annotiert,
  sondern in Anlehnung an das Leidener Klammernsystem umgeschrieben. 
- **EPI-Tagset**: Im Epigraf-Redaktionssystem erfasste Inschriften.
  Epigraf wird aktuell und zukünftig für die Erfassung und die Bereitstellung 
  der Bestände als strukturierte Forschungsdaten verwendet.
  Die in Epigraf erfassten Bestände können in verschiedene Datenformate 
  wie Word, EpiDoc, Triples (JSON-LD etc.) sowie epiCSV, epiJSON und epiXML ausgespielt werden.

Alle im DIO-Portal vorhandenen Bestände sollen in Epigraf integriert werden,
um sie strukturiert veröffentlichen zu können.
Dazu sollen die Transkriptionen vom DIO-Tagset in das EPI-Tagset überführt 
und die Textauszeichnung (Leidener Klammernsystem) möglichst expliziert werden.

Ein zentraler Unterschied zwischen den beiden Tagsets besteht darin, dass ein Transkriptionsfeld in Epigraf
immer strikt nur eine Inschrift enthält. Dagegen sind im DIO-Transkriptionsfeld mehrere Inschriften
enthalten. Das bleibt vorerst auch so.

Ein zentraler Unterschied zu anderen möglichen Annotationssystemen besteht darin, dass der Bezugstext einer textkritischen 
Anmerkung (leider) nicht ausgezeichnet wird. Es werden immer nur Fußnoten hinter die Textstelle gesetzt.
Der Bezugstext wird dann in der Fußnote wiederholt. Fußnotentexte werden nicht im Transkriptionsfeld erfasst, sondern 
in einer eigenen Tabelle (`footnotes`). Die Fußnoten werden dafür über das Attribut `tagid` eindeutig identifiziert.

### DIO-Tagset

Die folgende Auflistung umfasst Tags, die sowohl in den Ursprungsdaten in der Typo3-Datenbank
enthalten sind (z.B. sco, sec,par), als auch  im Zug des Epigraf-Imports der DIO-Bestände
neu gebildete Tags (z.B. appalpha, appnum). Sie bilden das Ausgangsmaterial der Konvertierung.

| Tag      | Attribute | Beschreibung                                   |
|----------|-----------|------------------------------------------------|
| sco      |           | Container der Inschriften                      |                      
| sec      |           | Inschriftenteil                                |                    
| snr      |           | Inschriftennummer                              |                   
| appalpha | tagid     | Alphabetische Fußnote (textkritischer Apparat) | 
| appnum   | tagid     | Numerische Fußnote.                            |
| par      |           | Absatz                                         |
| lno      |           | Zeile                                          |
| lin      |           | Einrückung                                     |
| lig      |           | Ligatur                                        |
| em       |           | Hervorhebung                                   |
| strong   |           | Hervorhebung                                   |

Die Editionsrichtlinie des DI-Projekts sieht in Transkriptionstexten folgende Konventionen vor
(in Anlehnung an das Leidener Klammernsystem, Stand Februar 2025):

| Transkription                         | Bedeutung                                                                                                                                                                                                                                       | Beispiel       | 
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| Runde Klammern                        | Kürzungen werden in runden Klammern aufgelöst. Das Kürzungszeichen fällt dabei weg.                                                                                                                                                             | A(nno) D(omini) |
| Eckige Klammern                       | Verlorener Inschriftentext. Kann den ergänzten Text, falls nicht ergänzbar Punkte (jeder Punkt ein Zeichen) oder drei Gedankenstriche (ganze Zeile fehlt oder Umfang nicht abschätzbar) enthalten                                               | [...]          | 
| Spitze Klammern                       | Ursprünglich frei gelassene, nachträglich gefüllte Stellen, z.B. nachträgliche Sterbedaten. Kann den nachgetragenen Text, falls nicht vorhanden Punkte (jeder Punkt ein Zeichen) oder drei Gedankenstriche (Umfang nicht abschätzbar) enthalten | < >            |
| Großbuchstaben                        | Majuskelbuchstaben                                                                                                                                                                                                                              |                |
| Kleinbuchstaben (normale Textschrift) | Minuskelbuchstaben                                                                                                                                                                                                                              |                | 
| Vergrößerung oder Hervorhebung        | Chronogramme, Akrostiche u. ä.                                                                                                                                                                                                                  |                |
| Unterstreichung oder Bogen            | Nexus litterarum, Ligaturen und Bogenverbindungen                                                                                                                                                                                               |                |
| Punkt unter einem Buchstaben          | Nicht eindeutig lesbarer Buchstabe                                                                                                                                                                                                              |                | 
| Einfache Schrägstriche                | Zeilentrennungen der Inschrift, auch Richtungswechsel von Umschriften und Knicke von Schriftbändern. Ohne Spatien, wenn das Zeilenende im Wortinneren liegt, sonst mit.                                                                         | /              |
| Doppelte Schrägstriche                | Wechsel der Inschriften auf ein anderes Feld, innerhalb einer Zeile die Unterbrechung der Schrift z. B. durch Wappen, Ornamente oder bildliche Darstellung                                                                                      | //             |
| Zeilenumbruch                         | Versinschriften sind versweise zu setzen. Wenn durchgängig je ein Vers mit einer Zeile übereinstimmt, kann auf Wiedergabe der Zeilenumbrüche mit Schrägstrichen verzichtet werden                                                               |                |
| Gleichheitszeichen                    | Bei originalen Inschriften vorhandene Worttrennstriche am Zeilenende                                                                                                                                                                            | =              |
| Trennzeichen                          | Worttrennung nach Befund oder sinngemäß, auch bei scriptura continua eingesetzt                                                                                                                                                                 | -              |
| Mittelpunkt                           | Worttrennungszeichen wie Punkte, Zierpunkte, Rosetten, Kreuze, Glöckchen                                                                                                                                                                        | ·              |
| Interpunktion                         | Interpunktionszeichen werden beibehalten und möglichst mit ihren modernen Entsprechungen wiedergegeben; auf eine Unterscheidung zu Kürzungszeichen, vor allem im Falle von Punkt und Doppelpunkt, ist zu achten                                 | . :           |
| Punkt oder Komma                      | Worttrenner auf der Grundlinie                                                                                                                                                                                                                  | . ,            |
| Pluszeichen                           | Kreuze zu Beginn einer Inschrift                                                                                                                                                                                                                | +              |
| Hochstellung nach Zahlzeichen         | übergeschriebene oder hochgestellte Endungen bei Zahlzeichen werden hinter der Zahl hochgestellt.                                                                                                                                               |                |
| Buchstabenanmerkungen                 | Textkritischer Apparat. Abweichungen der Parallelüberlieferung, Besonderheiten, Auffälligkeiten.                                                                                                                                                |                |
| Ziffernanmerkungen                    | Allgemeiner Apparat. Nachweise und ergänzende Bemerkungen.                                                                                                                                                                                      |                | 

Weitere Merkmale werden im textkritischen Apparat erläutert, zum Beispiel:   
- Abweichungen von den Klammerregeln.  
- Wenn bei Versen auf die Kennzeichnung der Zeilen durch Schrägstriche verzichtet wurde (dann z.B. Hinweis auf "Elegische Distichen").
- Nicht wiedergegebene diakritische Zeichen, variable Spationierung innerhalb von Wörtern.  
- Der tatsächliche Befund bei Auflösung von Nomina sacra, die lautlich transkribiert werden. Beispiel: XC wird als CH(RISTV)S transkribiert.  
- Andere Arten von Buchstabenkombinationen als Nexus litterarum, Ligaturen und Bogenverbindungen.  
- Die Form von Worttrennern oder Kreuzen.  

**Siehe die Beispiele in dio_inschriften.csv**

### EPI-Tagset

Im EPI-Tagset werden drei verschiedene Auszeichnungsarten unterschieden:

- bracket: In der Darstellung wird eine Textstelle umklammert, im Markup von einem XML-Tag umschlossen.   
- text: In der Darstellung wird ein definierter Text ausgegeben, im Markup handelt es sich um ein leeres Tag.  
- format: Der ausgezeichnete Text wird formatiert dargestellt, zum Beispiel hochgestellt oder kursiv. Im Markup wird die Textstelle von einem XML-Tag umschlossen.  

Die Darstellung innerhalb der Epigraf-Anwendung orientiert sich am Leidener Klammersystem. 
Sie muss aber nicht mit der Darstellung in DIO-Transkriptionen übereinstimmen, ein Abgleich steht noch aus.

Nur selten werden in den Attributen direkt weitere Werte erfasst (del und spatium_v). 
Häufig wird dagegen auf eine Kategorienliste (properties) verwiesen. 
Jedes Tag hat dazu ein eindeutiges Attribut `tagid`, die Zuordnung erfolgt in einer eigenen Tabelle (links).

| Tag       | Tag Type | Caption             | Rendering    | Attributes | Properties                                                 | Description                                                                                                                                                                   |
|-----------|----------|---------------------|--------------|------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| abr       | bracket  | Abbreviation        | (TEXT)       |            |                                                            | Mark resolved abbreviations                                                                                                                                                   |
| all       | bracket  | Ligatures           | {TEXT}       | tagid      | ligatures (e.g. "nexus")                                   | Mark Nexus litterarum, ligatures, merged and connecting bows, enclaves, interlacing. Further explanations are given in an alphabetic footnote.                                |
| add       | bracket  | Addendum            | \<TEXT\>     |            |                                                            | Later additions on the inscription carrier                                                                                                                                    |
| bl        | bracket  | Block               |              | tagid      | alignments (e.g. "umlaufend")                              | Definition of the transcription area. For column arrangements, a container block with the property "column" and one child block for each column is used.                      |
| cpl       | bracket  | Addition            | [TEXT]       |            |                                                            | Lost characters that can be restored (whether conjecturally or from other witnesses)                                                                                          |
| oms       | bracket  | Ellipsis            | [(TEXT)]     |            |                                                            |                                                                                                                                                                               |
| app1      | text     | Numeric footnote    | 1            | tagid      |                                                            | Insert a numeric footnote for further explanations or citation references                                                                                                     |
| app2      | text     | Alphabetic footnote | a            | tagid      |                                                            | Insert an alphabetic footnote to clarify/explain readings or to present different readings in case of textual transmission through copies.                                    |
| del       | text     | Lost characters     | [---] or […] | num_sign   |                                                            | Lost characters that cannot be restored. In the rendering, each dot represents one character. For unknown quantities, three dashes (and an empty num_sign attribute) are used |
| spatium_v | text     | Spatium             |              | width      |                                                            |                                                                                                                                                                               |
| vz        | text     | Verse line break    | \|           | tagid      | indentations (indented or not indented, e.g. for distichs) | Verse line break, used to define the arrangement of the lines in verses. Inserted at line start.                                                                              |
| wtr       | text     | Word separator      | ·            | tagid      | wordseparators (e.g. "Blume")                              | Word separators                                                                                                                                                               |
| z         | text     | Line break          | /            | tagid      | linebindings (e.g. "Fragmentwechsel")                      | Line break. Inserted at line end (?).                                                                                                                                         |
| chr       | format   | Chronogram letter   |              |            |                                                            |                                                                                                                                                                               |
| ini       | format   | Initial             |              |            |                                                            |                                                                                                                                                                               |
| insec     | format   | Uncertain           |              |            |                                                            | Uncertain reading; appears in the DI-export document as a dot under the letter                                                                                                |
| kap       | format   | Small Capitals      |              |            |                                                            |                                                                                                                                                                               |                                                                             |
| sup       | format   | Superscript         |              | tagid      | verticalalignments (e.g. "unter der Oberlinie")            | Superscript, e.g., for displaying ordinal numbers                                                                                                                             |
| vsl       | format   | Versal              |              |            |                                                            | Display of letters as uppercase/Versal                                                                                                                                        |

 **Siehe die Konfiguration in epi_types.json.**