# Poli.
Introducting Poli, a platform designed the break the cycle of political isolation and misinformation. 
We recognize that many of us grew up disengaged from politics — often fed one-sided narratives by algorithm-driven news feeds. Thus, we built Poli to provide balanced, factual insights into political content. Using a modern, conversational chatbot interface, users can easily input political texts or speeches. Poli then leverages generative AI, large datasets, and logical reasoning to analyze the content for bias, extremity, subjectivity, and factual accuracy, while also noting keypoints and education takeaways. Our goal is to make political education accessible and help users form well-rounded opinions, paving the way for a more informed, critically engaged society. Looking forward, we aim to expand Poli’s reach globally and enhance the experience with interactive, personalized features for users to deepen their understanding and engagement.

## Inspiration
Our inspiration came from questioning how we consumed political content. In a simple experiment, we created two separate accounts on popular news and social media apps, Instagram and TikTok, to see what would happen if we only interacted with one unique side of the political spectrum. The results were stark: each account became a bubble of homogeneous opinions, drastically opposing the views of the other side. Content from either account mirrored the same magnitude of bias. This confirmed our suspicion that politics in algorithm-driven platforms tend to create echo chambers—filtering out diverse viewpoints and leaving users with a one-sided narrative. This spurred us to develop a platform where used can explore political content at your own pace, ask questions in a judgment-free environment, and gain insights that empower you to form well-rounded opinions about the news and political decisions affecting our communities.

## What it does
Poli offers a non-intimidating, accessible way for anyone to engage with politics, regardless of their previous level of interest or expertise. Our mission is to provide balanced, factual information that allows users to see multiple perspectives. Poli not only educates on the fundamentals of governing bodies and political processes but also helps users assess whether a text or speech carries any inadvertent bias, ensuring that you’re exposed to both sides of every issue without the interference of skewed algorithms or propaganda.

## How we built it
We built the platform using FastAPI and Python, validating user input using Pydantic models. It processes both plain text and web content (

Backend – Robust Data Processing: The backend, developed with FastAPI and asynchronous Python, validates user input using Pydantic models. It processes both plain text and web content (extracted via Requests and BeautifulSoup) to create a refined textual dataset. This dataset is then analyzed using OpenAI’s GPT-3.5-turbo via the ChatCompletion API, which returns structured JSON data including a quote (with the original text and a concise summary) and an analysis featuring numerical ratings for extremity, subjectivity, and accuracy. Comprehensive logging and error handling ensure reliable operation and transparency.

Frontend – Responsive User Interface: The frontend is built with React and styled with modern CSS, offering a user-friendly, chat-based interface. As users submit queries, asynchronous HTTP requests communicate with the backend, and the responses are dynamically rendered. Data visualizations, such as animated SVG-based rating circles, translate the numerical insights into clear, digestible information, enhancing the overall user experience, with the ability to interact with them to view the rationale/logic behind rating assignments.


## Challenges we ran into

## Accomplishments that we're proud of 


## Demo

## What's next for Poli.
Looking ahead, our vision for Poli is to evolve into a comprehensive platform for civic education and expand beyond just the US. We especially plan to bolster the educational experience by adding interactive features and personalized content that further enrich the learning experience, ensuring that users not only stay informed but also become active, critical thinkers in today’s complex political landscape.
Poli is more than just an app — it’s a step toward a more balanced, informed society where every individual has the opportunity to see the full picture, free from the limitations of echo chambers and misinformation.
