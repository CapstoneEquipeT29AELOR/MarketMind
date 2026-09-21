# MarketMind

## SEG4910 / SEG4911 — Projet de génie logiciel en fin d’études

### Équipe

| Membre | Numéro d’étudiant |
|---|---:|
| Erik Skjenna | 300273106 |
| Océane Prud’Homme | 300272920 |
| Lili Rose Théoret | 300342096 |
| Ryan Awad | 300273078 |
| Andy How Hok Hium | 300306884 |



## Type de projet: Type 2 — Marché ouvert 

## Description (Outline) 

- MarketMind est un projet de plateforme financière utilisant l’intelligence artificielle pour analyser les nouvelles et les tendances du marché boursier.
- Plus de détails seront ajoutés au fur et à mesure de la conception du projet. 


## Objectif (Objectives: benefit to customer, key things to accomplish, criteria for success): offrir aux clients une façon centralise de consulter les informations liées aux marches boursières. L’IA va facilite la consultation de plusieurs nouvelles et informations financière disponible. Le système devrait permettre de :  

- Réduire le temps nécessaire pour trouver des informations financières
- Présenter les informations de manière claire et facile a comprendre pour les utilisateurs
- Obtenir des analyse générées a partir des informations disponibles
- Suivre les tendances du marché 

## Voici unes listes d’objectif principales à accomplir :  

Un utilisateur peut consulter les principales informations du marché à partir d’une seule interface intuitive. 

Les nouvelles financières peuvent être récupérées et affichées correctement. 

L’IA peut générer des résumés cohérents à partir des nouvelles disponibles/consultés 


The main objective of MarketMind is to provide users with a centralized, clear and easy way to access stock market information. We will use artificial intelligence to help users process information from multiple financial sources more efficiently. Our system should allow users to:  

- Reduce the time needed to find financial information
- View information in a clear and easy way to understand
- Receive summaries and analysis generated from available information
- Follow market trends
- Understand relation between financial news, events and market movements.  


## Architecture anticipée (Expected/anticipated architecture) 

- Front end : Main UI provided to the user
- Back end: Handles AI-related functionality, financial/news data retrieval, data processing, and communication with external APIs.
- Useful tools for training and making predictions: https://auto.gluon.ai/stable/index.html and https://optuna.readthedocs.io/en/stable/
- Useful tools for pulling recent stock data: https://lmstudio.ai/

## Technologies envisagées 

- Front-end: React / Next.js
- Back-end: Python
- AI/ML: modèle LLM et bibliothèques Python appropriées
- Database: à déterminer selon les besoins du projet
- Financial data: API financière à déterminer
- News: API ou sources de nouvelles financières à déterminer
- Version control: Git / GitHub
- Development environment: VS Code 


## Risques anticipées (Anticipated risks: engineering challenges) 

- Performance: Consulter plusieurs Nouvelles et données financières pourrait avoir un impact sur les performances de l’application.
- Intégration de l’IA : nécessite plusieurs essais pour garantir des résultats pertinents et fiables
- Intégration des données : Les données financières et les nouvelles proviennent de différentes sources et donc varie et formats, limites et niveaux de disponibilité.  

 

## Problèmes juridiques ou sociales (Legal and social issues) 

- Ressources : les sources que l’on va utiliser devront respecter leurs conditions d’utilisation, licences et limites
- AI : les résultats produits par l’IA peuvent contenir des erreurs et donc on ne peux pas assurer l’information comme des conseil financiers.  

 

## Plan initial pour la première publication (Initial plans for first release, tool setup) 

1. Finaliser les exigences et le scope du projet 

2. Choisir les sources de données financières et de nouvelles 

3. Créer un premier prototype du dashboard 

4. Mettre en place le backend et la récupération des données 

5. Intégrer une première solution IA pour les résumer des nouvelles 

6. Ajouter des graphiques/analyse des tendances 

7. Tester l’intégration entre le front-end, le back-end et les services externes 

8. Effectuer des tests auprès des utilisateurs et récolter tout commentaires afin de corriger les problèmes 

9. Préparer une première version fonctionnelle pour démonstration 

 

## Scope du projet:  

- Front end: Dashboard principale avec l'info importante des récentes conclusions. Section de résumé des nouvelles financières, des tenances et l'analyse de l'AI avec des graphiquess
- IA: résumer des nouvelles, pas de promesse de prédiction
- Marchés analyses:  Indices boursiers (représentations de grandes entreprises: S&P 500, NASDAQ-100… ) et principales actions (entreprise individuelle : Apple, Microsoft, Tesla… ) 

## Sources consultees:  a rajouter

 

## Future Functionalities: the following functionalities may be considered for future versions of MarketMind but outside the MVP: 

- Trading automatique
- Comptes utilisateurs et personnalisation plus avancé
- Utilisation de plusieurs modèles d’IA pour sélectionner le plus efficace
- Prédiction automatisée du marché


## Market Review section:  

EToro: Financial markets news and analysis from eToro 

Advantages: 

- Provides a large variety of financial news and market analysis.  
- Covers stocks, ETFs, indices, crypto, commodities, and currencies.  
- Provides company and sector analysis with additional context.  
- Organizes information into different categories and types of articles.  
- Includes search functionality for finding specific financial instruments.  
- Provides charts and market information that help users follow market movements. 

Weaknesses:  

- The large amount of information can make it difficult to quickly identify the most important news.  
- Users may need to read several articles to understand the overall impact of an event.  
- Information from different sources is not necessarily summarized into one clear overview.  
- Users may need to make their own connections between financial news, market movements, and historical events.  
- Some of the available features are focused on investing and trading, which may be more than what a user looking only for market information needs. 
- A lot of navigation needed, a lot of pages and can be hard to find what you want to find.  

 

Analysis : Danel fin 

- The AI Score rates stocks and ETFs by their probability of beating the market over the next 3 months. 
- Uses an ensemble of decision trees and 10,000 features per stock. 
- Not much information about how they make predicitons. 
- They’re basically a big AI-powered analytics dashboard. 



Analysis : QuestTrade: 

- They’re different: Questrade helps people invest and trade; MarketMind would focus on news-based forecasts. 
- There’s overlap: Questrade already offers news, research, AI tools, and automation. 
- Explain the news: We could clearly show how a news event might affect a stock. 
- Compare past events: We could show what happened after similar news before. 
- Show uncertainty: We could explain each forecast’s confidence and conflicting evidence. 
- Prove our value: We could track successes and failures through paper trading before claiming better results. 
 

Analysis: RavenPack 

Advantages 

- Analyzes financial news and social-media information from 40,000+ sources. 
- Uses sentiment analysis to determine whether financial information is positive or negative. 
- Assigns relevance and novelty scores, helping identify news that is both important and genuinely new. 
- Automatically identifies companies, people, locations, products and events in financial news. 
- Uses a large taxonomy of 7,000+ event topics, allowing news to be categorized beyond simple positive/negative sentiment. 
- Provides historical and real-time news data, which can be useful for analyzing how news relates to stock movements. 
- Provides Factors, which turn large amounts of news, filings and transcripts into structured numerical signals that can be used in investment models. 
- Specifically targgets equity trading and says its analytics can be used as inputs to models predicting future stock returns. 

 

Weaknesses 

- RavenPack is primarily an institutional financial-data/analytics platform, rather than a simple application designed for individual investors. 
- Its large amount of data and analytics can be complex for users who simply want to understand why a stock moved. 
- The system provides signals and data rather than presenting one simple explanation of "what happened and why." 
- Users may still need to combine different signals and datasets to understand the relationship between news and stock-price movements. 
- RavenPack focuses heavily on providing data and analytical infrastructure, meaning the user or another system still needs to build the final prediction/decision model. 
- Its approach can be more sophisticated than necessary for users who only want basic financial news and stock information. 


Analysis: Perplexity Finance 

- AI-powered research — Users can ask questions in normal language instead of manually searching through financial websites.  
- Lots of information in one place — Combines news, stock prices, financial data, earnings, SEC filings, and other sources.  
- Saves time — Instead of reading many articles and documents, the AI can summarize the important information.  
- Easy-to-understand analysis — It can explain complicated financial information in simpler language.  
- Sources are provided — Users can check where the information came from, which is especially important for financial information.  
- Historical information — Users can look at past stock prices and financial information.  
- Stock screening — Users can search for stocks matching specific criteria instead of checking companies individually.  
- Can analyze financial documents — Useful for things like earnings reports and SEC filings.  
- Natural-language questions — You can ask something like "Why did NVIDIA's stock fall today?" instead of learning how to use a complicated financial platform.  
- Alerts and monitoring — Users can keep track of stocks and important events. 

Weaknesses 

- Can be overwhelming — There is a huge amount of information and many different features, which could be confusing for beginners.  
- Some advanced features/data may require paid access — Professional financial data and advanced capabilities aren't necessarily available to everyone for free.  
- Dependent on external data sources — If a source is unavailable, delayed, or incomplete, the resulting analysis can also be affected.  
- Financial information changes quickly — A response can become outdated as stock prices and news change.  
- Broad rather than specialized — It tries to cover many aspects of financial research rather than focusing on one specific task.  
- AI analysis isn't guaranteed financial advice — Users still need to make their own decisions rather than treating the AI's analysis as certain. 

 
## MEETING MINUTES SECTION

## Minutes - Meeting on Friday, September 11 (4pm to 5:30pm) - Everyone is present 

- Mock-up of a website by ChatGPT with burgundy/dark red, gold and white
- Separate website for new clients and another platform for existing clients?
- Initially: MVP and later full account
- Later: Login + accounts = more professional and personalization, user info
- Payroll for full access to the AI vs Free version with a less performant AI --> subscription based (not a percentage of our clients’ revenue because too much dependant on the markets)
- Macros
- AI provides only insights vs AI does the trades for the clients, maybe higher subscription fees for AI doing the trades
- Maybe have many different models, and for each trade choose the best model
- Use the cookies/tokens/things-based training (behaviors, not only words)
- AI goes through the news and other social medias like Twitter (watching for specific accounts, like Trump)
- Auto-trading could be interesting
- Look into the companies’ history to help make the link between events/news and the gains and losses on the stock markets (ex: Apple loses with iPhone 7 and audio-jack removal, then it goes back up when it comes back) --> these predictions can be made by LLMs (web search, APIs, open-source AIs) and then fine-tuned them afterwards so that there is a software engineering part to the project
- Confirm with teacher if we have a budget
- Importance of the front-end to attract clients
- Brainstorming over having a domain, link with an email domain, and potentially changing the name of the project
- Day and time for next meeting (Monday, in person after class) 

 

## Minutes - Meeting on Friday, September 14 (after class) - Everyone is present 

- Two algorithms (one for the news, one for the chart) that look at the prices separately and then we calculate the average. Possibly blend then together.
- Next step: Individually analyse the one similar company on the market and note the features that we want to keep or add to our product (we will then meet and compare on our side what we found) 


## Minutes – Meeting on Monday, September 21, 4:30pm – Everyone is present 

- Comparison of the companies in our market review
- More reflection on what specifically our product should be, the scope of the project 
- Each on our side we will brainstorm tasks that during the next reunion we will review. 
- We will work on a pipeline for next reunion, so that we can establish how we want to advance.  
